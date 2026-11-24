#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove the second duplicate label in Chapter-06/section-04.tex."""
from pathlib import Path

p = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/Chapter-06/section-04.tex')
t = p.read_text(encoding='utf-8')
needle = '\\label{align:ch06-Bernoulli}'
first = t.find(needle)
second = t.find(needle, first + 1)
if second == -1:
    print('no duplicate found')
else:
    t = t[:second] + t[second + len(needle):]
    p.write_text(t, encoding='utf-8')
    print('removed second duplicate label')
