#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Standalone probe: run the plugin's RIG checks on the Deep Learning project.

The project currently has no texbook.json, so the probe uses DEFAULT_CONFIG
and only exercises scan_project + check_rigor (read-only).
"""
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning')
CHECK = Path('/mnt/c/Users/32063/Desktop/PDF-LaTeX重构插件/plugin/assets/check.py')

spec = importlib.util.spec_from_file_location('dsh_check', CHECK)
check = importlib.util.module_from_spec(spec)
sys.modules['dsh_check'] = check
spec.loader.exec_module(check)

cfg = dict(check.DEFAULT_CONFIG)
scan = check.scan_project(ROOT, cfg)
findings = []
check.check_rigor(scan, findings)

by_rule = Counter(f['rule'] for f in findings)
by_sev = Counter(f['severity'] for f in findings)
print('TOTAL', len(findings), dict(by_sev))
print('BY RULE', dict(sorted(by_rule.items())))
print()
print('TOP FILES')
c = Counter(f['file'] for f in findings)
for f, n in c.most_common(30):
    print(n, f)
print()
for rule in sorted(by_rule):
    print('====', rule, by_rule[rule])
    for f in findings:
        if f['rule'] == rule:
            print(f["file"], f["line"], f["message"][:160])
            break

out = ROOT / 'audit-revision' / 'rigor-findings.json'
out.write_text(json.dumps(findings, ensure_ascii=False, indent=1), encoding='utf-8')
print('wrote', out)
