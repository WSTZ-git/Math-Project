# 数学笔记与 Lean 形式化

LaTeX 记录的数学笔记，以及对应的 Lean 4 形式化代码，放在同一个仓库里统一管理。

## 仓库结构

```text
Math Project/
├── Code/                                论文配套代码
│   └── Python/
│       └── Undergraduate Thesis Code/   本科毕业论文的代码、data/ 数据与 figures/ 插图
├── ElegantBook/                         ElegantBook 模板官方文档与示例
├── LaTeX Project/                       LaTeX 笔记工程
│   ├── MathNote/                        全部笔记，一个学科一个目录
│   ├── Paper/                           论文
│   ├── PPT/                             演示文稿
│   ├── Others/                          其他材料
│   ├── Template/                        ElegantBook 模板，笔记以 ../../Template/elegantbook 引用
│   ├── Styles/                          自定义宏与样式
│   ├── Sample Files/                    subfiles 拆分示例，新建笔记照此结构
│   ├── VScode Configuration Files/      latexmk 配方，调用 XeLaTeX + Biber
│   ├── Scratch/                         临时试验，不影响正式文档
│   └── Latex常见问题.txt                编译问题记录
├── Lean Project/                        Lean 4 形式化工程（依赖 mathlib v4.36.0）
│   ├── LeanProject/                     库模块，目录结构即模块名
│   │   ├── MathNote/PDE/Main.lean       偏微分方程笔记
│   │   └── Paper/UndergraduateThesis/   本科毕业论文
│   │       └── Main.lean
│   ├── LeanProject.lean                 库入口，汇总 import
│   ├── lakefile.toml                    包名、构建目标与依赖
│   ├── lake-manifest.json               依赖版本锁定，自动生成，勿手改
│   ├── lean-toolchain                   固定的 Lean 版本
│   └── Scratch/Test.lean                测试文件，测试 Lean 用的，不参与构建
├── MIL/                                 Mathematics in Lean 教材与习题（随仓库提供）
├── .vscode/
│   ├── settings.json                    全仓库唯一配置：隐藏 .lake、LaTeX 中间文件与 PDF，排除搜索与监视
│   └── tasks.json                       批量清理与编译任务
├── .gitignore                           忽略 .lake 与 LaTeX 中间文件
└── README.md
```

## 本地环境

项目在 **WSL2 + Ubuntu** 下开发，Windows 侧的 VS Code 通过 **Remote-WSL** 连接，所有编译都在 Linux 侧完成。

### 版本

| 组件 | 当前版本 | 验证命令 |
|---|---|---|
| Ubuntu (WSL2) | 26.04 LTS | `lsb_release -d` |
| TeX Live / XeLaTeX | 2025 | `xelatex --version` |
| latexmk | 4.87 | `latexmk -v` |
| Biber | 2.21 | `biber --version` |
| Python | 3.14 | `python3 --version` |
| elan | 4.4.0 | `elan --version` |
| Lean | 4.36.0 | `lean --version` |
| Lake | 5.0.0 | `lake --version` |

### LaTeX

需要 XeLaTeX、Biber、latexmk，以及中文支持（`ctex`）：

```bash
sudo apt install texlive-xetex texlive-lang-chinese texlive-bibtex-extra \
                 texlive-latex-extra biber latexmk
```

完整安装可用 `texlive-full`（约 5 GB）。装完验证：

```bash
kpsewhich ctexart.cls      # 有输出即可
```

VS Code 需安装 **LaTeX Workshop** 扩展，并且必须装在 **WSL 侧**（扩展面板里点「Install in WSL: Ubuntu」）。

### Lean 4

需要 elan，由它按 `lean-toolchain` 自动匹配编译器版本。推荐用 GitHub 直链安装（官方一键脚本依赖 `elan.lean-lang.org`，国内常超时）：

```bash
cd /tmp
curl -sSL -O https://github.com/leanprover/elan/releases/latest/download/elan-x86_64-unknown-linux-gnu.tar.gz
tar -xzf elan-x86_64-unknown-linux-gnu.tar.gz
./elan-init -y --default-toolchain none
```

