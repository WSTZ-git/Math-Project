#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rigor patch for appendix B (variational calculus)."""
from pathlib import Path

P = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/appendix-B.tex')

REPL = [
("""\\begin{definition}[泛函]\\label{definition:appB-泛函}
设某个函数类中的每个函数 $y(x)$ 都按确定的规则对应一个数 $F$。这样的对应关系称为定义在该函数类上的\\textbf{泛函}（functional），记作 $F[y]$：它接收函数 $y(x)$，并返回输出值 $F$。
\\end{definition}""",
"""\\begin{definition}[泛函]\\label{definition:appB-泛函}
设 $I\\subseteq\\mathbb{R}$ 为区间，$\\mathcal{Y}$ 为定义在 $I$ 上、取值于 $\\mathbb{R}$ 的函数构成的非空函数类，$F:\\mathcal{Y}\\to\\mathbb{R}$ 为映射。若对每个 $y\\in\\mathcal{Y}$，$F$ 按确定的规则给出唯一的实数 $F[y]$，则称 $F$ 为定义在 $\\mathcal{Y}$ 上的\\textbf{泛函}（functional），记作 $F[y]$；$\\mathcal{Y}$ 称为 $F$ 的\\textbf{容许函数类}，$F[y]$ 称为 $F$ 在 $y$ 处的值。泛函的输入是函数 $y$，输出是实数。
\\end{definition}"""),

("""\\begin{definition}[变分法]\\label{definition:appB-变分法}
在给定的函数类中寻找使泛函 $F[y]$ 取极大值或极小值的函数 $y(x)$，这类问题称为变分问题；研究变分问题、并给出其解所满足的微分方程的数学分支，称为\\textbf{变分法}（calculus of variations）。
\\end{definition}""",
"""\\begin{definition}[变分法]\\label{definition:appB-变分法}
设 $I=[a,b]\\subseteq\\mathbb{R}$，$\\mathcal{Y}$ 为 $I$ 上满足给定边界条件与正则性条件的非空函数类，$F:\\mathcal{Y}\\to\\mathbb{R}$ 为泛函。若 $y_{*}\\in\\mathcal{Y}$ 满足 $F[y_{*}]\\geqslant F[y]$（或 $F[y_{*}]\\leqslant F[y]$）对一切 $y\\in\\mathcal{Y}$ 成立，则称 $y_{*}$ 为 $F$ 在 $\\mathcal{Y}$ 上的极大点（或极小点）；求此类 $y_{*}$ 的问题称为\\textbf{变分问题}。研究变分问题、并给出其驻点所满足的微分方程的数学分支，称为\\textbf{变分法}（calculus of variations）。
\\end{definition}"""),

("""\\begin{definition}[泛函导数]\\label{definition:appB-泛函导数}
\\begin{align}
  F[y(x)+\\varepsilon\\eta(x)]=F[y(x)]+\\varepsilon\\int\\frac{\\delta F}{\\delta y(x)}\\eta(x)\\,\\mathrm{d}x+O(\\varepsilon^{2})
  \\label{align:appB-泛函导数定义}
\\end{align}
\\end{definition}""",
"""\\begin{definition}[泛函导数]\\label{definition:appB-泛函导数}
设 $I=[a,b]\\subseteq\\mathbb{R}$，$\\mathcal{Y}$ 为 $I$ 上满足给定边界条件的函数类，$F:\\mathcal{Y}\\to\\mathbb{R}$ 为泛函，$y\\in\\mathcal{Y}$。若存在函数 $\\frac{\\delta F}{\\delta y}:I\\to\\mathbb{R}$，使得对每个 $\\eta\\in C_{c}^{\\infty}((a,b))$，当 $|\\varepsilon|$ 充分小时 $y+\\varepsilon\\eta\\in\\mathcal{Y}$，且
\\begin{align}
  F[y+\\varepsilon\\eta]=F[y]+\\varepsilon\\int_{a}^{b}\\frac{\\delta F}{\\delta y}(x)\\,\\eta(x)\\,\\mathrm{d}x+O(\\varepsilon^{2})
  \\label{align:appB-泛函导数定义}
\\end{align}
其中 $O(\\varepsilon^{2})$ 的常数只依赖于 $\\eta$ 的紧支撑集与有限阶导数，则称 $\\frac{\\delta F}{\\delta y}$ 为 $F$ 在 $y$ 处的\\textbf{泛函导数}（functional derivative）。
\\end{definition}"""),

("""\\begin{proposition}[变分法的基本引理]\\label{proposition:appB-基本引理}
若\\eqref{align:appB-平稳条件}对积分区间内任意（足够光滑且在边界处为零的）函数 $\\eta(x)$ 都成立，则对该区间内的每个 $x$ 都有 $\\delta F/\\delta y(x)=0$。
\\end{proposition}

\\begin{proof}
为了说明这一点，选择一个扰动 $\\eta(x)$，其在除了点 $\\hat{x}$ 的邻域之外的任意位置都为零。在这种情况下，泛函的导数在 $x=\\hat{x}$ 处必须为零。但是，由于对任意的 $\\hat{x}$ 都必须满足此条件，因此对于任意的 $x$，泛函的导数都必须消除。
\\end{proof}""",
"""\\begin{proposition}[变分法的基本引理]\\label{proposition:appB-基本引理}
设 $I=[a,b]\\subseteq\\mathbb{R}$，$g:I\\to\\mathbb{R}$ 连续。若
\\begin{align}
  \\int_{a}^{b}g(x)\\eta(x)\\,\\mathrm{d}x=0
  \\label{align:appB-基本引理条件}
\\end{align}
对一切 $\\eta\\in C_{c}^{\\infty}((a,b))$ 成立，则 $g(x)=0$ 对一切 $x\\in I$ 成立。
\\end{proposition}

\\begin{proof}
反设存在 $x_{0}\\in(a,b)$ 使 $g(x_{0})\\neq0$。由 $g$ 连续，存在 $\\delta>0$ 使 $[x_{0}-\\delta,x_{0}+\\delta]\\subset(a,b)$ 且 $g$ 在该区间上不变号、$|g|\\geqslant|g(x_{0})|/2$。取非负的 $\\eta\\in C_{c}^{\\infty}((a,b))$，满足 $\\eta(x)>0$ 在 $(x_{0}-\\delta,x_{0}+\\delta)$ 内、$\\eta$ 在该区间外为零。则 $g\\eta$ 在 $(x_{0}-\\delta,x_{0}+\\delta)$ 内不变号且不恒为零，故 $\\int_{a}^{b}g\\eta\\,\\mathrm{d}x\\neq0$，与\\eqref{align:appB-基本引理条件}矛盾。端点 $x_{0}=a,b$ 由 $g$ 的连续性取极限得到。故 $g\\equiv0$。
\\end{proof}"""),

("""\\begin{definition}[积分型泛函]\\label{definition:appB-积分型泛函}
\\begin{align}
  F[y]=\\int G(y(x),y'(x),x)\\,\\mathrm{d}x
  \\label{align:appB-积分型泛函}
\\end{align}
其中，假设 $y(x)$ 的值在积分的边界处（可能在无穷大处）为定值。
\\end{definition}""",
"""\\begin{definition}[积分型泛函]\\label{definition:appB-积分型泛函}
设 $I=[a,b]\\subseteq\\mathbb{R}$，$G:\\mathbb{R}\\times\\mathbb{R}\\times I\\to\\mathbb{R}$ 为 $C^{2}$ 函数，$y\\in C^{2}(I)$，且 $y(a)=y_{a}$、$y(b)=y_{b}$ 为给定常数。称
\\begin{align}
  F[y]=\\int_{a}^{b}G\\bigl(y(x),y'(x),x\\bigr)\\,\\mathrm{d}x
  \\label{align:appB-积分型泛函}
\\end{align}
为定义在固定端点函数类 $\\mathcal{Y}=\\{y\\in C^{2}(I):y(a)=y_{a},\\ y(b)=y_{b}\\}$ 上的\\textbf{积分型泛函}。被积函数 $G$ 只含 $y$、$y'$ 与 $x$，不含 $y''$ 及更高阶导数。
\\end{definition}"""),

("""\\begin{theorem}[Euler-Lagrange 方程]\\label{theorem:appB-euler-lagrange}
设 $y(x)$ 使\\eqref{align:appB-积分型泛函}中的泛函在端点固定的函数类中取驻点，即\\eqref{align:appB-平稳条件}对任意在边界处为零的 $\\eta(x)$ 成立，则 $y$ 满足
\\begin{align}
  \\frac{\\partial G}{\\partial y}-\\frac{\\mathrm{d}}{\\mathrm{d}x}\\Bigl(\\frac{\\partial G}{\\partial y'}\\Bigr)=0
  \\label{align:appB-euler-lagrange}
\\end{align}
\\end{theorem}""",
"""\\begin{theorem}[Euler-Lagrange 方程]\\label{theorem:appB-euler-lagrange}
设 $I=[a,b]$，$G\\in C^{2}(\\mathbb{R}\\times\\mathbb{R}\\times I)$，$y\\in C^{2}(I)$ 且 $y(a),y(b)$ 固定。若 $y$ 是\\eqref{align:appB-积分型泛函}中泛函 $F$ 在固定端点函数类中的驻点，即对一切 $\\eta\\in C_{c}^{\\infty}((a,b))$ 有
\\begin{align}
  \\frac{\\mathrm{d}}{\\mathrm{d}\\varepsilon}F[y+\\varepsilon\\eta]\\Big|_{\\varepsilon=0}=0,
  \\label{align:appB-驻点条件}
\\end{align}
则 $y$ 在 $I$ 上满足
\\begin{align}
  \\frac{\\partial G}{\\partial y}\\bigl(y(x),y'(x),x\\bigr)-\\frac{\\mathrm{d}}{\\mathrm{d}x}\\Bigl(\\frac{\\partial G}{\\partial y'}\\bigl(y(x),y'(x),x\\bigr)\\Bigr)=0.
  \\label{align:appB-euler-lagrange}
\\end{align}
\\end{theorem}"""),

("""\\begin{proposition}[不含导数的泛函的驻点条件]\\label{proposition:appB-不含导数}
若\\eqref{align:appB-积分型泛函}中的 $G$ 不依赖于 $y'$，即 $G=G(y,x)$，则变分问题的驻点由逐点条件
\\begin{align*}
  \\frac{\\partial G}{\\partial y(x)}=0
\\end{align*}
给出，其中 $x$ 取遍积分区间内的所有值。
\\end{proposition}""",
"""\\begin{proposition}[不含导数的泛函的驻点条件]\\label{proposition:appB-不含导数}
设 $I=[a,b]$，$G\\in C^{1}(\\mathbb{R}\\times I)$ 不依赖于 $y'$，$F[y]=\\int_{a}^{b}G(y(x),x)\\,\\mathrm{d}x$，$y\\in C^{1}(I)$ 且端点固定。若 $y$ 是 $F$ 的驻点，则
\\begin{align*}
  \\frac{\\partial G}{\\partial y}\\bigl(y(x),x\\bigr)=0
\\end{align*}
对一切 $x\\in I$ 成立。
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
