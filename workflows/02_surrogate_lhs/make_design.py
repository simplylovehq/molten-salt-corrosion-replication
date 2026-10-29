"""
Generate a Latin-hypercube design that mirrors Bhave & Tonks 2025 (JNM 606, 155616), Table 2,
optionally extended with extra factors (e.g. irradiation dose rate, temperature, salt redox potential).

Usage:  python make_design.py --n 100 --seed 1 --out ../../data/processed/design.csv
Then run one phase-field simulation per row and append results (mass_loss_mg_cm2, depth_um) to the CSV.
"""
import argparse, numpy as np, pandas as pd
from scipy.stats import qmc

BASE = {  # name: (low, high)  -- units: um
    "alloy_grain_um":   (5.0, 15.0),
    "coating_grain_um": (5.0, 15.0),
    "coating_thick_um": (30.0, 90.0),
}
EXTRA = {  # proposed extension factors (edit freely)
    "E_F_V": (3.30, 3.45),          # fluoride potential of salt (redox control), V
    "T_K":   (923.0, 1023.0),       # temperature
}

p = argparse.ArgumentParser()
p.add_argument("--n", type=int, default=100)
p.add_argument("--seed", type=int, default=1)
p.add_argument("--extended", action="store_true")
p.add_argument("--out", default="design.csv")
a = p.parse_args()

space = {**BASE, **(EXTRA if a.extended else {})}
lo = np.array([v[0] for v in space.values()]); hi = np.array([v[1] for v in space.values()])
X = qmc.scale(qmc.LatinHypercube(d=len(space), seed=a.seed).random(a.n), lo, hi)
df = pd.DataFrame(X, columns=list(space)); df.insert(0, "run_id", range(a.n))
df.to_csv(a.out, index=False); print(f"wrote {a.out}  ({a.n} x {len(space)})")
