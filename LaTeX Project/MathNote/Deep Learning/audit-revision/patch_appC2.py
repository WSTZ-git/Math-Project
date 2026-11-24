#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Second rigor patch for appendix C: correct the active-case multiplier sign and remove meta."""
from pathlib import Path

P = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/appendix-C.tex')

REPL = [
("""  \\item 激活情形：$g(\\bm{x}^{*})=0$，此时存在 $\\lambda>0$ 使 $\\nabla f(\\bm{x}^{*})=-\\lambda\\nabla g(\\bm{x}^{*})$。""",
 """  \\item 激活情形：$g(\\bm{x}^{*})=0$，此时存在 $\\lambda\\geqslant0$ 使 $\\nabla f(\\bm{x}^{*})=-\\lambda\\nabla g(\\bm{x}^{*})$，且 $\\lambda g(\\bm{x}^{*})=0$。"""),

("""原书论证如下：在前一种情况下，函数 $g(\\bm{x})$ 不起作用，因此驻点条件是 $\\nabla f(\\bm{x})=\\bm{0}$，这对应于 $\\lambda=0$ 的 Lagrange 函数的驻点；在后一种情况下，驻点位于边界上，类似于前面讨论的等式约束，对应于 $\\lambda\\neq0$ 的 Lagrange 函数的驻点。可见 Lagrange 乘子的符号是关键，因为只有当 $f(\\bm{x})$ 的梯度远离 $g(\\bm{x})>0$ 的区域时，函数 $f(\\bm{x})$ 才会达到最大值。因此，当 $\\lambda>0$ 时，有 $\\nabla f(\\bm{x}^{*})=-\\lambda\\nabla g(\\bm{x}^{*})$。

补全符号论证。非激活情形是区域内部的驻点，无需约束，故 $\\nabla f(\\bm{x}^{*})=\\bm{0}$。""",
 """非激活情形是区域内部的驻点，无需约束，故 $\\nabla f(\\bm{x}^{*})=\\bm{0}$，取 $\\lambda=0$ 即满足 $\\nabla f(\\bm{x}^{*})+\\lambda\\nabla g(\\bm{x}^{*})=\\bm{0}$ 与 $\\lambda g(\\bm{x}^{*})=0$。"""),

("""于是 $\\nabla f(\\bm{x}^{*})$ 在所有使 $\\nabla g(\\bm{x}^{*})^{\\mathsf{T}}\\bm{d}>0$ 的方向上取非正值，这迫使 $\\nabla f(\\bm{x}^{*})$ 与 $\\nabla g(\\bm{x}^{*})$ 反向共线，即存在 $\\lambda\\geqslant0$ 使 $\\nabla f(\\bm{x}^{*})=-\\lambda\\nabla g(\\bm{x}^{*})$；再由 $g(\\bm{x}^{*})=0$ 与\\cref{proposition:appC-梯度正交}知 $\\nabla f(\\bm{x}^{*})\\neq\\bm{0}$，故 $\\lambda>0$。""",
 """于是 $\\nabla f(\\bm{x}^{*})$ 在所有使 $\\nabla g(\\bm{x}^{*})^{\\mathsf{T}}\\bm{d}>0$ 的方向上取非正值，这迫使 $\\nabla f(\\bm{x}^{*})$ 与 $\\nabla g(\\bm{x}^{*})$ 反向共线，即存在 $\\lambda\\geqslant0$ 使 $\\nabla f(\\bm{x}^{*})=-\\lambda\\nabla g(\\bm{x}^{*})$；又 $g(\\bm{x}^{*})=0$，故 $\\lambda g(\\bm{x}^{*})=0$。"""),

("""两种情形的分界是“约束是否被触及”，而 $\\lambda$ 的符号则记录“约束把最优点往哪边推”：$\\lambda>0$ 表示目标函数的上升方向被约束挡住。""",
 """两种情形的分界是“约束是否被触及”，而 $\\lambda$ 的符号则记录“约束把最优点往哪边推”：$\\lambda>0$ 表示目标函数的上升方向被约束挡住；$\\lambda=0$ 时约束虽被触及，但对一阶条件没有贡献。"""),
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
