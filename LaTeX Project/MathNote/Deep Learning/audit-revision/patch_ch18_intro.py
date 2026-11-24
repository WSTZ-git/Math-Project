from pathlib import Path
p = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/chapter-18.tex')
t = p.read_text(encoding='utf-8')
old = """\\begin{definition}[标准化流]\\label{definition:ch18-标准化流}
设 $p_z$ 是潜变量 $\\bm{z}$ 上的简单分布（基础分布），$\\bm{f}(\\cdot,\\bm{w})$ 是由深度神经网络给出的可逆映射。若数据分布 $p_x$ 由\\cref{proposition:ch18-变量变换}的变量变换公式从 $p_z$ 与 $\\bm{f}$ 确定，则称这种对灵活分布进行建模的方法为\\textbf{标准化流}（normalizing flow），并称复合成 $\\bm{f}$ 的每个可逆映射为一层流。
\\end{definition}"""
new = """\\begin{definition}[标准化流]\\label{definition:ch18-标准化流}
设维数 $D\\geqslant1$，潜变量空间为 $\\mathbb{R}^{D}$，$p_z$ 为 $\\mathbb{R}^{D}$ 上的概率密度（称为基础分布）；设参数 $\\bm{w}\\in\\mathcal{W}$，$\\bm{f}(\\cdot,\\bm{w}):\\mathbb{R}^{D}\\to\\mathbb{R}^{D}$ 为 $C^{1}$ 双射，其 Jacobian 矩阵 $\\bm{J}_{\\bm{f}}(\\bm{z})=\\partial\\bm{f}(\\bm{z},\\bm{w})/\\partial\\bm{z}$ 满足 $\\det\\bm{J}_{\\bm{f}}(\\bm{z})\\neq0$ 对一切 $\\bm{z}\\in\\mathbb{R}^{D}$ 成立。若数据分布 $p_x$ 由\\cref{proposition:ch18-变量变换}的变量变换公式
\\begin{align*}
  p_x(\\bm{x})=p_z\\bigl(\\bm{f}^{-1}(\\bm{x},\\bm{w})\\bigr)\\bigl|\\det\\bm{J}_{\\bm{f}^{-1}}(\\bm{x})\\bigr|
\\end{align*}
从 $p_z$ 与 $\\bm{f}$ 确定，则称这种对灵活分布进行建模的方法为\\textbf{标准化流}（normalizing flow），并称复合成 $\\bm{f}$ 的每个可逆映射为一层流。
\\end{definition}"""
assert old in t, 'not found'
t = t.replace(old, new, 1)
p.write_text(t, encoding='utf-8')
print('patched')
