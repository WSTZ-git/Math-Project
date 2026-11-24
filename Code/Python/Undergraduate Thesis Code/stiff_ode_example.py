#!/usr/bin/env python3
"""Small stiff ODE example for Chapter 2 (numbers only)."""
import numpy as np

lam = 1000.0
t_end = 1.0


def f(t, y):
    return -lam * (y - np.cos(t)) - np.sin(t)


def explicit_euler(dt):
    n = int(np.ceil(t_end / dt))
    y, t = 1.0, 0.0
    mx = 0.0
    for _ in range(n):
        y = y + dt * f(t, y)
        t += dt
        mx = max(mx, abs(y - np.cos(t)))
        if not np.isfinite(y) or abs(y) > 1e6:
            return np.inf
    return mx


def implicit_euler(dt):
    n = int(np.ceil(t_end / dt))
    y, t = 1.0, 0.0
    mx = 0.0
    for _ in range(n):
        y = (y + dt * (lam * np.cos(t) - np.sin(t))) / (1.0 + lam * dt)
        t += dt
        mx = max(mx, abs(y - np.cos(t)))
    return mx


print("explicit Euler")
for dt in (0.001, 0.002, 0.0021):
    print(f"  dt={dt}: max error = {explicit_euler(dt):.3e}")
print("implicit Euler")
for dt in (0.01, 0.05, 0.1):
    print(f"  dt={dt}: max error = {implicit_euler(dt):.3e}")
