from pathlib import Path
p = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/Chapter-19/section-02.tex')
t = p.read_text(encoding='utf-8')
old = r"""\begin{align}
z_{nj}^{(l)}=\mu_j(\bm{x}_n,\bm{\phi})\,\varepsilon_{nj}^{(l)}+\sigma_j^{2}(\bm{x}_n,\bm{\phi}).
\label{align:ch19-重参数化样本}
\end{align}"""
new = r"""\begin{align}
z_{nj}^{(l)}=\mu_j(\bm{x}_n,\bm{\phi})+\sigma_j(\bm{x}_n,\bm{\phi})\,\varepsilon_{nj}^{(l)}.
\label{align:ch19-重参数化样本}
\end{align}"""
assert old in t, 'equation not found'
t = t.replace(old, new, 1)
old2 = '原书随后在\\eqref{align:ch19-完整损失}下方给出的元素表达式 $z_{nj}^{(l)}=\\sigma_{nj}\\varepsilon^{(l)}+\\mu_{nj}$（其中 $\\sigma_{nj}=\\sigma_j(\\bm{x}_n,\\bm{\\phi})$）正是上面的正确形式，可作为内部一致的依据；算法 19.1 中同一行赋值也应按此更正。本译本保留原式以供对照，实际使用时应采用修正形式。'
new2 = '原书随后在\\eqref{align:ch19-完整损失}下方给出的元素表达式 $z_{nj}^{(l)}=\\sigma_{nj}\\varepsilon^{(l)}+\\mu_{nj}$（其中 $\\sigma_{nj}=\\sigma_j(\\bm{x}_n,\\bm{\\phi})$）正是上面的正确形式，可作为内部一致的依据；算法 19.1 中同一行赋值也已采用该式。'
assert old2 in t, 'remark sentence not found'
t = t.replace(old2, new2, 1)
p.write_text(t, encoding='utf-8')
print('patched')
