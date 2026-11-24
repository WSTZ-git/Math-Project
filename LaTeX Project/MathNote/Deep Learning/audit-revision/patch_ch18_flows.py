from pathlib import Path
p = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/Chapter-18/section-02.tex')
t = p.read_text(encoding='utf-8')

old1 = """\\begin{definition}[掩码自回归流]\\label{definition:ch18-掩码自回归流}
设潜变量为 $\\bm{z}=(z_1,\\cdots,z_D)$、数据变量为 $\\bm{x}=(x_1,\\cdots,x_D)$。掩码自回归流是形如
\\begin{align}
  x_i=h\\big(z_i,g_i(\\bm{x}_{1:i-1},\\bm{w}_i)\\big)\\label{align:ch18-maf}
\\end{align}
的变换，其中 $h(z_i,\\cdot)$ 是耦合函数，因为对每个给定的条件值都可以很容易地对 $z_i$ 求逆；$g_i$ 是条件函数，通常用一个深度神经网络来表示，$\\bm{w}_i$ 是它的参数。
\\end{definition}"""
new1 = """\\begin{definition}[掩码自回归流]\\label{definition:ch18-掩码自回归流}
设维数 $D\\geqslant1$，潜变量 $\\bm{z}=(z_1,\\cdots,z_D)\\in\\mathbb{R}^{D}$，数据变量 $\\bm{x}=(x_1,\\cdots,x_D)\\in\\mathbb{R}^{D}$。对 $i=1,\\cdots,D$，设参数 $\\bm{w}_i\\in\\mathcal{W}_i$，条件函数 $g_i:\\mathbb{R}^{i-1}\\times\\mathcal{W}_i\\to\\mathbb{R}$（$g_1$ 只依赖 $\\bm{w}_1$），耦合函数 $h:\\mathbb{R}\\times\\mathbb{R}\\to\\mathbb{R}$。若变换由
\\begin{align}
  x_i=h\\big(z_i,g_i(\\bm{x}_{1:i-1},\\bm{w}_i)\\big),\\qquad i=1,\\cdots,D,
  \\label{align:ch18-maf}
\\end{align}
给出，且对每个固定的条件值 $c=g_i(\\bm{x}_{1:i-1},\\bm{w}_i)$，映射 $z_i\\mapsto h(z_i,c)$ 为 $C^{1}$ 双射、其导数处处非零，则称该变换为\\textbf{掩码自回归流}（Masked Autoregressive Flow, MAF）。$g_i$ 称为第 $i$ 个\\textbf{条件函数}，通常由深度神经网络表示；$h$ 称为\\textbf{耦合函数}。
\\end{definition}"""
assert old1 in t, 'maf not found'
t = t.replace(old1, new1, 1)

old2 = """\\begin{definition}[逆自回归流]\\label{definition:ch18-逆自回归流}
逆自回归流是形如
\\begin{align}
  x_i=h\\big(z_i,\\tilde{g}_i(\\bm{z}_{1:i-1},\\bm{w}_i)\\big)\\label{align:ch18-iaf}
\\end{align}
的变换，其中 $\\tilde{g}_i$ 是条件函数，$h(z_i,\\cdot)$ 是耦合函数。它与\\eqref{align:ch18-maf}的唯一差别在于：条件函数依赖的是潜变量的前缀 $\\bm{z}_{1:i-1}$，而不是数据变量的前缀 $\\bm{x}_{1:i-1}$。
\\end{definition}"""
new2 = """\\begin{definition}[逆自回归流]\\label{definition:ch18-逆自回归流}
设维数 $D\\geqslant1$，潜变量 $\\bm{z}=(z_1,\\cdots,z_D)\\in\\mathbb{R}^{D}$，数据变量 $\\bm{x}=(x_1,\\cdots,x_D)\\in\\mathbb{R}^{D}$。对 $i=1,\\cdots,D$，设参数 $\\bm{w}_i\\in\\mathcal{W}_i$，条件函数 $\\tilde{g}_i:\\mathbb{R}^{i-1}\\times\\mathcal{W}_i\\to\\mathbb{R}$，耦合函数 $h:\\mathbb{R}\\times\\mathbb{R}\\to\\mathbb{R}$。若变换由
\\begin{align}
  x_i=h\\big(z_i,\\tilde{g}_i(\\bm{z}_{1:i-1},\\bm{w}_i)\\big),\\qquad i=1,\\cdots,D,
  \\label{align:ch18-iaf}
\\end{align}
给出，且对每个固定的条件值 $c=\\tilde{g}_i(\\bm{z}_{1:i-1},\\bm{w}_i)$，映射 $z_i\\mapsto h(z_i,c)$ 为 $C^{1}$ 双射、其导数处处非零，则称该变换为\\textbf{逆自回归流}（Inverse Autoregressive Flow, IAF）。它与\\eqref{align:ch18-maf}的唯一差别在于：条件函数依赖的是潜变量的前缀 $\\bm{z}_{1:i-1}$，而不是数据变量的前缀 $\\bm{x}_{1:i-1}$。
\\end{definition}"""
assert old2 in t, 'iaf not found'
t = t.replace(old2, new2, 1)
p.write_text(t, encoding='utf-8')
print('patched')
