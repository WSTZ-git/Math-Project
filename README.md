# 数学笔记与 Lean 形式化

> 创建于 2024 年 10 月 25 日，持续更新中~

本仓库用于存放我在学习各个数学分支过程中记录的 LaTeX 笔记，以及用 Lean 4 对其中部分内容做的形式化验证。两个工程共享同一个 Git 仓库，统一提交、统一推送。

---

## 目录结构

```text
Math Project/
├── README.md
├── .gitignore                      忽略构建产物（.lake、LaTeX 中间文件等）
├── .vscode/settings.json           工作区设置：隐藏 .lake、排除搜索与监视
│
├── LaTeX Project/                  LaTeX 笔记工程
│   ├── MathNote/                   主体内容，按学科分目录
│   ├── Paper/                      论文
│   ├── PPT/                        演示文稿
│   ├── Others/                     其他材料
│   ├── Template/                   ElegantBook 模板（elegantbook.cls）
│   ├── Styles/                     自定义样式
│   ├── Sample Files/               subfiles 拆分示例
│   ├── VScode Configuration Files/ LaTeX 编译配方
│   ├── Code/                       模板与辅助脚本
│   ├── ElegantBook/                模板说明
│   └── Scratch/                    临时试验，不参与正式文档
│
└── Lean Project/                   Lean 4 形式化工程
    ├── lean-toolchain              固定 Lean 版本
    ├── lakefile.toml               Lake 工程定义
    ├── lake-manifest.json          依赖版本锁定（请勿手改）
    ├── LeanProject.lean            库入口，汇总 import
    ├── LeanProject/                库模块（路径即模块名）
    │   ├── Basic.lean              公共定义与记号
    │   ├── MathNote/PDE/Main.lean
    │   └── Paper/UndergraduateThesis/Main.lean
    └── Scratch/                    草稿区，不参与构建
```

---

## 环境要求

推荐在 **WSL2 + Ubuntu** 下工作，Windows 侧的 VS Code 通过 Remote-WSL 连接。

| 组件 | 要求 | 说明 |
|---|---|---|
| WSL2 / Ubuntu | 任意近期版本 | 所有编译都在 Linux 侧进行 |
| TeX Live | 含 `xelatex`、`biber`、`latexmk`、`ctex` | 用 `kpsewhich ctexart.cls` 检查 |
| elan | 4.x | Lean 版本管理器 |
| Lean | 4.36.0 | 由 `lean-toolchain` 固定，elan 自动匹配 |
| Lake | 5.0.0 | 随 Lean 一起安装 |
| VS Code | 1.100+ | 需装 **LaTeX Workshop** 与 **Lean 4** |

**VS Code 扩展必须装在 WSL 侧。** 在扩展面板里看到「Install in WSL: Ubuntu」按钮就点它；装在 Windows 侧会找不到 Linux 里的 elan 和 TeX。

---

## 快速开始

```bash
git clone git@github.com:WSTZ-git/Math.git "Math Project"
cd "Math Project"
code .
```

**务必确认左下角显示 `WSL: Ubuntu`**，否则 Lean 服务起不来、LaTeX 也会调用 Windows 的 TeX。

---

## LaTeX 笔记

### 模板

