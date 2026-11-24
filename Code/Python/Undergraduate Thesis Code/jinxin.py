r"""
jinxin.py
=========
Jin-Xin relaxation system for the inviscid Burgers equation

    u_t + v_x = 0,
    v_t + a^2 u_x = -(1/eps) (v - f(u)),      f(u) = u^2/2,

with the subcharacteristic condition a >= max|f'(u)|.  As eps -> 0 the
system relaxes to u_t + f(u)_x = 0.

Two IMEX-Euler source splittings are implemented:

  strategy A : the whole source is implicit at the new time,
               v^{n+1} = [v^n + dt L_v(w^n) + mu f(u^{n+1})]/(1+mu);

  strategy B : only the linear stiff part -v/eps is implicit, while the
               nonlinear part f(u)/eps is evaluated explicitly,
               v^{n+1} = [v^n + dt L_v(w^n) + mu f(u^n)]/(1+mu).

Here mu = dt/eps and L is the Rusanov-discretised transport operator.

The module also contains the 2x2 Fourier amplification matrices used in
the linear stability analysis of the two splittings.
"""

from __future__ import annotations

import numpy as np


def f_burgers(u):
    return 0.5 * np.asarray(u) ** 2


def exact_riemann(x, t, uL=1.0, uR=0.0):
    """Entropy solution of the inviscid Riemann problem (uL > uR)."""
    s = 0.5 * (uL + uR)
    return np.where(np.asarray(x) < s * t, uL, uR)


def transport_rhs(u, v, dx, a, uL, uR):
    """Rusanov semi-discrete transport operator for (u, v)."""
    ue = np.concatenate(([uL], u, [uR]))
    ve = np.concatenate(([f_burgers(uL)], v, [f_burgers(uR)]))
    # interface fluxes, N+1 entries
    flux_u = 0.5 * (ve[:-1] + ve[1:]) - 0.5 * a * (ue[1:] - ue[:-1])
    flux_v = 0.5 * a * a * (ue[:-1] + ue[1:]) - 0.5 * a * (ve[1:] - ve[:-1])
    du = -(flux_u[1:] - flux_u[:-1]) / dx
    dv = -(flux_v[1:] - flux_v[:-1]) / dx
    return du, dv


def solve_jinxin(u0, v0, t_end, dt, eps, a, grid, strategy="A",
                 uL=1.0, uR=0.0, blowup=1.0e3):
    """IMEX-Euler for the Jin-Xin system with source strategy A or B."""
    u = np.array(u0, dtype=float)
    v = np.array(v0, dtype=float)
    mu = dt / eps
    nsteps = int(np.ceil(t_end / dt - 1.0e-12))
    status = "ok"

    for _ in range(nsteps):
        du, dv = transport_rhs(u, v, grid.dx, a, uL, uR)
        u_new = u + dt * du
        if strategy == "A":
            v_new = (v + dt * dv + mu * f_burgers(u_new)) / (1.0 + mu)
        elif strategy == "B":
            v_new = (v + dt * dv + mu * f_burgers(u)) / (1.0 + mu)
        elif strategy == "C":  # fully explicit source, control only
            v_new = v + dt * dv + mu * (f_burgers(u) - v)
        else:
            raise ValueError("strategy must be 'A', 'B' or 'C'")
        u, v = u_new, v_new
        if (not np.all(np.isfinite(u))) or (not np.all(np.isfinite(v))) \
                or np.max(np.abs(u)) > blowup or np.max(np.abs(v)) > blowup:
            status = "blowup"
            break

    return {"u": u, "v": v, "status": status, "nsteps": nsteps, "t": nsteps * dt}


# --------------------------------------------------------------------------
# Fourier stability analysis
# --------------------------------------------------------------------------
def amplification_matrices(xi, cfl, mu, b=1.0, a=1.0):
    """Stiff-source IMEX amplification matrices for one Fourier mode.

    xi  : dimensionless wavenumber in [0, pi]
    cfl : a dt / dx
    mu  : dt / eps
    b   : frozen f'(u)
    """
    g = cfl * (1.0 - np.cos(xi))
    h = (cfl / a) * np.sin(xi)

    # strategy A: f(u^{n+1}) in the implicit source
    M_A = np.array([
        [1.0 - g, -1j * h],
        [(mu * b * (1.0 - g) - 1j * a * a * h) / (1.0 + mu),
         ((1.0 - g) - 1j * mu * b * h) / (1.0 + mu)],
    ])

    # strategy B: f(u^n) explicit
    M_B = np.array([
        [1.0 - g, -1j * h],
        [(-1j * a * a * h + mu * b) / (1.0 + mu), (1.0 - g) / (1.0 + mu)],
    ])
    return M_A, M_B


def spectral_radius(xi, cfl, mu, strategy="A", b=1.0, a=1.0):
    M_A, M_B = amplification_matrices(xi, cfl, mu, b, a)
    M = M_A if strategy == "A" else M_B
    return float(np.max(np.abs(np.linalg.eigvals(M))))


def max_spectral_radius(cfl, mu, strategy="A", b=1.0, a=1.0, nxi=2001):
    xi = np.linspace(0.0, np.pi, nxi)
    return max(spectral_radius(x, cfl, mu, strategy, b, a) for x in xi)


def critical_cfl_stiff(strategy="B", b=1.0, a=1.0, mu=1.0e12,
                       c_lo=0.05, c_hi=1.0):
    """Largest CFL with spectral radius <= 1 in the stiff limit."""
    lo, hi = c_lo, c_hi
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if max_spectral_radius(mid, mu, strategy, b, a, nxi=1201) <= 1.0 + 1e-10:
            lo = mid
        else:
            hi = mid
    return lo
