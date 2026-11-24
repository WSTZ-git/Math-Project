#!/usr/bin/env python3
"""
run_jinxin_experiments.py
=========================
Stability and numerical experiments for the two Jin-Xin source splittings.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

import plot_style as ps
import jinxin as jx
from burgers_imex import Grid

os.makedirs("figures", exist_ok=True)
os.makedirs("data", exist_ok=True)

MUS = [0.1, 1.0, 10.0, 100.0, 1.0e4]
CFLS = np.linspace(0.05, 1.0, 39)


# --------------------------------------------------------------------------
# spectral radius maps
# --------------------------------------------------------------------------
def stability_maps():
    rows = ["strategy,mu,cfl,rho"]
    data = {"A": {}, "B": {}}
    for strat in ("A", "B"):
        for mu in MUS:
            vals = [jx.max_spectral_radius(c, mu, strat, nxi=801)
                    for c in CFLS]
            data[strat][mu] = np.array(vals)
            for c, v in zip(CFLS, vals):
                rows.append(f"{strat},{mu:.6e},{c:.6e},{v:.9e}")
    open("data/jinxin_stability.csv", "w").write("\n".join(rows) + "\n")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.4, 2.8), sharey=True)
    for ax, strat, title in [(ax1, "A", "(a) 策略 A：源项全隐式"),
                             (ax2, "B", "(b) 策略 B：仅线性部分隐式")]:
        for mu, col in zip(MUS, [ps.C["sky"], ps.C["blue"], ps.C["green"],
                                 ps.C["orange"], ps.C["red"]]):
            ax.plot(CFLS, data[strat][mu], color=col,
                    label=rf"$\mu={mu:g}$")
        ax.axhline(1.0, color="k", ls="--", lw=0.9)
        ax.set_xlabel(r"$\mathrm{CFL}=a\Delta t/\Delta x$")
        ax.set_title(title)
        ax.set_ylim(0.98, 1.25)
    ax1.set_ylabel(r"$\rho(M)$")
    ax1.legend(fontsize=7.5, frameon=False, ncol=2)
    ax2.axvline(1.0 / 3.0, color=ps.C["grey"], ls=":", lw=0.9)
    ax2.text(0.345, 1.22, r"$1/3$", fontsize=8, color=ps.C["grey"])
    fig.tight_layout()
    ps.save(fig, "figures/jinxin_stability.pdf")


# --------------------------------------------------------------------------
# critical CFL of strategy B versus stiffness
# --------------------------------------------------------------------------
def critical_cfl():
    mus = np.logspace(-1, 4, 11)
    crit = [jx.critical_cfl_stiff("B", mu=m, c_lo=0.05, c_hi=1.2)
            for m in mus]
    rows = ["mu,cfl_crit"] + [f"{m:.6e},{c:.6e}" for m, c in zip(mus, crit)]
    open("data/jinxin_critical.csv", "w").write("\n".join(rows) + "\n")

    fig, ax = plt.subplots(figsize=(4.6, 3.1))
    ax.semilogx(mus, crit, "o-", color=ps.C["red"])
    ax.axhline(1.0 / 3.0, color=ps.C["grey"], ls="--", lw=0.9)
    ax.text(0.15, 0.345, r"$1/3$", fontsize=9, color=ps.C["grey"])
    ax.set_xlabel(r"刚性参数 $\mu=\Delta t/\varepsilon$")
    ax.set_ylabel(r"临界 $\mathrm{CFL}$")
    ax.set_title("策略 B 的容许 CFL 随刚性的变化")
    ax.set_ylim(0.25, 1.05)
    fig.tight_layout()
    ps.save(fig, "figures/jinxin_critical.pdf")
    print("critical:", mus, crit)


# --------------------------------------------------------------------------
# numerical comparison on the Riemann problem
# --------------------------------------------------------------------------
def numerics():
    g = Grid(-1.0, 1.0, 400)
    a = 1.0
    eps = 1.0e-4
    t_end = 1.0
    u0 = np.where(g.x < 0.0, 1.0, 0.0)
    v0 = jx.f_burgers(u0)
    ue = jx.exact_riemann(g.x, t_end)

    rows = ["strategy,cfl,status,l1,maxu,maxv,eq_res"]
    profiles = {}
    for strat in ("A", "B"):
        for cfl in (0.3, 0.5, 0.7):
            dt = cfl * g.dx
            res = jx.solve_jinxin(u0, v0, t_end, dt, eps, a, g,
                                  strategy=strat, uL=1.0, uR=0.0,
                                  blowup=1.0e2)
            if res["status"] == "ok":
                l1 = np.trapezoid(np.abs(res["u"] - ue), g.x) / 2.0
            else:
                l1 = np.nan
            eq = np.max(np.abs(res["v"] - jx.f_burgers(res["u"])))
            rows.append(f"{strat},{cfl},{res['status']},{l1:.6e},"
                        f"{np.max(np.abs(res['u'])):.6e},"
                        f"{np.max(np.abs(res['v'])):.6e},{eq:.6e}")
            profiles[(strat, cfl)] = res["u"].copy()
            print(strat, cfl, res["status"], l1)
    open("data/jinxin_numerics.csv", "w").write("\n".join(rows) + "\n")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.4, 2.8),
                                   gridspec_kw={"width_ratios": [1.35, 1.0]})
    ax1.plot(g.x, ue, "k--", lw=1.0, label="精确解")
    ax1.plot(g.x, profiles[("A", 0.3)], color=ps.C["blue"], lw=1.2,
             label=r"A, $\mathrm{CFL}=0.3$")
    ax1.plot(g.x, profiles[("B", 0.3)], color=ps.C["orange"], lw=1.2,
             label=r"B, $\mathrm{CFL}=0.3$")
    ax1.plot(g.x, profiles[("A", 0.7)], color=ps.C["green"], lw=1.2,
             label=r"A, $\mathrm{CFL}=0.7$")
    ax1.set_xlim(-0.4, 0.9)
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$u$")
    ax1.set_title(r"(a) $t=1$ 时的松弛解（$\varepsilon=10^{-4}$）")
    ax1.legend(fontsize=7.8, frameon=False, loc="upper right")

    cfls = [0.3, 0.5, 0.7]
    for strat, col, mk in [("A", ps.C["blue"], "o"), ("B", ps.C["red"], "s")]:
        vals = [float(next(r.split(",")[3] for r in rows[1:]
                           if r.split(",")[0] == strat
                           and float(r.split(",")[1]) == c)) for c in cfls]
        vals = np.array(vals, dtype=float)
        good = np.isfinite(vals)
        ax2.semilogy(np.array(cfls)[good], vals[good], mk + "-",
                     color=col, label=f"策略 {strat}")
    ax2.axvline(1.0 / 3.0, color=ps.C["grey"], ls=":", lw=0.9)
    ax2.set_xlabel(r"$\mathrm{CFL}$")
    ax2.set_ylabel(r"$L^1$ 误差")
    ax2.set_title("(b) 误差与稳定性")
    ax2.legend(fontsize=8, frameon=False, loc="lower left")
    fig.tight_layout()
    ps.save(fig, "figures/jinxin_numerics.pdf")


if __name__ == "__main__":
    stability_maps()
    critical_cfl()
    numerics()
