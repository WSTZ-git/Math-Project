#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move the explanatory example out of appendix C's definition body (robust)."""
from pathlib import Path

p = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/appendix-C.tex')
t = p.read_text(encoding='utf-8')
needle = '（例如 $g(\\bm{x})=\\|\\bm{x}\\|^{2}$ 在 $\\bm{x}_{0}=\\bm{0}$ 处只给出一个点）'
print('needle count', t.count(needle))
if needle in t:
    t = t.replace(needle, '', 1)
anchor = '本附录后面所有几何论证都默认 $\\nabla g\\neq\\bm{0}$，\\cref{proposition:appC-梯度正交}的证明中也显式用到这一点。'
print('anchor count', t.count(anchor))
extra = '例如 $g(\\bm{x})=\\|\\bm{x}\\|^{2}$ 在 $\\bm{x}_{0}=\\bm{0}$ 处只给出一个点，就是退化情形。'
if anchor in t and extra not in t:
    t = t.replace(anchor, anchor + extra, 1)
p.write_text(t, encoding='utf-8')
print('patched')
