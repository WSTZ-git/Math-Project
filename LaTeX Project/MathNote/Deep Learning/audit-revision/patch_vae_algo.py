from pathlib import Path
p = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/Chapter-19/section-02.tex')
t = p.read_text(encoding='utf-8')
old = r'\hspace*{3em}$z_{nj}\leftarrow\mu_j(\bm{x}_n,\bm{\phi})\,\varepsilon_{nj}+\sigma_j^{2}(\bm{x}_n,\bm{\phi})$ \quad // 原文如此，见上文更正\\'
new = r'\hspace*{3em}$z_{nj}\leftarrow\mu_j(\bm{x}_n,\bm{\phi})+\sigma_j(\bm{x}_n,\bm{\phi})\,\varepsilon_{nj}$ \quad // 重参数化采样\\'
assert old in t, 'not found'
t = t.replace(old, new, 1)
p.write_text(t, encoding='utf-8')
print('patched')
