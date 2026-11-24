#!/usr/bin/env python3
"""
stability_analysis.py
=====================
Linear stability analysis of the parameterised IMEX-Euler splitting

    R(z_E, z_I) = (1 + z_E) / (1 - z_I).

Outputs
-------
figures/stability_geometry.pdf   stability disks and the coupled stiff ray
figures/stability_region.pdf     exact phase diagram in (theta, |z_D|)
figures/stability_coupled.pdf    continuous joint stability region mu_max(d)
                                 and beta_inf(epsilon)
figures/stability_discrete.pdf   |R(xi)| for the fully discrete symbol
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.colors import TwoSlopeNorm

import plot_style as ps
from burgers_imex import Grid, amplification

os.makedirs("figures", exist_ok=True)
os.makedirs("data", exist_ok=True)


def R_ray(theta, x):
    """R along z_D = -x, z_E = -theta x, z_I = -(1-theta) x."""
    z_e = -theta * x
    z_i = -(1.0 - theta) * x
    return (1.0 + z_e) / (1.0 - z_i)


# --------------------------------------------------------------------------
# figure 1: stability disk at a fixed stiffness and growth along the ray
# --------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.6, 2.9))

x0 = 10.0
for theta, col in [(0.25, ps.C["blue"]), (0.75, ps.C["red"])]:
    z_i = -(1.0 - theta) * x0
    radius = 1.0 - z_i
    ax1.add_patch(Circle((-1.0, 0.0), radius, facecolor=col, alpha=0.08,
                         edgecolor=col, lw=1.2, ls="--"))
    ax1.plot([-theta * x0], [0.0], "o", color=col, ms=8, zorder=5)

ax1.annotate(r"$\theta=0.25$：圆内", xy=(-2.5, 0.0), xytext=(-5.6, 4.3),
             color=ps.C["blue"], fontsize=8.8, ha="center",
             arrowprops=dict(arrowstyle="->", color=ps.C["blue"], lw=0.9))
ax1.annotate(r"$\theta=0.75$：圆外", xy=(-7.5, 0.0), xytext=(-8.6, -3.2),
             color=ps.C["red"], fontsize=8.8, ha="center",
             arrowprops=dict(arrowstyle="->", color=ps.C["red"], lw=0.9))
ax1.axhline(0.0, color=ps.C["grey"], lw=0.5)
ax1.axvline(-1.0, color=ps.C["grey"], lw=0.5, ls=":")
ax1.set_xlim(-12.0, 2.5)
ax1.set_ylim(-9.0, 9.0)
ax1.set_xlabel(r"$\mathrm{Re}\,z_E$")
ax1.set_ylabel(r"$\mathrm{Im}\,z_E$")
ax1.set_title(r"(a) 固定 $|z_D|=10$ 时的稳定域圆盘")
ax1.set_aspect("equal")

x = np.logspace(-2, 2.5, 500)
for theta, col in [(0.0, ps.C["blue"]), (0.25, ps.C["sky"]),
                   (0.5, ps.C["green"]), (0.75, ps.C["orange"]),
                   (1.0, ps.C["red"])]:
    ax2.semilogx(x, np.abs(R_ray(theta, x)), color=col,
                 label=rf"$\theta={theta:g}$")
    if theta < 1.0:
        ax2.axhline(theta / (1.0 - theta), color=col, ls=":", lw=0.8)
ax2.axhline(1.0, color=ps.C["black"], lw=1.0, ls="--")
ax2.set_xscale("log")
ax2.set_xticks([1e-2, 1e-1, 1e0, 1e1, 1e2])
ax2.set_xticklabels([r"$10^{-2}$", r"$10^{-1}$", r"$10^{0}$",
                     r"$10^{1}$", r"$10^{2}$"])
ax2.set_xlabel(r"耗散强度 $|z_D|$")
ax2.set_ylabel(r"$|R|$")
ax2.set_ylim(0.0, 3.3)
ax2.set_title(r"(b) 刚性射线上的放大因子")
ax2.legend(fontsize=7.2, frameon=False, ncol=5, loc="upper center",
           bbox_to_anchor=(0.5, -0.27))
fig.tight_layout()
fig.subplots_adjust(bottom=0.30)
ps.save(fig, "figures/stability_geometry.pdf")

rows = ["theta,x,absR"]
for theta in (0.0, 0.25, 0.5, 0.75, 1.0):
    for xv in np.logspace(-2, 3, 200):
        rows.append(f"{theta},{xv:.6e},{abs(R_ray(theta, xv)):.6e}")
open("data/stability_ray.csv", "w").write("\n".join(rows) + "\n")


# --------------------------------------------------------------------------
# figure 2: exact phase diagram in the (theta, |z_D|) plane
# --------------------------------------------------------------------------
theta = np.linspace(0.0, 1.0, 401)
logz = np.linspace(-2.0, 3.0, 401)
T, LZ = np.meshgrid(theta, logz)
Z = 10.0 ** LZ
absR = np.abs((1.0 - T * Z) / (1.0 + (1.0 - T) * Z))
logR = np.log10(np.clip(absR, 1e-8, 1e3))

fig, ax = plt.subplots(figsize=(4.6, 3.2))
im = ax.imshow(logR, extent=[0.0, 1.0, -2.0, 3.0], origin="lower",
               aspect="auto", cmap="RdBu_r",
               norm=TwoSlopeNorm(vmin=-2.0, vcenter=0.0, vmax=1.0))
theta_b = np.linspace(0.5005, 1.0, 400)
ax.plot(theta_b, np.log10(2.0 / (2.0 * theta_b - 1.0)), color="k", lw=1.4)
ax.axvline(0.5, color="k", ls="--", lw=1.0)
ax.set_xlabel(r"分裂参数 $\theta$")
ax.set_ylabel(r"$\log_{10}|z_D|$")
ax.set_title(r"放大因子与 $|R|=1$ 边界")
ax.text(0.06, 2.35, "稳定", color="k", fontsize=10)
ax.text(0.58, 2.35, "不稳定", color="white", fontsize=10)
cb = fig.colorbar(im, ax=ax, pad=0.02)
cb.set_label(r"$\log_{10}|R|$")
fig.tight_layout()
ps.save(fig, "figures/stability_region.pdf")


# --------------------------------------------------------------------------
# figure 2b: continuous advection-diffusion stability region and the
# coupled-stiffness limit beta_inf(epsilon)
# --------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.4, 2.9))

theta_c = [0.0, 0.25, 0.5, 0.75, 1.0]
colors_c = [ps.C["blue"], ps.C["sky"], ps.C["green"], ps.C["orange"],
            ps.C["red"]]
rows = ["theta,d,mu_max"]
for th, col in zip(theta_c, colors_c):
    if th <= 0.5:
        d = np.logspace(-3.0, 3.0, 500)
    else:
        dmax = 2.0 / (2.0 * th - 1.0)
        d = np.logspace(-3.0, np.log10(dmax), 400)
    mu = np.sqrt(np.maximum(0.0, 2.0 * d + (1.0 - 2.0 * th) * d**2))
    ax1.loglog(d, mu, color=col, label=rf"$\theta={th:g}$")
    if th > 0.5:
        ax1.plot([d[-1]], [1.0e-3], "v", color=col, ms=4.0, clip_on=False)
    for dv, mv in zip(d[::25], mu[::25]):
        rows.append(f"{th},{dv:.6e},{mv:.6e}")

ax1.set_xlabel(r"$d=\nu k^2\Delta t$")
ax1.set_ylabel(r"$\mu_{\max}=ak\Delta t$")
ax1.set_title(r"(a) 联合稳定域（曲线下方稳定）", fontsize=9.5)
ax1.set_xlim(1e-3, 1e3)
ax1.set_ylim(1e-3, 1e3)
ax1.legend(fontsize=7.2, frameon=False, ncol=2, loc="lower right")
ax1.grid(True, which="both", alpha=0.18, lw=0.5)

eps = np.logspace(-2.0, 2.0, 500)
ax2.loglog(eps, 1.0 / eps, color=ps.C["black"], lw=1.6)
ax2.axvline(1.0, color=ps.C["grey"], ls="--", lw=0.9)
ax2.fill_betweenx([1e-2, 1e2], 1.0, 1e2, color=ps.C["green"], alpha=0.10)
ax2.text(1.6, 2.0, "稳定\n" r"$|\epsilon|\geq1$",
         color=ps.C["green"], fontsize=8.5, ha="left")
ax2.text(0.22, 2.0, "不稳定", color=ps.C["red"], fontsize=8.5, ha="left")
ax2.set_xlabel(r"$\epsilon=z_I/z_E$")
ax2.set_ylabel(r"$|\beta_\infty(\epsilon)|$")
ax2.set_title(r"(b) 刚性极限放大因子", fontsize=9.5)
ax2.set_xlim(1e-2, 1e2)
ax2.set_ylim(1e-2, 1e2)
ax2.grid(True, which="both", alpha=0.18, lw=0.5)

fig.tight_layout()
ps.save(fig, "figures/stability_coupled.pdf")
open("data/stability_coupled.csv", "w").write("\n".join(rows) + "\n")


# --------------------------------------------------------------------------
# figure 3: discrete symbol at a fixed CFL
# --------------------------------------------------------------------------
g = Grid(0.0, 1.0, 200)
nu = 1.0
dt = 0.4 * g.dx
xi = np.linspace(0.0, np.pi, 2001)
fig, ax = plt.subplots(figsize=(5.0, 3.0))
for theta, col in [(0.0, ps.C["blue"]), (0.25, ps.C["sky"]),
                   (0.5, ps.C["green"]), (0.6, ps.C["orange"]),
                   (0.75, ps.C["red"]), (1.0, ps.C["purple"])]:
    vals = np.abs(amplification(xi, dt, nu, theta, 1.0, g.dx))
    ax.plot(xi / np.pi, vals, color=col, label=rf"$\theta={theta:g}$")
ax.axhline(1.0, color=ps.C["black"], lw=0.9, ls="--")
ax.set_xlabel(r"无量纲波数 $\xi/\pi$")
ax.set_ylabel(r"$|R(\xi)|$")
ax.set_title(r"离散放大因子（$\mathrm{CFL}=0.4$，$\nu\Delta t/\Delta x^2=80$）")
ax.set_ylim(0.0, 3.5)
ax.set_yticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
ax.legend(fontsize=7.2, ncol=6, frameon=False, loc="upper center",
          bbox_to_anchor=(0.5, -0.24))
fig.tight_layout()
fig.subplots_adjust(bottom=0.27)
ps.save(fig, "figures/stability_discrete.pdf")

print("stability analysis done")
