r"""
burgers_imex.py
===============
One-dimensional viscous Burgers equation

    u_t + (u^2/2)_x = nu u_xx,      x in [xmin, xmax],  t > 0,

discretised in space by a finite-volume method (Rusanov flux, optional
MUSCL/minmod reconstruction) and advanced in time by the parameterised
IMEX-Euler family

    dU/dt = C(U) + theta * nu * D U  +  (1-theta) * nu * D U,
             \_______ explicit _______/    \_____ implicit _____/

    [I - (1-theta) nu dt D] U^{n+1}
        = U^n + dt C(U^n) + theta nu dt D U^n.

The diffusion operator D is the standard three-point Laplacian; the
convective operator C uses the local Lax-Friedrichs (Rusanov) flux.
Dirichlet boundary conditions are imposed through ghost cells; periodic
boundary conditions are also supported.

The module is dependency-light: numpy + scipy.sparse (LU factorisation).
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import splu

# NumPy 2.0 renamed trapz to trapezoid; keep a fallback for older versions.
_trapezoid = getattr(np, "trapezoid", None)
if _trapezoid is None:  # pragma: no cover - only for NumPy < 2.0
    _trapezoid = np.trapz


# --------------------------------------------------------------------------
# grid and exact solution
# --------------------------------------------------------------------------
@dataclass
class Grid:
    xmin: float
    xmax: float
    N: int

    def __post_init__(self):
        self.dx = (self.xmax - self.xmin) / self.N
        self.x = self.xmin + (np.arange(self.N) + 0.5) * self.dx

    @property
    def edges(self):
        return np.linspace(self.xmin, self.xmax, self.N + 1)


def exact_viscous_shock(x, t, nu, uL=1.0, uR=0.0):
    """Exact travelling-wave solution of viscous Burgers (uL > uR).

    u(x,t) = uR + (uL-uR) / (1 + exp(A (x - s t) / (2 nu))),
    s = (uL+uR)/2,  A = uL-uR.
    """
    A = uL - uR
    s = 0.5 * (uL + uR)
    z = A * (np.asarray(x, dtype=float) - s * t) / (2.0 * nu)
    z = np.clip(z, -700.0, 700.0)
    return uR + A / (1.0 + np.exp(z))


# --------------------------------------------------------------------------
# numerical fluxes
# --------------------------------------------------------------------------
def minmod(a, b):
    """Minmod slope limiter."""
    return 0.5 * (np.sign(a) + np.sign(b)) * np.minimum(np.abs(a), np.abs(b))


def _interface_states(u, bcl, bcr, order, periodic):
    """Return (left, right) states at the N+1 cell interfaces.

    The MUSCL slopes are attached to the N physical cells.  At a periodic
    boundary the slope of the last (first) cell is used for the left (right)
    state of the wrap-around interface, so no interface is degraded to first
    order.  At a Dirichlet boundary the ghost value is not reconstructed.
    """
    if periodic:
        ue = np.concatenate(([u[-1]], u, [u[0]]))
    else:
        ue = np.concatenate(([bcl], u, [bcr]))  # ghosts at both ends
    if order == 1:
        return ue[:-1], ue[1:]
    du = np.diff(ue)
    slope = minmod(du[:-1], du[1:])  # one slope per physical cell
    if periodic:
        left_slope = np.concatenate(([slope[-1]], slope))
        right_slope = np.concatenate((slope, [slope[0]]))
    else:
        left_slope = np.concatenate(([0.0], slope))
        right_slope = np.concatenate((slope, [0.0]))
    left = ue[:-1] + 0.5 * left_slope
    right = ue[1:] - 0.5 * right_slope
    return left, right


def rhs_convective(u, grid, bcl=0.0, bcr=0.0, order=1, periodic=False):
    """Semi-discrete convective operator C(U), shape (N,)."""
    ul, ur = _interface_states(u, bcl, bcr, order, periodic)
    fl = 0.5 * ul * ul
    fr = 0.5 * ur * ur
    alpha = np.maximum(np.abs(ul), np.abs(ur))
    flux = 0.5 * (fl + fr) - 0.5 * alpha * (ur - ul)
    return -(flux[1:] - flux[:-1]) / grid.dx


def laplacian(u, grid, bcl=0.0, bcr=0.0, periodic=False):
    """Three-point Laplacian with ghost cells (Dirichlet or periodic)."""
    lap = np.empty_like(u)
    lap[1:-1] = (u[2:] - 2.0 * u[1:-1] + u[:-2]) / grid.dx**2
    if periodic:
        lap[0] = (u[1] - 2.0 * u[0] + u[-1]) / grid.dx**2
        lap[-1] = (u[0] - 2.0 * u[-1] + u[-2]) / grid.dx**2
    else:
        lap[0] = (u[1] - 2.0 * u[0] + bcl) / grid.dx**2
        lap[-1] = (bcr - 2.0 * u[-1] + u[-2]) / grid.dx**2
    return lap


# --------------------------------------------------------------------------
# parameterised IMEX-Euler solver
# --------------------------------------------------------------------------
def _implicit_operator(N, dx, nu, dt, theta, periodic):
    """Sparse matrix A = I - (1-theta) nu dt D."""
    c = (1.0 - theta) * nu * dt / dx**2
    if c == 0.0:
        return None
    main = np.full(N, 1.0 + 2.0 * c)
    off = np.full(N - 1, -c)
    A = diags([off, main, off], [-1, 0, 1], format="csc")
    if periodic:
        A = A + diags([np.array([-c]), np.array([-c])], [N - 1, -(N - 1)], format="csc")
    return A


def solve_burgers(u0, t_end, dt, nu, theta, grid, bcl=0.0, bcr=0.0,
                  order=1, record_every=0, blowup=1.0e3, periodic=False):
    """Advance the semi-discrete Burgers system with IMEX-Euler.

    Parameters
    ----------
    u0 : ndarray
        Initial cell averages.
    t_end : float
        Final time.
    dt : float
        Time step (kept constant).
    nu : float
        Viscosity.
    theta : float
        Splitting parameter in [0, 1].
    grid : Grid
    bcl, bcr : float
        Dirichlet boundary values (ignored if periodic=True).
    order : int
        1 = first-order Rusanov, 2 = MUSCL/minmod reconstruction.
    record_every : int
        If > 0, store the solution every this many steps.
    blowup : float
        Abort when max|u| exceeds this value (returns status='blowup').
    periodic : bool
        Periodic boundary conditions.

    Returns
    -------
    dict with keys u, t, nsteps, status, history, times
    """
    u = np.array(u0, dtype=float)
    nsteps = int(np.ceil(t_end / dt - 1.0e-12))
    A = _implicit_operator(grid.N, grid.dx, nu, dt, theta, periodic)
    lu = splu(A) if A is not None else None

    history = []
    times = []
    status = "ok"

    for n in range(nsteps):
        conv = rhs_convective(u, grid, bcl, bcr, order=order, periodic=periodic)
        lap = laplacian(u, grid, bcl, bcr, periodic=periodic)
        rhs = u + dt * (conv + theta * nu * lap)

        if lu is not None:
            c = (1.0 - theta) * nu * dt / grid.dx**2
            if not periodic:
                rhs[0] += c * bcl
                rhs[-1] += c * bcr
            u = lu.solve(rhs)
        else:
            u = rhs

        if not np.all(np.isfinite(u)) or np.max(np.abs(u)) > blowup:
            status = "blowup"
            break

        if record_every and (n % record_every == 0):
            history.append(u.copy())
            times.append((n + 1) * dt)

    if record_every and (not times or times[-1] < nsteps * dt - 1e-12):
        history.append(u.copy())
        times.append(nsteps * dt)

    return {
        "u": u,
        "t": nsteps * dt,
        "nsteps": nsteps,
        "status": status,
        "history": history,
        "times": times,
    }


def is_stable_run(u0, t_end, dt, nu, theta, grid, bcl=0.0, bcr=0.0,
                  order=1, max_abs=2.0, periodic=False):
    """Heuristic stability test: run and check that the solution stays bounded."""
    res = solve_burgers(u0, t_end, dt, nu, theta, grid, bcl, bcr,
                        order=order, blowup=max_abs, periodic=periodic)
    if res["status"] != "ok":
        return False
    return np.max(np.abs(res["u"])) <= max_abs


# --------------------------------------------------------------------------
# diagnostics
# --------------------------------------------------------------------------
def _level_crossing(x, u, level):
    """x-position where the (decreasing) profile crosses `level`."""
    i = int(np.argmin(np.abs(u - level)))
    for j in (i - 1, i):
        if 0 <= j < len(u) - 1:
            a, b = u[j], u[j + 1]
            if (a - level) * (b - level) <= 0.0 and a != b:
                w = (level - a) / (b - a)
                return x[j] + w * (x[j + 1] - x[j])
    return x[i]


def shock_metrics(x, u, t, nu, uL=1.0, uR=0.0):
    """L1 error, shock-position error and 10-90% transition thickness."""
    ue = exact_viscous_shock(x, t, nu, uL, uR)
    l1 = _trapezoid(np.abs(u - ue), x) / (x[-1] - x[0])
    linf = np.max(np.abs(u - ue))
    xs_num = _level_crossing(x, u, 0.5 * (uL + uR))
    xs_ex = 0.5 * (uL + uR) * t
    x90 = _level_crossing(x, u, uR + 0.9 * (uL - uR))
    x10 = _level_crossing(x, u, uR + 0.1 * (uL - uR))
    width = x10 - x90
    width_ex = 4.0 * nu * np.log(9.0) / (uL - uR)
    return {
        "l1": float(l1),
        "linf": float(linf),
        "shock_pos": float(xs_num),
        "shock_pos_error": float(xs_num - xs_ex),
        "width": float(width),
        "width_exact": float(width_ex),
        "width_error": float(width - width_ex),
    }


# --------------------------------------------------------------------------
# discrete Fourier symbol of the first-order Rusanov scheme
# --------------------------------------------------------------------------
def rusanov_symbol(xi, a, dx):
    """Fourier symbol of the linearised first-order Rusanov operator.

    lambda_C = -i a sin(xi)/dx - |a| (1-cos(xi))/dx
    lambda_D = -2 (1-cos(xi))/dx^2
    """
    lam_c = -1j * a * np.sin(xi) / dx - abs(a) * (1.0 - np.cos(xi)) / dx
    lam_d = -2.0 * (1.0 - np.cos(xi)) / dx**2
    return lam_c, lam_d


def amplification(xi, dt, nu, theta, a, dx):
    """Amplification factor R(z_E, z_I) for a Fourier mode."""
    lam_c, lam_d = rusanov_symbol(xi, a, dx)
    z_e = dt * (lam_c + theta * nu * lam_d)
    z_i = dt * (1.0 - theta) * nu * lam_d
    return (1.0 + z_e) / (1.0 - z_i)


def max_stable_dt_symbol(dx, nu, theta, a=1.0, nxi=4001,
                         dt_hi=None, tol=1e-12):
    """Largest dt with max_xi |R(xi)| <= 1 for the linearised scheme."""
    xi = np.linspace(0.0, np.pi, nxi)

    def ok(dt):
        return np.max(np.abs(amplification(xi, dt, nu, theta, a, dx))) <= 1.0 + tol

    lo = 1e-14
    hi = dt_hi if dt_hi is not None else 4.0 * dx
    while ok(hi) and hi < 1e8:
        hi *= 2.0
    if not ok(lo):
        return 0.0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if ok(mid):
            lo = mid
        else:
            hi = mid
        if hi - lo <= 1e-14 * max(1.0, hi):
            break
    return lo
