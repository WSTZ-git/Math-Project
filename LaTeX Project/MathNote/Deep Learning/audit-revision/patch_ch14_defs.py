from pathlib import Path
ROOT = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning')

# 1. chapter-14 sampling definition
p = ROOT / 'contents/chapter-14.tex'
t = p.read_text(encoding='utf-8')
old = """\\begin{definition}[采样与样本]\\label{definition:ch14-采样}
从概率分布 $p(\\bm{z})$ 中生成取值 $\\bm{z}$ 的过程称为采样（sampling），也称 Monte Carlo 采样（Monte Carlo sampling）；其中每一个被实例化的取值称为一个样本（sample）。
\\end{definition}"""
new = """\\begin{definition}[采样与样本]\\label{definition:ch14-采样}
设 $D\\geqslant1$，概率空间 $(\\Omega,\\mathcal{F},\\mathbb{P})$，随机变量 $\\bm{Z}:\\Omega\\to\\mathbb{R}^{D}$ 的分布为 $p(\\bm{z})$（关于 Lebesgue 测度或计数测度）。若一个计算过程每次运行都返回 $\\bm{Z}(\\omega)$ 的一个实现值 $\\bm{z}\\in\\mathbb{R}^{D}$，且对每个 Borel 集 $B\\subseteq\\mathbb{R}^{D}$ 有 $\\mathbb{P}(\\bm{Z}\\in B)=\\int_{B}p(\\bm{z})\\,\\mathrm{d}\\bm{z}$（离散情形为求和），则称该过程为从 $p$ \\textbf{采样}（sampling），也称 Monte Carlo 采样（Monte Carlo sampling）；每次返回的实现值称为一个\\textbf{样本}（sample）。
\\end{definition}"""
assert old in t, 'sampling def not found'
t = t.replace(old, new, 1)
p.write_text(t, encoding='utf-8')
print('patched chapter-14 sampling')

# 2. Chapter-14 energy-based model definition
p = ROOT / 'contents/Chapter-14/section-03.tex'
t = p.read_text(encoding='utf-8')
old2 = """\\begin{definition}[基于能量的模型]\\label{definition:ch14-基于能量模型}
设 $E(\\bm{x},\\bm{w})$ 是数据向量 $\\bm{x}$ 与参数 $\\bm{w}$ 的实值函数，称为能量函数，且
\\begin{align*}
0<Z(\\bm{w})=\\int\\exp\\{-E(\\bm{x},\\bm{w})\\}\\,\\mathrm{d}\\bm{x}<\\infty.
\\end{align*}
则由\\eqref{align:ch14-ebm}定义的分布族 $\\left\\{p(\\bm{x}\\mid\\bm{w})\\right\\}$ 称为基于能量的模型（energy-based model，EBM），$Z(\\bm{w})$ 称为配分函数（partition function）。
\\end{definition}"""
new2 = """\\begin{definition}[基于能量的模型]\\label{definition:ch14-基于能量模型}
设数据维数 $d\\geqslant1$、参数维数 $P\\geqslant1$，$\\bm{x}\\in\\mathbb{R}^{d}$、$\\bm{w}\\in\\mathbb{R}^{P}$，能量函数 $E:\\mathbb{R}^{d}\\times\\mathbb{R}^{P}\\to\\mathbb{R}$ 为 Borel 可测函数，且
\\begin{align*}
0<Z(\\bm{w})=\\int_{\\mathbb{R}^{d}}\\exp\\{-E(\\bm{x},\\bm{w})\\}\\ \\mathrm{d}\\bm{x}<\\infty
\\end{align*}
对每个 $\\bm{w}\\in\\mathbb{R}^{P}$ 成立。则由\\eqref{align:ch14-ebm}定义的分布族 $\\left\\{p(\\bm{x}\\mid\\bm{w}):\\bm{w}\\in\\mathbb{R}^{P}\\right\\}$ 称为\\textbf{基于能量的模型}（energy-based model，EBM），$Z(\\bm{w})$ 称为\\textbf{配分函数}（partition function）。
\\end{definition}"""
assert old2 in t, 'ebm def not found'
t = t.replace(old2, new2, 1)
p.write_text(t, encoding='utf-8')
print('patched EBM')
