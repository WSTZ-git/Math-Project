#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rigor patch for chapter-02 and chapter-19 introductory definitions."""
from pathlib import Path

ROOT = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning')


def patch(rel, pairs):
    p = ROOT / rel
    t = p.read_text(encoding='utf-8')
    for old, new in pairs:
        if old not in t:
            print('MISS', rel, old[:60].replace('\n', ' '))
        t = t.replace(old, new)
    p.write_text(t, encoding='utf-8')
    print('written', rel)


patch('contents/chapter-02.tex', [
("""若这种不确定性源自数据集的规模有限，即随着观测数据的增多（$N$ 增大）它可以被减小，则称之为\\textbf{认知不确定性}（epistemic uncertainty），也称系统不确定性（systematic uncertainty）。若这种不确定性即使 $N\\to\\infty$ 也不会消失，而源自人们只能观测到关于世界的部分信息，则称之为\\textbf{偶然不确定性}（aleatoric uncertainty），也称内在（intrinsic）不确定性或随机（stochastic）不确定性，有时简称噪声（noise）。""",
 """若这种不确定性源自数据集的规模有限，即随观测数据规模 $N$ 的增大而减小，则称其为\\textbf{认知不确定性}（epistemic uncertainty），也称系统不确定性（systematic uncertainty）。若这种不确定性即使 $N\\to\\infty$ 也不会消失，而源自观测者只能获得关于世界的部分信息，则称其为\\textbf{偶然不确定性}（aleatoric uncertainty），也称内在（intrinsic）不确定性或随机（stochastic）不确定性，有时简称噪声（noise）。"""),
])

patch('contents/chapter-19.tex', [
("""\\begin{definition}[自编码器]\\label{definition:ch19-自编码器}
自联想神经网络（auto-associative neural network）或\\textbf{自编码器}（autoencoder）是获得广泛认可的学习数据内部表示的方法，其中神经网络的输入单元和输出单元的数量相同，训练目的是让输出 $\\bm{y}$ 尽可能接近输入 $\\bm{x}$。一旦训练完成，神经网络中的一个内部层就为每个新的输入提供一个表示 $\\bm{z}(\\bm{x})$。这样的网络可以划分成两部分：首先是\\textbf{编码器}（encoder），它将输入 $\\bm{x}$ 映射到一个隐式表示 $\\bm{z}(\\bm{x})$；其次是\\textbf{解码器}（decoder），它将隐式表示映射到输出 $\\bm{y}(\\bm{z})$。
\\end{definition}""",
 """\\begin{definition}[自编码器]\\label{definition:ch19-自编码器}
设输入维数 $D\\geqslant1$、隐表示维数 $M\\geqslant1$，输入空间 $\\mathcal{X}\\subseteq\\mathbb{R}^{D}$，隐表示空间 $\\mathcal{Z}\\subseteq\\mathbb{R}^{M}$。设编码器 $e_{\\boldsymbol{\\theta}}:\\mathcal{X}\\to\\mathcal{Z}$ 与解码器 $d_{\\boldsymbol{\\phi}}:\\mathcal{Z}\\to\\mathcal{X}$ 为参数化映射，参数分别为 $\\boldsymbol{\\theta}\\in\\Theta$、$\\boldsymbol{\\phi}\\in\\Phi$，复合映射为 $f=d_{\\boldsymbol{\\phi}}\\circ e_{\\boldsymbol{\\theta}}$。给定训练集 $\\{\\bm{x}_n\\}_{n=1}^{N}\\subseteq\\mathcal{X}$，若参数 $(\\boldsymbol{\\theta},\\boldsymbol{\\phi})$ 由最小化重构误差
\\begin{align*}
  E(\\boldsymbol{\\theta},\\boldsymbol{\\phi})=\\frac{1}{N}\\sum_{n=1}^{N}\\bigl\\|\\bm{x}_n-d_{\\boldsymbol{\\phi}}(e_{\\boldsymbol{\\theta}}(\\bm{x}_n))\\bigr\\|^{2}
\\end{align*}
（或其他给定的重构损失）确定，则称 $f$ 为\\textbf{自编码器}（autoencoder），$e_{\\boldsymbol{\\theta}}$ 称为\\textbf{编码器}（encoder），$d_{\\boldsymbol{\\phi}}$ 称为\\textbf{解码器}（decoder），$\\bm{z}=e_{\\boldsymbol{\\theta}}(\\bm{x})\\in\\mathcal{Z}$ 称为输入 $\\bm{x}$ 的\\textbf{隐表示}（latent representation）。当 $M<D$ 时称为降维自编码器，当 $M>D$ 时称为过完备自编码器。
\\end{definition}"""),
])
