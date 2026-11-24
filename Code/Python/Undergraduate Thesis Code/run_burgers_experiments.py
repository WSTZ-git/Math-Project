#!/usr/bin/env python3
"""
run_burgers_experiments.py
==========================
Numerical experiments for the parameterised IMEX-Euler splitting.

Usage
-----
    python run_burgers_experiments.py stiff
    python run_burgers_experiments.py maxdt
    python run_burgers_experiments.py shock
    python run_burgers_experiments.py conv
    python run_burgers_experiments.py all
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

import plot_style as ps
import burgers_imex as bi

os.makedirs("figures", exist_ok=True)
os.makedirs("data", exist_ok=True)

THETAS = [0.0, 0.25, 0.5, 0.75, 1.0]


# ==========================================================================
# experiment 1: stiffness phase diagram
# ==========================================================================
def exp_stiff():
    g = bi.Grid(0.0, 1.0, 200)
    dt = 0.4 * g.dx
    t_end = 1.0
    u0 = 0.5 + 0.01 * np.sin(2.0 * np.pi * g.x)
    thetas = np.linspace(0.0, 1.0, 41)
    nus = np.logspace(-2.0, 2.0, 21)
    growth = np.zeros((len(nus), len(thetas)))

    for i, nu in enumerate(nus):
        for j, theta in enumerate(thetas):
            res = bi.solve_burgers(u0, t_end, dt, nu, theta, g,
                                   periodic=True, blowup=1.0e6)
            growth[i, j] = np.max(np.abs(res["u"]))
        print(f"nu={nu:.3e} done")

    np.savez("data/stiff_heatmap.npz", thetas=thetas, nus=nus, growth=growth)
    with open("data/stiff_heatmap.csv", "w") as fh:
        fh.write("nu,theta,maxabs\n")
        for i, nu in enumerate(nus):
            for j, theta in enumerate(thetas):
                fh.write(f"{nu:.6e},{theta:.6f},{growth[i, j]:.6e}\n")

    fig, ax = plt.subplots(figsize=(5.0, 3.5))
    data = np.log10(np.clip(growth, 0.4, 1.0e3))
    im = ax.imshow(data, extent=[0.0, 1.0, -2.0, 2.0], origin="lower",
                   aspect="auto", cmap="RdYlBu_r", vmin=-0.4, vmax=1.8)
    ax.axvline(0.5, color="k", ls="--", lw=1.0)
    ax.set_xlabel(r"分裂参数 $\theta$")
    ax.set_ylabel(r"$\log_{10}\nu$")
    ax.set_title(r"增长因子 $\max|u|$（$\mathrm{CFL}=0.4$）")
    ax.text(0.05, 1.65, "稳定", color="k", fontsize=10)
    ax.text(0.58, 1.65, "不稳定", color="white", fontsize=10)
    cb = fig.colorbar(im, ax=ax, pad=0.02)
    cb.set_label(r"$\log_{10}\max|u|$")
    fig.tight_layout()
    ps.save(fig, "figures/stiff_heatmap.pdf")


# ==========================================================================
# experiment 2: maximum stable time step versus theta
# ==========================================================================
def _empirical_maxdt(theta, nu, g, u0, nsteps=20000, max_abs=0.55,
                     dt_pred=None):
    """Finite-step empirical stability threshold.

    A grid-scale perturbation of size 1e-8 is added to the initial data so
    that the sawtooth mode is seeded.  The run is advanced for a fixed number
    of steps (not to a fixed physical time), because stability is a per-step
    property.  For theta <= 1/2 the linear threshold is either a long-wave
    condition (not represented on the small periodic domain) or a very weak
    grid-scale growth; in that case the routine returns None instead of a
    misleading finite number.
    """
    if theta <= 0.5 + 1.0e-12:
        return None
    if dt_pred is None:
        dt_pred = bi.max_stable_dt_symbol(g.dx, nu, theta)
    lo = 0.5 * dt_pred
    hi = 2.0 * dt_pred

    def stable(dt):
        res = bi.solve_burgers(u0, nsteps * dt, dt, nu, theta, g,
                               periodic=True, blowup=max_abs)
        return res["status"] == "ok" and np.max(np.abs(res["u"])) <= max_abs

    while not stable(lo):
        lo *= 0.5
    while stable(hi) and hi < 10.0:
        hi *= 2.0
    if hi >= 10.0:
        return None
    for _ in range(25):
        mid = 0.5 * (lo + hi)
        if stable(mid):
            lo = mid
        else:
            hi = mid
    return lo


def exp_maxdt():
    g = bi.Grid(0.0, 1.0, 200)
    nu = 1.0
    # Smooth large-scale perturbation plus a tiny grid-scale seed.  Without
    # the seed the sawtooth mode is not excited and the finite-time test
    # overestimates the threshold for theta close to 1/2.
    u0 = (0.5 + 1.0e-3 * np.sin(2.0 * np.pi * g.x)
          + 1.0e-8 * (-1.0) ** np.arange(g.N))
    thetas = np.linspace(0.0, 1.0, 101)
    dt_pred = np.array([bi.max_stable_dt_symbol(g.dx, nu, t) for t in thetas])

    emp_theta = [0.55, 0.6, 0.75, 1.0]
    emp_dt = []
    for t in emp_theta:
        d = _empirical_maxdt(t, nu, g, u0,
                             dt_pred=bi.max_stable_dt_symbol(g.dx, nu, t))
        emp_dt.append(np.nan if d is None else d)
        print(f"empirical theta={t:.2f}: {d}")

    with open("data/maxdt.csv", "w") as fh:
        fh.write("theta,dt_pred\n")
        for t, d in zip(thetas, dt_pred):
            fh.write(f"{t:.6f},{d:.6e}\n")
        fh.write("# empirical\n")
        for t, d in zip(emp_theta, emp_dt):
            fh.write(f"{t:.6f},{d:.6e}\n")

    fig, ax = plt.subplots(figsize=(5.2, 3.3))
    ax.semilogy(thetas, dt_pred, color=ps.C["blue"], lw=1.8,
                label="线性稳定性预测")
    good = np.isfinite(emp_dt)
    ax.semilogy(np.array(emp_theta)[good], np.array(emp_dt)[good], "o",
                color=ps.C["red"], ms=5, label="非线性实验")
    ax.axvline(0.5, color="k", ls="--", lw=1.0)
    ax.axhline(g.dx, color=ps.C["grey"], ls=":", lw=0.9)
    ax.text(0.505, 3.0e-1, r"$\theta=1/2$", fontsize=9)
    ax.text(0.02, 1.2 * g.dx, r"$\Delta t=\Delta x$", fontsize=8,
            color=ps.C["grey"])
    ax.set_xlabel(r"分裂参数 $\theta$")
    ax.set_ylabel(r"最大稳定步长 $\Delta t_{\max}$")
    ax.set_title(r"最大稳定步长（$\nu=1$，$N=200$）")
    ax.set_ylim(1.0e-6, 5.0)
    ax.legend(fontsize=8.5, frameon=False, loc="upper right")
    fig.tight_layout()
    ps.save(fig, "figures/maxdt.pdf")
    print("empirical:", emp_theta, emp_dt)


# ==========================================================================
# experiment 3: viscous shock accuracy
# ==========================================================================
def exp_shock():
    g = bi.Grid(-2.0, 3.0, 800)
    nu = 0.01
    cfl = 0.2
    dt = cfl * g.dx
    t_end = 2.0
    u0 = bi.exact_viscous_shock(g.x, 0.0, nu)

    rows = ["theta,order,l1,linf,pos_err,width,width_err"]
    profiles = {}
    for order in (1, 2):
        for theta in THETAS:
            res = bi.solve_burgers(u0, t_end, dt, nu, theta, g, 1.0, 0.0,
                                   order=order)
            if res["status"] != "ok":
                print("BLOWUP", theta, order)
                continue
            m = bi.shock_metrics(g.x, res["u"], res["t"], nu)
            rows.append(f"{theta},{order},{m['l1']:.6e},{m['linf']:.6e},"
                        f"{m['shock_pos_error']:.6e},{m['width']:.6e},"
                        f"{m['width_error']:.6e}")
            if order == 2:
                profiles[theta] = res["u"].copy()
            print(f"order={order} theta={theta} l1={m['l1']:.4e} "
                  f"pos={m['shock_pos_error']:+.5f} width={m['width']:.5f}")

    open("data/shock_metrics.csv", "w").write("\n".join(rows) + "\n")
    np.savez("data/shock_profiles.npz", x=g.x, **{f"u{t}": profiles[t]
                                                  for t in profiles})

    # figure: profiles
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.1),
                                   gridspec_kw={"width_ratios": [1.35, 1.0]})
    xe = np.linspace(-2.0, 3.0, 2000)
    ue = bi.exact_viscous_shock(xe, t_end, nu)
    ax1.plot(xe, ue, "k--", lw=1.0, label="精确解")
    for theta, col in [(0.0, ps.C["blue"]), (0.5, ps.C["green"]),
                       (1.0, ps.C["red"])]:
        ax1.plot(g.x, profiles[theta], color=col, lw=1.1,
                 label=rf"$\theta={theta:g}$")
    ax1.set_xlim(-0.4, 1.6)
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$u$")
    ax1.set_title(r"(a) $t=2$ 时的激波剖面")
    ax1.legend(fontsize=8, frameon=False, loc="upper right")

    # figure: error metrics (MUSCL)
    th = np.array(THETAS)
    l1 = np.array([float(r.split(",")[2]) for r in rows[1:]
                   if r.split(",")[1] == "2"])
    pos = np.array([float(r.split(",")[4]) for r in rows[1:]
                    if r.split(",")[1] == "2"])
    wid = np.array([float(r.split(",")[6]) for r in rows[1:]
                    if r.split(",")[1] == "2"])
    ax2.semilogy(th, l1, "o-", color=ps.C["blue"], label=r"$L^1$ 误差")
    ax2.set_xlabel(r"分裂参数 $\theta$")
    ax2.set_ylabel(r"$L^1$ 误差")
    ax2.set_title(r"(b) 误差随 $\theta$ 的变化（MUSCL）")
    ax2b = ax2.twinx()
    ax2b.plot(th, np.abs(pos) * 1e4, "s--", color=ps.C["orange"],
              label=r"$|x_s-x_s^{\rm ex}|\times 10^4$")
    ax2b.plot(th, np.abs(wid) * 1e4, "^:", color=ps.C["green"],
              label=r"$|w-w^{\rm ex}|\times 10^4$")
    ax2b.set_ylabel("位置/厚度误差（$\\times 10^{-4}$）")
    lines = ax2.get_lines() + ax2b.get_lines()
    ax2.legend(lines, [l.get_label() for l in lines], fontsize=7.2,
               frameon=False, loc="upper left")
    fig.tight_layout()
    ps.save(fig, "figures/shock_profiles.pdf")


# ==========================================================================
# experiment 4: convergence under refinement
# ==========================================================================
def exp_conv():
    nu = 0.01
    cfl = 0.2
    t_end = 1.0
    Ns = [100, 200, 400, 800]
    rows = ["N,theta,order,dx,l1"]
    for order in (1, 2):
        for theta in (0.0, 0.5):
            for N in Ns:
                g = bi.Grid(-2.0, 3.0, N)
                dt = cfl * g.dx
                u0 = bi.exact_viscous_shock(g.x, 0.0, nu)
                res = bi.solve_burgers(u0, t_end, dt, nu, theta, g, 1.0, 0.0,
                                       order=order)
                m = bi.shock_metrics(g.x, res["u"], res["t"], nu)
                rows.append(f"{N},{theta},{order},{g.dx:.6e},{m['l1']:.6e}")
                print(f"order={order} theta={theta} N={N} l1={m['l1']:.4e}")
    open("data/convergence.csv", "w").write("\n".join(rows) + "\n")

    fig, ax = plt.subplots(figsize=(4.8, 3.2))
    for order, theta, marker, col in [
            (1, 0.5, "s", ps.C["grey"]), (2, 0.0, "o", ps.C["blue"]),
            (2, 0.5, "^", ps.C["green"])]:
        ns = [100, 200, 400, 800]
        errs = []
        for n in ns:
            for r in rows[1:]:
                p = r.split(",")
                if int(p[0]) == n and float(p[1]) == theta and int(p[2]) == order:
                    errs.append(float(p[4]))
        ax.loglog(ns, errs, marker + "-", color=col,
                  label=rf"order {order}, $\theta={theta:g}$")
    ax.set_xlabel(r"网格数 $N$")
    ax.set_ylabel(r"$L^1$ 误差")
    ax.set_title("网格收敛性（移动激波）")
    ax.legend(fontsize=8, frameon=False)
    ax.grid(True, which="both", alpha=0.25, lw=0.5)
    fig.tight_layout()
    ps.save(fig, "figures/convergence.pdf")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("stiff", "all"):
        exp_stiff()
    if what in ("maxdt", "all"):
        exp_maxdt()
    if what in ("shock", "all"):
        exp_shock()
    if what in ("conv", "all"):
        exp_conv()
