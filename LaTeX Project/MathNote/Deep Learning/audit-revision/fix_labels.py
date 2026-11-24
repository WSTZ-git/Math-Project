#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix duplicate/missing equation labels introduced during the rigor rewrite."""
from pathlib import Path

ROOT = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning')


def fix(path, old, new):
    p = ROOT / path
    t = p.read_text(encoding='utf-8')
    if t.count(old) == 0:
        print('MISS', path, old[:60].replace('\n', ' '))
        return
    t = t.replace(old, new, 1)
    p.write_text(t, encoding='utf-8')
    print('fixed', path)


# 1. Chapter 6: remove the second (duplicate) label inside the definition;
#    the earlier display already owns the label.
fix('contents/Chapter-06/section-01.tex',
    """\\begin{align}
\\phi_n(\\boldsymbol{x})=\\exp\\!\\left(-\\frac{\\|\\boldsymbol{x}-\\boldsymbol{x}_n\\|^{2}}{s^{2}}\\right),
\\label{align:ch06-径向基函数}
\\end{align}""",
    """\\begin{align}
\\phi_n(\\boldsymbol{x})=\\exp\\!\\left(-\\frac{\\|\\boldsymbol{x}-\\boldsymbol{x}_n\\|^{2}}{s^{2}}\\right).
\\end{align}""")

fix('contents/Chapter-06/section-03.tex',
    """\\begin{align}
\\boldsymbol{z}^{(l)}=h^{(l)}\\!\\left(\\boldsymbol{W}^{(l)}\\boldsymbol{z}^{(l-1)}\\right),
\\label{align:ch06-深层递推}
\\end{align}""",
    """\\begin{align}
\\boldsymbol{z}^{(l)}=h^{(l)}\\!\\left(\\boldsymbol{W}^{(l)}\\boldsymbol{z}^{(l-1)}\\right).
\\end{align}""")

# 2. Chapter 10: restore the missing DeepDream update equation with its label.
fix('contents/Chapter-10/section-03.tex',
    """从图像
$I_0\\in\\mathbb{R}^{H\\times W\\times C}$ 出发，按
\\eqref{align:ch10-DeepDream更新}迭代
$I_{\\tau+1}=I_{\\tau}+\\eta\\nabla_IF(I_{\\tau})$，$\\tau=0,1,2,\\dots$，其中 $\\eta>0$ 为
步长，并在每一步之后施加空间平滑算子、再把像素值截断到图像的合法取值区间。""",
    """从图像
$I_0\\in\\mathbb{R}^{H\\times W\\times C}$ 出发，按
\\begin{align}
I_{\\tau+1}=I_{\\tau}+\\eta\\nabla_IF(I_{\\tau}),
\\label{align:ch10-DeepDream更新}
\\end{align}
迭代，$\\tau=0,1,2,\\dots$，其中 $\\eta>0$ 为步长，并在每一步之后施加空间平滑算子、
再把像素值截断到图像的合法取值区间。""")
