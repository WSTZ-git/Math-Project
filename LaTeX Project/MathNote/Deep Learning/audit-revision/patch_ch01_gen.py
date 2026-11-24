from pathlib import Path
p = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/Chapter-01/section-01.tex')
t = p.read_text(encoding='utf-8')
old = '若存在 $\\varepsilon>0$ 使 $d(p_{\\boldsymbol{\\theta}},p_{\\mathrm{data}})\\leqslant\\varepsilon$，且由 $p_{\\boldsymbol{\\theta}}$ 采样所得的样本以概率 $1$ 不等于任何训练样本，则 $\\{p_{\\boldsymbol{\\theta}}\\}$ 连同其采样过程称为\\textbf{生成式模型}（generative model）；'
new = '给定容差 $\\varepsilon\\in(0,1)$。若 $d(p_{\\boldsymbol{\\theta}},p_{\\mathrm{data}})\\leqslant\\varepsilon$ 且存在从 $p_{\\boldsymbol{\\theta}}$ 采样的算法，则 $\\{p_{\\boldsymbol{\\theta}}\\}$ 连同其采样过程称为\\textbf{生成式模型}（generative model）；'
assert old in t, 'not found'
t = t.replace(old, new, 1)
# Add an explanation to the following remark, after the first paragraph.
anchor = '由于没有标签可以把“错”定义成“与 $t_n$ 不一致”，无监督学习必须以数据分布本身为学习目标，这既是它的困难所在，也是它能够被用于生成的原因。'
assert anchor in t, 'remark anchor not found'
extra = '\n\n定义中的“新样本”指从 $p_{\\boldsymbol{\\theta}}$ 独立抽取的样本，并不要求它与训练集逐点不同：在连续分布下，新样本与任一训练样本重合的概率为零；在离散分布下则允许以正概率重复训练样本，这正是语言模型可以逐字复现训练文本的原因。容差 $\\varepsilon$ 是模型选择时给定的精度指标，不是“存在某个 $\\varepsilon$”的存在性断言。'
if '定义中的“新样本”指从' not in t:
    t = t.replace(anchor, anchor + extra, 1)
p.write_text(t, encoding='utf-8')
print('patched')