使用 [ElegantBook](https://github.com/ElegantLaTeX/ElegantBook) 模板，位于 `LaTeX Project/Template/`，各文档通过相对路径引用：

```latex
\documentclass[lang=cn,newtx,10pt,scheme=Chinese,citestyle=numeric,bibstyle=numeric]{../../Template/elegantbook}
```

### 编译

VS Code 中打开 `main.tex`，按 `Ctrl+Alt+B` 编译、`Ctrl+Alt+V` 预览。配方是 `latexmk` 调用 **XeLaTeX + Biber**（配置文件见 `VScode Configuration Files/`）。

由于中文必须走 XeLaTeX，若某个文件没有按预期编译，在首行加魔法注释：

```latex
% !TEX program = xelatex
```

### 文档拆分

页数较多的文档用 `subfiles` 宏包按章节拆分，编译时仍以 `main.tex` 为入口。可参考 `Sample Files/` 里已拆分好的例子。

### Scratch

`LaTeX Project/Scratch/` 放临时试验的 `.tex`，写坏了大不了删掉重来，不影响 `MathNote`、`Paper` 下的正式文档。

---

## Lean 形式化

### 构建

```bash
cd "Lean Project"
lake build          # 编译整个库
lake clean          # 清理 .lake/build
```

首次构建会自动下载 `lean-toolchain` 指定的 Lean 版本。若网络不通，可用 GitHub 直链手工安装 elan（`elan.lean-lang.org` 在国内可能超时）：

```bash
cd /tmp
curl -sSL -O https://github.com/leanprover/elan/releases/latest/download/elan-x86_64-unknown-linux-gnu.tar.gz
tar -xzf elan-x86_64-unknown-linux-gnu.tar.gz
./elan-init -y --default-toolchain none
```

### 模块与命名

**文件路径即模块名**，import 时把 `/` 换成 `.`：

| 文件 | 模块名 |
|---|---|
| `LeanProject/Basic.lean` | `LeanProject.Basic` |
| `LeanProject/MathNote/PDE/Main.lean` | `LeanProject.MathNote.PDE.Main` |

命名只能用英文、数字、下划线，**不能**有空格、连字符、点或中文，也不能以数字开头。`Ch1.2.lean` 这类名字会被解析成非法模块名。

`LeanProject.lean` 是库的聚合入口，只写 import。别处 `import LeanProject` 即可一次拿到全部内容。

### 新增一个课题

```bash
mkdir -p "Lean Project/LeanProject/MathNote/Algebra"
```

新建 `LeanProject/MathNote/Algebra/GroupTheory.lean`：

```lean
import LeanProject.Basic

namespace LeanProject.Algebra

-- 定义与定理

end LeanProject.Algebra
```

再在 `LeanProject.lean` 里补一行 `import LeanProject.MathNote.Algebra.GroupTheory`，然后 `lake build`。

### Scratch

`Lean Project/Scratch/` 在库目录之外，编辑器里照样能检查语法，但 `lake build` 不会因为它出错而失败。

---

## 仓库包含什么

仓库目前包含：

+ 抽象代数
+ 解析几何
+ 高等代数
+ 数学分析
+ 复分析
+ 微分几何
+ 微分流形
+ 泛函分析
+ 调和分析
+ 连续介质物理中的双曲守恒律
+ 测度论与非线性方程
+ 数论
+ 数值分析
+ 偏微分方程
+ 概率论
+ 实分析
+ 集合论
+ 拓扑学
+ 深度学习
+ 数值代数

---

## 日常命令

```bash
cd ~/"Math Project"

# 提交并推送
git add -A
git commit -m "说明这次改了什么"
git push

# 同步别人的改动
git pull
```

---

## 常见问题

**1. `.tex` 编译不报错但也没有输出**

最常见的原因是**路径里有中文**（例如 `MathNote/拓扑学/`），XeLaTeX 会在某些环节静默失败。把目录改成英文即可。另外确认该文件没有在别的程序里被占用。

**2. VS Code 里 Lean 代码全红 / 没有语法检查**

先看左下角是不是 `WSL: Ubuntu`。若是 `><` 本地窗口，说明是本地打开的，扩展找不到 Linux 里的 elan。

**3. `.lake` 目录不见了**

`.vscode/settings.json` 里把它隐藏了，磁盘上仍在。这是构建缓存，可以随时删除后重新 `lake build`，**不要提交**。

**4. 仓库里的 PDF 要不要提交**

目前 PDF 是入库的（方便直接看成品），单个最大约 49 MB。GitHub 单文件上限 100 MB、仓库超过 1 GB 会有提示。以后想瘦身可以：

```bash
git rm --cached -r "LaTeX Project/**/*.pdf"
echo "*.pdf" >> .gitignore
git commit -m "Stop tracking PDFs"
```

注意这只能阻止新 PDF 进入版本库，历史里的体积仍在。

**5. 构建产物突然一堆未跟踪文件**

检查根目录 `.gitignore` 是否被误改。正常状态下 `git status` 只应显示源码改动。

---

## AI 注明

+ 仓库中包含未经人工检验的 AI 生成内容，部分学科的部分内容可能经过人工重构。

---

## 为什么创立这个仓库？

**1. 用纸质笔记不易于更新**

纸质笔记写完就真的写完了，即使有时候想翻看，很难找到地方再添加一些内容，不便于后续修改整理。而且我记笔记比较乱，一般只有签字笔，不好区分重点，排版比较丑陋。

**2. 文件只放在电脑本地真的不安全**

用 git 就算是多了（至少）一个分布式存储节点，防止哪天电脑进水、笔记丢失这种悲惨的事情。

**3. git 方便多人协作**

如果多人编辑同一个 Word 文档，不同的人修改的部分需要重新复制粘贴到主文档上，容易丢失细节。而 git 上传拉取若有冲突会直接提示，可以准确监控每一个修改；编辑内容较多时也能通过分支与合并来整合多个人的工作。

---

## 为什么是 LaTeX？

Markdown 写起来很方便，但对公式的支持到今天仍然不够好，我在记笔记时遇到两个主要问题：

+ 对于交换图的支持不够好，画箭头会非常复杂。

+ 无法引用公式（LaTeX 的 `\ref`）。

第二个问题可能更为致命——无法引用意味着我没有办法有效地进行公式的引用，笔记中将充斥着大量「上式」以及「参考某一小节的某个公式」这样的模糊论述，查找起来会非常麻烦。
