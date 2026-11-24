#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove every visible/comment occurrence of the reconstruction marker.

Policy (user 2026-11): the PDF and the sources must not contain
“（重构新增）” or “重构新增”; supplement identity lives only in
`% SUPPLEMENT:` comments and the audit ledger.
"""
from pathlib import Path

ROOT = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning')
VARIANTS = [
    ('（重构新增：原文问题说明）', '（原文问题说明）'),
    ('（重构新增，原文问题说明）', '（原文问题说明）'),
    ('（重构新增）', ''),
    ('（重构新增', ''),
    ('重构新增', ''),
]

changed = 0
removed = 0
for p in sorted(ROOT.rglob('*.tex')):
    if 'audit-revision' in p.parts:
        continue
    t = p.read_text(encoding='utf-8')
    n = t.count('重构新增')
    if not n:
        continue
    for old, new in VARIANTS:
        t = t.replace(old, new)
    p.write_text(t, encoding='utf-8')
    changed += 1
    removed += n
    print('cleaned', p.relative_to(ROOT), n)

print('files', changed, 'removed', removed, 'remaining',
      sum(p.read_text(encoding='utf-8').count('重构新增')
          for p in ROOT.rglob('*.tex') if 'audit-revision' not in p.parts))
