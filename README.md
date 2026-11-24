# 数学笔记与 Lean 形式化

LaTeX 记录的数学笔记，以及对应的 Lean 4 形式化代码，放在同一个仓库里统一管理。

## 仓库结构

```text
Math Project/
├── LaTeX Project/                  LaTeX 笔记工程
│   ├── MathNote/                   笔记主体，一个学科一个目录
│   ├── Paper/                      论文
│   ├── PPT/                        演示文稿
│   ├── Others/                     其他材料
│   ├── Template/                   ElegantBook 模板
│   ├── Styles/                     自定义样式
│   ├── Sample Files/               subfiles 拆分示例
│   ├── VScode Configuration Files/ LaTeX 编译配方
│   ├── Code/                       辅助脚本
│   ├── ElegantBook/                模板说明
│   └── Scratch/                    临时试验
└── Lean Project/                   Lean 4 形式化工程
    ├── LeanProject/                库模块，目录结构即模块名
    ├── LeanProject.lean            库入口，汇总 import
    ├── lakefile.toml               工程定义
    ├── lake-manifest.json          依赖版本锁定
    ├── lean-toolchain              固定的 Lean 版本
    └── Scratch/                    草稿，不参与构建
```

## 文件夹与文件作用

| 路径 | 作用 |
|---|---|
| `LaTeX Project/MathNote/` | 全部笔记，每篇一个目录 |
| `LaTeX Project/Template/` | ElegantBook 模板，笔记用 `../../Template/elegantbook` 引用 |
| `LaTeX Project/Styles/` | 自定义宏与样式 |
| `LaTeX Project/Sample Files/` | `subfiles` 拆分示例，新建笔记照此结构 |
| `LaTeX Project/VScode Configuration Files/` | `latexmk` 配方，调用 XeLaTeX + Biber |
| `LaTeX Project/Scratch/` | 临时试验的 `.tex`，不影响正式文档 |
| `Lean Project/LeanProject/` | Lean 源码，路径即模块名，如 `LeanProject/Basic.lean` 对应 `LeanProject.Basic` |
| `Lean Project/LeanProject.lean` | 库入口，只写 import，`import LeanProject` 即可载入全部 |
| `Lean Project/lakefile.toml` | 包名、构建目标与依赖 |
| `Lean Project/lean-toolchain` | 固定 Lean 版本，elan 据此选择编译器 |
| `Lean Project/lake-manifest.json` | 依赖版本锁定，自动生成，请勿手改 |
| `Lean Project/Scratch/` | 草稿区，编辑器可检查，但不参与 `lake build` |
| `.gitignore` | 忽略 `.lake` 与 LaTeX 中间文件 |
| `.vscode/settings.json` | 隐藏 `.lake`，排除搜索与文件监视 |
| `.vscode/tasks.json` | 批量清理与编译任务 |

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

## 使用

```bash
# 编译笔记：打开某篇的 main.tex 后
Ctrl+Alt+B     # latexmk + XeLaTeX + Biber
Ctrl+Alt+V     # 预览 PDF

# 形式化
cd "Lean Project"
lake build

# 提交
cd ~/"Math Project"
git add -A && git commit -m "说明" && git push
```

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

## 为什么创建

**纸质笔记不易更新。** 写完就固定了，想补内容找不到地方；手写排版也难以区分重点。

**本地文件不安全。** 用 git 至少多一个分布式存储节点，不怕硬盘损坏或误删。

**git 便于协作。** 冲突会直接提示，改动可逐行追溯，也能用分支整合多个人的工作。

## AI 注明

仓库中包含未经人工检验的 AI 生成内容，部分学科的部分内容经过人工重构。
