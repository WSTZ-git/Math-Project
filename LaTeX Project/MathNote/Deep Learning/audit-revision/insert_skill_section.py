#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insert the new 3.11 rigor section into SKILL.md (which embeds the spec)."""
import sys
from pathlib import Path

HERE = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/audit-revision')
sys.path.insert(0, str(HERE))
import update_plugin_spec as u

skill = u.SKILL
t = skill.read_text(encoding='utf-8')
marker = '【4. 标签强制规范'
if '【3.11 数学陈述的严格性' not in t:
    if marker not in t:
        raise SystemExit('anchor not found in SKILL.md')
    t = t.replace(marker, u.NEW_SECTION + marker, 1)
    skill.write_text(t, encoding='utf-8')
    print('inserted 3.11 into', skill)
else:
    print('already present in', skill)

# Repair the accidental line join in the spec copies.
for p in u.SPEC_FILES + [skill]:
    t = p.read_text(encoding='utf-8')
    old = '   supplements 台账登记身份并验证，但不在 PDF 标注“重构新增”。不要随意添加无关背景或新的研究分支。动机可以先于对应对象的证明，'
    new = ('   supplements 台账登记身份并验证，但不在 PDF 标注“重构新增”。\n'
           '   不要随意添加无关背景或新的研究分支。动机可以先于对应对象的证明，')
    if old in t:
        t = t.replace(old, new)
        p.write_text(t, encoding='utf-8')
        print('repaired', p)
