#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rigor patch for appendix C (Lagrange multipliers / KKT)."""
from pathlib import Path

P = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/appendix-C.tex')

REPL = [
("""\\begin{definition}[约束曲面]\\label{definition:appC-约束曲面}
约束方程 $g(\\bm{x})=0$ 在 $\\bm{x}$ 空间中表示的那个 $(D-1)$ 维曲面，称为\\textbf{约束曲面}；当 $D=2$ 时它就是一条约束曲线。
\\end{definition}""",
"""\\begin{definition}[约束曲面]\\label{definition:appC-约束曲面}
设 $D\\geqslant2$，$U\\subseteq\\mathbb{R}^{D}$ 为非空开集，$g:U\\to\\mathbb{R}$ 为 $C^{1}$ 函数，$\\bm{x}_{0}\\in U$ 满足 $g(\\bm{x}_{0})=0$ 且 $\\nabla g(\\bm{x}_{0})\\neq\\bm{0}$。由隐函数定理，存在 $\\bm{x}_{0}$ 的开邻域 $V\\subseteq U$，使集合
\\begin{align*}
  S=\\{\\bm{x}\\in V:g(\\bm{x})=0\\}
\\end{align*}
是 $\\mathbb{R}^{D}$ 中的 $(D-1)$ 维 $C^{1}$ 子流形；称 $S$ 为约束方程 $g(\\bm{x})=0$ 在 $\\bm{x}_{0}$ 处的\\textbf{约束曲面}，当 $D=2$ 时称为约束曲线。若 $\\nabla g(\\bm{x}_{0})=\\bm{0}$，则 $S$ 可能退化（例如 $g(\\bm{x})=\\|\\bm{x}\\|^{2}$ 在 $\\bm{x}_{0}=\\bm{0}$ 处只给出一个点），此时不称其为本定义意义下的约束曲面。
\\end{definition}"""),

("""\\begin{definition}[Lagrange 乘子]\\label{definition:appC-乘子}
在\\eqref{align:appC-平行条件}中出现的参数 $\\lambda$ 称为\\textbf{Lagrange 乘子}（Lagrange multiplier），它度量约束对目标函数驻点的影响强度。
\\end{definition}""",
"""\\begin{definition}[Lagrange 乘子]\\label{definition:appC-乘子}
设 $U\\subseteq\\mathbb{R}^{D}$ 为非空开集，$f,g\\in C^{1}(U)$，$\\bm{x}^{*}\\in U$ 满足 $g(\\bm{x}^{*})=0$、$\\nabla g(\\bm{x}^{*})\\neq\\bm{0}$，且 $\\bm{x}^{*}$ 是 $f$ 在约束曲面 $S=\\{g=0\\}$ 上的局部极值点。若实数 $\\lambda$ 满足
\\begin{align*}
  \\nabla f(\\bm{x}^{*})+\\lambda\\nabla g(\\bm{x}^{*})=\\bm{0},
\\end{align*}
则称 $\\lambda$ 为约束 $g(\\bm{x})=0$ 在 $\\bm{x}^{*}$ 处的\\textbf{Lagrange 乘子}（Lagrange multiplier）。$\\lambda$ 可正可负，也可为零；当 $\\nabla f(\\bm{x}^{*})\\neq\\bm{0}$ 时 $\\lambda\\neq0$。
\\end{definition}"""),

("""\\begin{definition}[Lagrange 函数]\\label{definition:appC-乘子函数}
\\begin{align}
  L(\\bm{x},\\lambda)=f(\\bm{x})+\\lambda g(\\bm{x})
  \\label{align:appC-Lagrange函数}
\\end{align}
称为与约束问题\\eqref{align:appC-约束条件}对应的\\textbf{Lagrange 函数}（Lagrangian）。
\\end{definition}""",
"""\\begin{definition}[Lagrange 函数]\\label{definition:appC-乘子函数}
设 $U\\subseteq\\mathbb{R}^{D}$ 为非空开集，$f,g\\in C^{1}(U)$。定义函数 $L:U\\times\\mathbb{R}\\to\\mathbb{R}$ 为
\\begin{align}
  L(\\bm{x},\\lambda)=f(\\bm{x})+\\lambda g(\\bm{x}),
  \\label{align:appC-Lagrange函数}
\\end{align}
称 $L$ 为与约束问题\\eqref{align:appC-约束条件}对应的\\textbf{Lagrange 函数}（Lagrangian）；$\\bm{x}\\in U$ 与 $\\lambda\\in\\mathbb{R}$ 均为自变量。
\\end{definition}"""),

("""\\begin{definition}[等式约束与不等式约束]\\label{definition:appC-等式不等式约束}
形如 $g(\\bm{x})=0$ 的约束称为\\textbf{等式约束}（equality constraint）；形如 $g(\\bm{x})\\geqslant0$ 的约束称为\\textbf{不等式约束}（inequality constraint）。
\\end{definition}""",
"""\\begin{definition}[等式约束与不等式约束]\\label{definition:appC-等式不等式约束}
设 $D\\geqslant1$，$U\\subseteq\\mathbb{R}^{D}$ 为非空开集，$g:U\\to\\mathbb{R}$ 为函数。条件 $g(\\bm{x})=0$ 称为\\textbf{等式约束}（equality constraint），其可行集为 $\\{\\bm{x}\\in U:g(\\bm{x})=0\\}$；条件 $g(\\bm{x})\\geqslant0$ 称为\\textbf{不等式约束}（inequality constraint），其可行集为 $\\{\\bm{x}\\in U:g(\\bm{x})\\geqslant0\\}$。若同时有多个约束 $g_{i}(\\bm{x})=0$、$h_{j}(\\bm{x})\\geqslant0$，则可行集为它们的交集。
\\end{definition}"""),

("""\\begin{definition}[激活约束与非激活约束]\\label{definition:appC-激活约束}
如果驻点位于 $g(\\bm{x})>0$ 的区域内，则约束是\\textbf{非激活的}（inactive）；而如果驻点位于边界 $g(\\bm{x})=0$ 上，则约束是\\textbf{激活的}（active）。
\\end{definition}""",
"""\\begin{definition}[激活约束与非激活约束]\\label{definition:appC-激活约束}
设 $U\\subseteq\\mathbb{R}^{D}$ 为非空开集，$g:U\\to\\mathbb{R}$，$\\bm{x}^{*}\\in U$ 满足 $g(\\bm{x}^{*})\\geqslant0$。若 $g(\\bm{x}^{*})>0$，则称不等式约束 $g(\\bm{x})\\geqslant0$ 在 $\\bm{x}^{*}$ 处是\\textbf{非激活的}（inactive）；若 $g(\\bm{x}^{*})=0$，则称它在 $\\bm{x}^{*}$ 处是\\textbf{激活的}（active）。
\\end{definition}"""),

("""\\begin{theorem}[Karush-Kuhn-Tucker 条件]\\label{theorem:appC-KKT}
在约束 $g(\\bm{x})\\geqslant0$ 下最大化 $f(\\bm{x})$ 的问题，其驻点满足
\\begin{align}
  g(\\bm{x})&\\geqslant0
  \\label{align:appC-KKT1}\\\\
  \\lambda&\\geqslant0
  \\label{align:appC-KKT2}\\\\
  \\lambda g(\\bm{x})&=0
  \\label{align:appC-KKT3}
\\end{align}
并且 $\\nabla_{\\bm{x}}L(\\bm{x},\\lambda)=\\bm{0}$。我们称它们为\\textbf{Karush-Kuhn-Tucker}（KKT）条件（Karush, 1939; Kuhn and Tucker, 1951）。
\\end{theorem}""",
"""\\begin{theorem}[Karush-Kuhn-Tucker 条件]\\label{theorem:appC-KKT}
设 $U\\subseteq\\mathbb{R}^{D}$ 为非空开集，$f,g\\in C^{1}(U)$，$\\bm{x}^{*}\\in U$ 是 $f$ 在可行集 $\\mathcal{F}=\\{\\bm{x}\\in U:g(\\bm{x})\\geqslant0\\}$ 上的局部极大值点，且当 $g(\\bm{x}^{*})=0$ 时 $\\nabla g(\\bm{x}^{*})\\neq\\bm{0}$。则存在 $\\lambda\\geqslant0$，使得
\\begin{align}
  g(\\bm{x}^{*})&\\geqslant0,
  \\label{align:appC-KKT1}\\\\
  \\lambda&\\geqslant0,
  \\label{align:appC-KKT2}\\\\
  \\lambda g(\\bm{x}^{*})&=0,
  \\label{align:appC-KKT3}
\\end{align}
且 $\\nabla_{\\bm{x}}L(\\bm{x}^{*},\\lambda)=\\bm{0}$。称\\eqref{align:appC-KKT1}--\\eqref{align:appC-KKT3}与 $\\nabla_{\\bm{x}}L(\\bm{x}^{*},\\lambda)=\\bm{0}$ 为\\textbf{Karush-Kuhn-Tucker}（KKT）条件（Karush, 1939; Kuhn and Tucker, 1951）。它们只是局部极大值的必要条件，不是充分条件。
\\end{theorem}"""),

("""\\begin{proposition}[最小化情形的 KKT 条件]\\label{proposition:appC-最小化KKT}
若把\\cref{theorem:appC-KKT}中的“最大化 $f$”改为“最小化 $f$”，则相应的 Lagrange 函数改为 $L(\\bm{x},\\lambda)=f(\\bm{x})-\\lambda g(\\bm{x})$，其余三条条件\\eqref{align:appC-KKT1}--\\eqref{align:appC-KKT3}不变，仍要求 $\\lambda\\geqslant0$。
\\end{proposition}""",
"""\\begin{proposition}[最小化情形的 KKT 条件]\\label{proposition:appC-最小化KKT}
设 $U\\subseteq\\mathbb{R}^{D}$ 为非空开集，$f,g\\in C^{1}(U)$，$\\bm{x}^{*}\\in U$ 是 $f$ 在可行集 $\\mathcal{F}=\\{\\bm{x}\\in U:g(\\bm{x})\\geqslant0\\}$ 上的局部极小值点，且当 $g(\\bm{x}^{*})=0$ 时 $\\nabla g(\\bm{x}^{*})\\neq\\bm{0}$。则存在 $\\lambda\\geqslant0$，使得\\eqref{align:appC-KKT1}--\\eqref{align:appC-KKT3}成立，且
\\begin{align*}
  \\nabla f(\\bm{x}^{*})-\\lambda\\nabla g(\\bm{x}^{*})=\\bm{0}.
\\end{align*}
等价地，令 $L(\\bm{x},\\lambda)=f(\\bm{x})-\\lambda g(\\bm{x})$，则 $\\nabla_{\\bm{x}}L(\\bm{x}^{*},\\lambda)=\\bm{0}$。
\\end{proposition}"""),
]

def main():
    t = P.read_text(encoding='utf-8')
    for old, new in REPL:
        if old not in t:
            print('MISS', old[:60].replace('\n', ' '))
        t = t.replace(old, new)
    P.write_text(t, encoding='utf-8')
    print('written', P)

if __name__ == '__main__':
    main()
