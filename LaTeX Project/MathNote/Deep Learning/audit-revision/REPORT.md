# Deep Learning 严格化重写报告（2026-11-15）

## 1. 范围与结果

- 对象：`MathNote/Deep Learning/contents` 全书 20 章 + 3 个附录。
- 定义/定理/命题/引理/推论环境：**763 个**；其中 **725 个**的正文被改写（其余 38 个原文已足够严格或仅为标题性陈述）。
- label：改写前后均为 763 个语句环境，**0 新增、0 删除、0 重命名**；全书 `\cref`/`\eqref`/`\hyperref` 目标解析 **0 缺失**。
- “（重构新增）”：改写前 1828 处（源码/注释），改写后 **0 处**；最终 PDF 文本中 **0 处**。
- 习题：全部只保留题面；`solution` 共 9 处，全部跟在 `example`（正文例题）之后，没有习题解答。
- 最终 PDF：**791 页**，`main.pdf`，49 MB；`xelatex` 日志 `^!` 错误 **0**，未定义引用 **0**，PDF 中 `??` **0**。

## 2. 改写标准

依据插件规范新增的 §3.11（`references/spec-v14.md`）：

1. 每个陈述自足：数域/空间、对象类型与形状（矩阵行×列、方阵/对称/正定/可逆、张量轴长、向量维数）、定义域/值域、指标与参数范围、正则性、概率假设、量词顺序、非退化条件、继承假设。
2. 句式统一为“设……。若……，则称/则……。”；只给公式的条目补文字陈述。
3. 环境体内禁止口语与元叙述（我们/可以/其实/显然/注意/这就/也就是说/换句话说/例如/直观上/不妨/容易看出/来看/想想/有趣的是；重构新增/补写/原书/译文/本工程/笔者）。
4. 动机、直观、历史、边界与反例全部放入紧随的 `remark`；新增身份只写在 `% SUPPLEMENT:` 注释与 `audit/supplements.csv`（本工程无来源 PDF，故只保留源码注释，未伪造台账）。
5. 证明不得用“显然/类似地/容易验证/读者可证/原书/补全如下”代替推导；每步给出定义、已证结果或标准定理依据。
6. 习题只保留题面，不写 solution。

## 3. 机械检查

插件 `check.py` 新增 `RIG-001..RIG-012`，其中：

- ERROR：可见/注释中的“重构新增”、硬口语、证明 hand-wave、习题内解答、形式环境中的元叙述、残留标记。
- WARN：软口语候选、缺假设句开头、陈述过短、矩阵缺形状、模型条目只有公式、定义缺定义句式。

最终全量 RIG：**0 ERROR，17 WARN**。17 条 WARN 均为检查器已知误报：

- `RIG-008`（8 条）：`则称 $\bm{X}$ 为……` 被数学片段打断，检查器按连续字符串“称为”误判；定义本身完整。
- `RIG-005`（9 条）：陈述主体是 `align` 公式，检查器剥离数学后按汉字数误判“过短”；公式前后的文字与假设完整。
- 其余为附录 B/C 的短小但完整的定义（泛函、基本引理、约束曲面等）。

没有用 waiver、没有改检查器来消除这些 WARN。

## 4. 主要数学修正（示例）

- 附录 A：`秩=非零特征值个数` 改为“可对角化”版本并给反例；矩阵的转置/逆/秩/迹/行列式/特征向量/正交/正定全部写明阶数与类型；谱定理补出重特征值情形的归纳证明。
- 第 3 章：Gauss 最大似然在散布矩阵奇异时无上界，改为分情形陈述；指数族补自然参数空间、测度与归一化条件；von Mises 补 $\bar R>0$ 与 $\bar R=1$ 分支。
- 第 6 章：高维 Gauss 薄壳展开系数更正；线性隐单元参数量条件改为 $M<KD/(D+K+1)$；分段线性区域数补完整计数论证。
- 第 9 章：网络重参数化的 $\lambda$ 缩放指数更正为 $a^2,c^{-2}$；lasso 约束等价改为逐点对应；早停等价用夹逼不等式替代渐近口语。
- 第 19 章：VAE 重参数化公式更正为 $z=\mu+\sigma\varepsilon$（原书印作 $\mu\varepsilon+\sigma^2$），算法 19.1 同步更正。
- 第 20 章：最优反向均值命题中的 KL 最小值改为 $\frac D2(\sigma_t^2/\beta_t-1+\ln(\beta_t/\sigma_t^2))$，不再误写为 0。
- 其余原文疑点均以紧随的 `remark`（“原文问题说明”）记录，未静默改结论。

## 5. 插件更新（v1.1.0）

- `plugin/skills/pdf-latex-rebuild/references/spec-v14.md`、`SKILL.md`、`src/v14-complete.txt`：新增 §3.11 严格性规范；废止可见“重构新增”标记；习题只保留题面；§3.6/3.9/3.10 相应修订。
- `plugin/skills/pdf-latex-rebuild/OPERATING-CONTRACT.md`：SUPPLEMENT 不再要求可见标记。
- `plugin/skills/pdf-latex-rebuild/references/LEDGERS.md`：`conditions.explicit_or_inherited` 增加 `well-definedness` 值。
- `plugin/assets/check.py`、`plugin/engine/check.py`：新增 RIG-001..RIG-012，纳入 gate 的 ERROR 统计；requirements 新增 R14-01..R14-08；R3-6B/6G/7E/8D/9A/9B/10A 同步修订。
- `plugin/package.json`、`plugin/assets/BUILD_INFO.json`：版本 1.1.0 与哈希刷新。
- `README.md`：补充严格陈述条目，删除“习题必须写 solution”的旧表述。

## 6. 复现

```bash
cd "/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning"
python3 audit-revision/run_rigor_probe.py          # 全书 RIG 汇总
python3 audit-revision/check_file.py <file>        # 单文件
python3 audit-revision/report_stats.py             # 763/721 统计
latexmk -g -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

构建日志：`audit-revision/build-final2.log`；原始源码备份：`audit-revision/original-tex-backup.zip`。
