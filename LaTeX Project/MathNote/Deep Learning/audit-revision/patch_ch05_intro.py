#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rigor patch for contents/chapter-05.tex introductory definitions."""
from pathlib import Path

p = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/chapter-05.tex')

REPL = [
("""\\begin{definition}[决策区域、决策边界与线性可分]\\label{definition:ch05-决策区域}
将输入空间划分为若干区域$\\mathcal{R}_k$，并令每个区域对应一个类$C_k$，即约定当且仅当$\\boldsymbol{x}\\in\\mathcal{R}_k$时把$\\boldsymbol{x}$归入$C_k$类。这些区域称为决策区域（decision region）。决策区域之间的边界称为决策边界（decision boundary）或决策面（decision surface）。若存在一个线性决策面，使得数据集中的每个输入向量都被归入其所属的类，则称该数据集是线性可分（linearly separable）的。
\\end{definition}""",
"""\\begin{definition}[决策区域、决策边界与线性可分]\\label{definition:ch05-决策区域}
设 $D\\geqslant1$，输入空间 $\\mathcal{X}\\subseteq\\mathbb{R}^{D}$，类标签集 $\\{C_1,\\cdots,C_K\\}$（$K\\geqslant2$）。若 $\\mathcal{R}_1,\\cdots,\\mathcal{R}_K\\subseteq\\mathcal{X}$ 满足 $\\mathcal{R}_i\\cap\\mathcal{R}_j=\\varnothing$（$i\\neq j$）且 $\\bigcup_{k=1}^{K}\\mathcal{R}_k=\\mathcal{X}$，并约定 $\\boldsymbol{x}\\in\\mathcal{R}_k$ 时把 $\\boldsymbol{x}$ 归入 $C_k$ 类，则称 $\\mathcal{R}_k$ 为类 $C_k$ 的\\textbf{决策区域}（decision region）。若两个决策区域的闭包相交，则其交集称为\\textbf{决策边界}（decision boundary）或决策面（decision surface）。设 $\\mathcal{D}=\\{(\\boldsymbol{x}_n,t_n)\\}_{n=1}^{N}\\subseteq\\mathcal{X}\\times\\{C_1,\\cdots,C_K\\}$ 为数据集。若 $K=2$ 且存在 $\\boldsymbol{w}\\in\\mathbb{R}^{D}$、$w_0\\in\\mathbb{R}$，使得对每个 $n$ 都有
\\begin{align*}
  t_n=C_1\\iff \\boldsymbol{w}^{\\mathsf{T}}\\boldsymbol{x}_n+w_0>0,
\\end{align*}
则称 $\\mathcal{D}$ 关于该线性决策面是\\textbf{线性可分}的（linearly separable）。
\\end{definition}"""),

("""\\begin{definition}[判别函数]\\label{definition:ch05-判别函数}
判别函数（discriminant function）是把每个输入向量$\\boldsymbol{x}$直接映射到某个类标签上的函数$f(\\boldsymbol{x})$；等价地说，它不借助任何概率模型，直接把输入空间划分为若干决策区域。
\\end{definition}""",
"""\\begin{definition}[判别函数]\\label{definition:ch05-判别函数}
设 $D\\geqslant1$，输入空间 $\\mathcal{X}\\subseteq\\mathbb{R}^{D}$，类标签集 $\\mathcal{C}=\\{C_1,\\cdots,C_K\\}$（$K\\geqslant2$）。若映射 $f:\\mathcal{X}\\to\\mathcal{C}$ 不借助概率模型，直接把每个输入 $\\boldsymbol{x}\\in\\mathcal{X}$ 映到某个类标签，则称 $f$ 为\\textbf{判别函数}（discriminant function）；$f$ 的等值集 $\\{\\boldsymbol{x}\\in\\mathcal{X}:f(\\boldsymbol{x})=C_k\\}$ 给出类 $C_k$ 的决策区域。
\\end{definition}"""),

("""\\begin{definition}[判别概率模型与生成概率模型]\\label{definition:ch05-生成与判别概率模型}
设$p(C_k\\mid\\boldsymbol{x})$为给定输入$\\boldsymbol{x}$时类$C_k$的后验概率。
\\begin{enumerate}[(i)]
  \\item 直接对后验概率$p(C_k\\mid\\boldsymbol{x})$建模，例如把它表示为参数模型并用训练集优化参数，这样得到的方法称为判别概率模型（discriminative probabilistic model）。
  \\item 先对类-条件概率密度$p(\\boldsymbol{x}\\mid C_k)$以及类的先验概率$p(C_k)$建模，再使用 Bayes 定理计算所需的后验概率，这样得到的方法称为生成概率模型（generative probabilistic model）。
\\end{enumerate}
\\end{definition}""",
"""\\begin{definition}[判别概率模型与生成概率模型]\\label{definition:ch05-生成与判别概率模型}
设 $D\\geqslant1$，输入空间 $\\mathcal{X}\\subseteq\\mathbb{R}^{D}$，类标签集 $\\{C_1,\\cdots,C_K\\}$。设 $(\\Omega,\\mathcal{F},\\mathbb{P})$ 为概率空间，$\\boldsymbol{X}:\\Omega\\to\\mathcal{X}$ 与 $C:\\Omega\\to\\{C_1,\\cdots,C_K\\}$ 为随机变量，$p(\\boldsymbol{x},C_k)$ 为 $(\\boldsymbol{X},C)$ 的联合分布，$p(C_k\\mid\\boldsymbol{x})$ 为给定 $\\boldsymbol{X}=\\boldsymbol{x}$ 时 $C=C_k$ 的后验概率。
\\begin{enumerate}[(i)]
  \\item 若模型直接对后验概率族 $\\{p_{\\boldsymbol{\\theta}}(C_k\\mid\\boldsymbol{x}):\\boldsymbol{\\theta}\\in\\Theta\\}$ 作参数假设，并用训练数据确定 $\\boldsymbol{\\theta}$，则称该方法为\\textbf{判别概率模型}（discriminative probabilistic model）；
  \\item 若模型先对类条件密度族 $\\{p_{\\boldsymbol{\\phi}}(\\boldsymbol{x}\\mid C_k)\\}$ 与先验概率 $\\{p(C_k)\\}$ 作参数假设，再用 Bayes 定理
  \\begin{align*}
    p(C_k\\mid\\boldsymbol{x})=\\frac{p_{\\boldsymbol{\\phi}}(\\boldsymbol{x}\\mid C_k)p(C_k)}{\\sum_{j=1}^{K}p_{\\boldsymbol{\\phi}}(\\boldsymbol{x}\\mid C_j)p(C_j)}
  \\end{align*}
  计算后验概率（要求分母为正），则称该方法为\\textbf{生成概率模型}（generative probabilistic model）。
\\end{enumerate}
\\end{definition}"""),

("""\\begin{definition}[线性判别式]\\label{definition:ch05-线性判别式}
若一个判别式（判别函数）的决策面是输入空间中的超平面，则称它为线性判别式（linear discriminant）。
\\end{definition}""",
"""\\begin{definition}[线性判别式]\\label{definition:ch05-线性判别式}
设 $D\\geqslant1$，输入空间 $\\mathcal{X}\\subseteq\\mathbb{R}^{D}$，$f:\\mathcal{X}\\to\\{C_1,\\cdots,C_K\\}$ 为判别函数。若存在 $\\boldsymbol{w}\\in\\mathbb{R}^{D}\\setminus\\{\\boldsymbol{0}\\}$ 与 $w_0\\in\\mathbb{R}$，使得 $f$ 的每个决策边界都包含于超平面
\\begin{align*}
  H=\\{\\boldsymbol{x}\\in\\mathcal{X}:\\boldsymbol{w}^{\\mathsf{T}}\\boldsymbol{x}+w_0=0\\}
\\end{align*}
之中，则称 $f$ 为\\textbf{线性判别式}（linear discriminant）；$\\boldsymbol{w}$ 称为该超平面的法向量，$w_0$ 称为偏置。
\\end{definition}"""),
]

def main():
    t = p.read_text(encoding='utf-8')
    for old, new in REPL:
        if old not in t:
            print('MISS', old[:60].replace('\n', ' '))
        t = t.replace(old, new)
    p.write_text(t, encoding='utf-8')
    print('written', p)

if __name__ == '__main__':
    main()
