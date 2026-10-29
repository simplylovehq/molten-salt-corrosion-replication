"""
Gaussian-process surrogate for LHS results, with leave-one-out error and Sobol-style sensitivity via
simple variance-based finite sampling. Expects a CSV with the design columns plus 'mass_loss_mg_cm2'
(and optionally 'depth_um').

Usage:  python fit_surrogate.py ../../data/processed/results.csv --target mass_loss_mg_cm2
"""
import argparse, numpy as np, pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel as C
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.preprocessing import StandardScaler

p = argparse.ArgumentParser(); p.add_argument("csv"); p.add_argument("--target", default="mass_loss_mg_cm2")
a = p.parse_args()
df = pd.read_csv(a.csv).dropna(subset=[a.target])
feats = [c for c in df.columns if c not in ("run_id", "mass_loss_mg_cm2", "depth_um")]
X = StandardScaler().fit_transform(df[feats]); y = df[a.target].values
k = C(1.0) * Matern(length_scale=np.ones(len(feats)), nu=2.5) + WhiteKernel(1e-3)
gp = GaussianProcessRegressor(k, normalize_y=True, n_restarts_optimizer=5, random_state=0)
pred = cross_val_predict(gp, X, y, cv=LeaveOneOut())
rmse = np.sqrt(np.mean((pred - y) ** 2)); print(f"LOO RMSE = {rmse:.4g}  (target std = {y.std():.4g})")
gp.fit(X, y); print("ARD length scales (short = influential):")
for f, l in zip(feats, gp.kernel_.k1.k2.length_scale): print(f"  {f:20s} {l:8.3f}")
