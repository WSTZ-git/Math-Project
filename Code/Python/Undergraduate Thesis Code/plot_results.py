#!/usr/bin/env python3
"""
plot_results.py
===============
Read the cached CSV/NPZ data produced by run_burgers_experiments.py and
draw the final thesis figures with a consistent style.
"""

import numpy as np
import matplotlib.pyplot as plt

import plot_style as ps

# --------------------------------------------------------------------------
# stiffness heat map
# --------------------------------------------------------------------------
d = np.load("data/stiff_heatmap.npz")
thetas, nus, growth = d["thetas"], d["nus"], d["growth"]
fig, ax = plt.subplots(figsize=(5.0, 3.4))
data = np.log10(np.clip(growth, 0.4, 63.0))
im = ax.imshow(data, extent=[0.0, 1.0, -2.0, 2.0], origin="lower",
               aspect="auto", cmap="RdYlBu_r", vmin=-0.4, vmax=1.8)
ax.axvline(0.5, color="k", ls="--", lw=1.0)
ax.set_xlabel(r"分裂参数 $\theta$")
ax.set_ylabel(r"$\log_{10}\nu$")
ax.set_title(r"增长因子 $\max|u|$（$\mathrm{CFL}=0.4$，$t=1$）")
ax.text(0.04, 1.62, "稳定", color="k", fontsize=10)
ax.text(0.57, 1.62, "不稳定", color="white", fontsize=10)
cb = fig.colorbar(im, ax=ax, pad=0.02)
cb.set_label(r"$\log_{10}\max|u|$")
fig.tight_layout()
ps.save(fig, "figures/stiff_heatmap.pdf")


# --------------------------------------------------------------------------
# maximum stable time step
# --------------------------------------------------------------------------
curve, emp = [], []
mode = "curve"
for line in open("data/maxdt.csv"):
    line = line.strip()
    if not line or line.startswith("theta"):
        continue
    if line.startswith("#"):
        mode = "emp"
        continue
    t, dtv = (float(v) for v in line.split(","))
    (curve if mode == "curve" else emp).append((t, dtv))
curve = np.array(curve)
emp = np.array(emp)

fig, ax = plt.subplots(figsize=(5.2, 3.3))
ax.semilogy(curve[:, 0], curve[:, 1], color=ps.C["blue"], lw=1.8,
            label="线性稳定性预测")
ax.semilogy(emp[:, 0], emp[:, 1], "o", color=ps.C["red"], ms=5.0,
            label="非线性实验")
ax.axvline(0.5, color="k", ls="--", lw=1.0)
ax.axhline(0.005, color=ps.C["grey"], ls=":", lw=0.9)
ax.text(0.505, 0.35, r"$\theta=1/2$", fontsize=9)
ax.text(0.02, 0.0058, r"$\Delta t=\Delta x$", fontsize=8, color=ps.C["grey"])
ax.set_xlabel(r"分裂参数 $\theta$")
ax.set_ylabel(r"最大稳定步长 $\Delta t_{\max}$")
ax.set_title(r"最大稳定步长（$\nu=1$，$N=200$）")
ax.set_ylim(1.0e-6, 5.0)
ax.legend(fontsize=8.5, frameon=False, loc="upper right")
fig.tight_layout()
ps.save(fig, "figures/maxdt.pdf")


# --------------------------------------------------------------------------
# shock profiles and error metrics
# --------------------------------------------------------------------------
metrics = {}
for line in open("data/shock_metrics.csv"):
    line = line.strip()
    if not line or line.startswith("theta"):
        continue
    p = line.split(",")
    metrics[(float(p[0]), int(p[1]))] = {
        "l1": float(p[2]), "linf": float(p[3]), "pos": float(p[4]),
        "width": float(p[5]), "werr": float(p[6]),
    }
prof = np.load("data/shock_profiles.npz")
x = prof["x"]

th = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.9),
                         gridspec_kw={"width_ratios": [1.25, 1.0, 1.0]})
ax = axes[0]
xe = np.linspace(-2.0, 3.0, 2000)
nu = 0.01
ue = 1.0 / (1.0 + np.exp((xe - 1.0) / (2.0 * nu)))
ax.plot(xe, ue, "k--", lw=1.0, label="精确解")
for theta, col in [(0.0, ps.C["blue"]), (0.5, ps.C["green"]),
                   (1.0, ps.C["red"])]:
    ax.plot(x, prof[f"u{theta}"], color=col, lw=1.2,
            label=rf"$\theta={theta:g}$")
ax.set_xlim(0.75, 1.25)
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$u$")
ax.set_title(r"(a) $t=2$ 时的粘性激波剖面", fontsize=9.0)
ax.legend(fontsize=8.0, frameon=False, loc="upper right")

ax = axes[1]
for order, col, mk in [(1, ps.C["grey"], "s"), (2, ps.C["blue"], "o")]:
    vals = [metrics[(t, order)]["l1"] for t in th]
    ax.semilogy(th, vals, mk + "-", color=col, ms=4.0,
                label=rf"order {order}")
ax.set_xlabel(r"分裂参数 $\theta$")
ax.set_ylabel(r"$L^1$ 误差")
ax.set_title(r"(b) $L^1$ 误差", fontsize=9.0)
ax.legend(fontsize=8, frameon=False)
ax.grid(True, which="both", alpha=0.2, lw=0.5)

ax = axes[2]
for order, col, mk in [(1, ps.C["grey"], "s"), (2, ps.C["green"], "^")]:
    vals = [abs(metrics[(t, order)]["werr"]) for t in th]
    ax.semilogy(th, vals, mk + "-", color=col, ms=4.0,
                label=rf"order {order}")
ax.set_xlabel(r"分裂参数 $\theta$")
ax.set_ylabel(r"$|w-w_{\rm ex}|$")
ax.set_title(r"(c) 过渡层厚度误差", fontsize=9.0)
ax.legend(fontsize=8, frameon=False)
ax.grid(True, which="both", alpha=0.2, lw=0.5)

fig.tight_layout()
ps.save(fig, "figures/shock_results.pdf")


# --------------------------------------------------------------------------
# convergence
# --------------------------------------------------------------------------
rows = []
for line in open("data/convergence.csv"):
    line = line.strip()
    if not line or line.startswith("N"):
        continue
    p = line.split(",")
    rows.append((int(p[0]), float(p[1]), int(p[2]), float(p[4])))

fig, ax = plt.subplots(figsize=(4.9, 3.2))
for order, theta, col, mk in [(1, 0.5, ps.C["grey"], "s"),
                              (2, 0.0, ps.C["blue"], "o"),
                              (2, 0.5, ps.C["green"], "^")]:
    ns = sorted({r[0] for r in rows})
    vals = [next(r[3] for r in rows if r[0] == n and r[1] == theta
                 and r[2] == order) for n in ns]
    p = np.log(vals[0] / vals[-1]) / np.log(ns[-1] / ns[0])
    ax.loglog(ns, vals, mk + "-", color=col,
              label=rf"order {order}, $\theta={theta:g}$（斜率 {p:.2f}）")
ax.set_xlabel(r"网格数 $N$")
ax.set_ylabel(r"$L^1$ 误差")
ax.set_title(r"网格收敛性（$t=1$ 的移动粘性激波）")
ax.legend(fontsize=7.6, frameon=False, loc="lower left")
ax.grid(True, which="both", alpha=0.2, lw=0.5)
fig.tight_layout()
ps.save(fig, "figures/convergence.pdf")

print("figures done")
