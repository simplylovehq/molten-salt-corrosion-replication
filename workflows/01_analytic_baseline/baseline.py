"""
Analytic baseline for diffusion-limited Cr depletion (Bhave et al. 2023, JNM 574, 154147).

Implements:
  Eqs. 42-45  Arrhenius diffusivities (bulk, grain boundary) for Ni and Cr   [um^2/s]
  Eq.  46     Hart effective polycrystal diffusivity
  Eq.  50     semi-infinite-medium mass loss  dM = 2 (c0 - csurf) rho sqrt(D t / pi)

Purpose: a zero-cost 'sanity layer' that any new phase-field result (2D/3D, coating, irradiation)
can be compared against, and a cheap feature generator for surrogate models.
Run:  python baseline.py
"""
import numpy as np

R = 8.314  # J/mol/K

def D_arr(D0, Q, T):           # um^2/s
    return D0 * np.exp(-Q / (R * T))

def D_cr_bulk(T):  return D_arr(4.28e8, 2.852e5, T)   # Eq. 44
def D_cr_gb(T):    return D_arr(4.85e10, 1.962e5, T)  # Eq. 45
def D_ni_bulk(T):  return D_arr(1.9e8, 2.80e5, T)     # Eq. 42
def D_ni_gb(T):    return D_arr(7.0e6, 1.15e5, T)     # Eq. 43

def D_hart(Db, Dgb, d_gb_um, G_um):
    """Eq. 46: assumes GBs parallel to the diffusion direction."""
    f = d_gb_um / G_um
    return Db * (1 - f) + Dgb * f

def mass_loss_mg_cm2(D_um2_s, t_hours, c0_wt, csurf_wt, rho_g_cm3):
    """Eq. 50 in mg/cm^2."""
    D_cm2_s = D_um2_s * 1e-8
    t = t_hours * 3600.0
    return 2 * (c0_wt - csurf_wt) * rho_g_cm3 * np.sqrt(D_cm2_s * t / np.pi) * 1e3

# Experimental data from Zheng thesis, as tabulated in Bhave 2023 Table 3
CASES = {
    "Ni-5Cr":  dict(c0=0.05, rho=8.70, G=16.22, exp={50: 0.09, 500: 0.27, 1000: 0.42}),
    "Ni-20Cr": dict(c0=0.20, rho=8.57, G=4.64,  exp={50: 0.67, 500: 3.06, 1000: 7.12}),
}

if __name__ == "__main__":
    T, d_gb, c_surf = 973.0, 5e-4, 1.8e-3
    print(f"T = {T} K")
    print(f"D_Cr bulk = {D_cr_bulk(T):.3e}  D_Cr GB = {D_cr_gb(T):.3e} um^2/s")
    for name, c in CASES.items():
        Dh = D_hart(D_cr_bulk(T), D_cr_gb(T), d_gb, c["G"])
        Db = D_cr_bulk(T)
        print(f"\n{name}  (G = {c['G']} um)  D_Hart = {Dh:.3e}  D_bulk = {Db:.3e} um^2/s")
        print("  t[h]   exp    Hart    bulk-only   (mg/cm^2)")
        for t_h, m_exp in c["exp"].items():
            mh = mass_loss_mg_cm2(Dh, t_h, c["c0"], c_surf, c["rho"])
            mb = mass_loss_mg_cm2(Db, t_h, c["c0"], c_surf, c["rho"])
            print(f"  {t_h:5d}  {m_exp:5.2f}  {mh:6.2f}  {mb:9.3f}")
