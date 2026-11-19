# Deep Learning 严格化重写进度（2026-11-15）

## 已完成

- 备份：`audit-revision/original-tex-backup.zip`（改写前全部 .tex）。
- 清除全书 1828 处“重构新增”（源码与 PDF 可见文本均为 0）。
- 插件更新（v1.1.0）：
  - `spec-v14.md` / `SKILL.md` / `src/v14-complete.txt` 新增 §3.11 严格性规范；
  - 废止可见“重构新增”标记，改为只在 `% SUPPLEMENT:` 与 `audit/supplements.csv` 登记；
  - `check.py` 新增 RIG-001..RIG-012，纳入 gate 的 ERROR 统计；
  - requirements 新增 R14-01..R14-08；习题只保留题面。
- 已严格化并通过 `check_file.py`（零 RIG 或仅合理 WARN）：
  - Chapter-01（3 节）
  - Chapter-02（6 节，82 个环境）
  - Chapter-03 section-01..03；section-04..05 正在由子代理处理
  - appendix-A（全部）
  - appendix-B（全部，仅少量误报 WARN）
  - appendix-C（全部，仅少量误报 WARN）

## 进行中（子代理）

- Chapter-04..05
- Chapter-06..07
- Chapter-08..09
- Chapter-10..11
- Chapter-12..14

## 待开始

- Chapter-15..17
- Chapter-18..20
- Chapter-03 section-04..05（子代理）
- 全局 proof 元叙述清理（“原书…补全/显然/易证/我们”）
- 全书 xelatex 构建
- 最终 RIG 全量复查、PDF 目视抽查、插件 BUILD_INFO 刷哈希

## 已知问题

- `edit` 工具对部分 `\\wsl.localhost` 文件报 `GetFileSecurityW EIO`；改用 WSL 内
  Python 脚本打补丁（见 `patch_appB.py`、`patch_appC.py`、`clean_proofs.py`）。
- `main.pdf` 仍是 2026-11-09 的旧版本；所有改动完成后必须重建。
- 部分 RIG WARN 是误报（公式型定义被剥离后长度过短、`则称 $X$ 为` 被数学打断），
  不应为了消 WARN 而删改正确内容。

## 复查命令

```bash
cd "/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning"
python3 audit-revision/run_rigor_probe.py      # 全书 RIG 汇总
python3 audit-revision/check_file.py <file>    # 单文件
```