装好后 `~/.elan/bin` 会写入 `~/.profile`，重开终端生效。Lean 本身不用手动装——首次 `lake build` 会按 `Lean Project/lean-toolchain` 自动下载 4.36.0。

工程依赖 **mathlib v4.36.0**。首次构建前先下载预编译缓存（约 7 GB），否则 Lake 会本地编译 mathlib：

```bash
cd "Lean Project"
lake exe cache get
```

仓库根目录的 `MIL/` 是 [Mathematics in Lean](https://github.com/leanprover-community/mathematics_in_lean) 教材工程（Lean 4.34.0，独立于 `Lean Project`，两者不互相 import），源码随仓库提供。克隆后需自行下载 mathlib 缓存（约 8 GB），否则 Lake 会本地编译 mathlib：

```bash
cd MIL
lake exe cache get
lake build
```

VS Code 需安装 **Lean 4** 扩展，同样装在 **WSL 侧**。

### Python

论文配套代码要求 Python 3.10+，依赖见 `Code/Python/Undergraduate Thesis Code/requirements.txt`：

```bash
cd "Code/Python/Undergraduate Thesis Code"
./setup.sh                     # 装到 ./.pylibs，不污染系统环境
export PYTHONPATH=.:.pylibs
export MPLCONFIGDIR=/tmp/mplconfig
```

## 笔记内容

每篇笔记的结构：

```text
MathNote/学科名/
├── main.tex                  入口，含 documentclass 与 \subfile
├── contents/Chapter-XX/      按章节拆分的正文
├── figure/  image/           插图
└── main.pdf                  编译产物
```

目前收录：

<table>
  <tr><td>抽象代数</td><td>解析几何</td><td>高等代数</td></tr>
  <tr><td>数学分析</td><td>复分析</td><td>微分几何</td></tr>
  <tr><td>微分流形</td><td>泛函分析</td><td>调和分析</td></tr>
  <tr><td>连续介质物理中的双曲守恒律</td><td>测度论与非线性方程</td><td>数论</td></tr>
  <tr><td>数值分析</td><td>偏微分方程</td><td>概率论</td></tr>
  <tr><td>实分析</td><td>集合论</td><td>拓扑学</td></tr>
  <tr><td>深度学习</td><td>数值代数</td><td></td></tr>
</table>

### 批量任务

`终端 → 运行任务…` 中可执行：

| 任务 | 作用 |
|---|---|
| `Clean Auxiliary Files` | 清理 `MathNote` 下全部笔记的中间文件 |
| `Compile All Sub-documents` | 编译 `MathNote` 下所有 `main.tex` |
| `Clean & Compile All Sub-documents` | 先清理，再全部编译 |
| `Clean One Note's Aux Files` | 选择单篇笔记，只清理该文件夹的中间文件 |

单篇清理运行时会弹出下拉列表选择文件夹。新增笔记后，把文件夹名补进 `.vscode/tasks.json` 的 `inputs.noteFolder.options`。

新增笔记：复制 `Sample Files/` 的结构。新增 Lean 模块：在 `LeanProject/` 下建文件，写 `namespace`，再在 `LeanProject.lean` 里补一行 import。

Lean 文件引用 mathlib 定理有两种方式：`import Mathlib`（全部，最省事）、`import Mathlib.Analysis.Calculus.Deriv.Pow`（只引某个模块，编译最快）。示例见 `Lean Project/Scratch/Test.lean`。

## 为什么创建

**纸质笔记不易更新。** 写完就固定了，想补内容找不到地方；手写排版也难以区分重点。

**本地文件不安全。** 用 git 至少多一个分布式存储节点，不怕硬盘损坏或误删。

**git 便于协作。** 冲突会直接提示，改动可逐行追溯，也能用分支整合多个人的工作。

## AI 注明

仓库中包含未经人工检验的 AI 生成内容，部分学科的部分内容经过人工重构。
