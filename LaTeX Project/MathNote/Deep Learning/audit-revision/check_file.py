#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the plugin's RIG checks on one .tex file of the Deep Learning project.

Usage: python3 audit-revision/check_file.py contents/Chapter-01/section-02.tex
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning')
CHECK = Path('/mnt/c/Users/32063/Desktop/PDF-LaTeX重构插件/plugin/assets/check.py')


def load_check():
    spec = importlib.util.spec_from_file_location('dsh_check', CHECK)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['dsh_check'] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    if len(sys.argv) != 2:
        raise SystemExit('usage: check_file.py <relative-tex-path>')
    rel = sys.argv[1].replace('\\', '/')
    target = ROOT / rel
    if not target.is_file():
        raise SystemExit('not a file: %s' % target)
    check = load_check()
    cfg = dict(check.DEFAULT_CONFIG)
    scan = check.scan_project(ROOT, cfg)
    findings = []
    check.check_rigor(scan, findings)
    rows = [f for f in findings if f.get('file') == rel]
    if not rows:
        print('OK: no RIG findings in', rel)
        return
    by_sev = {}
    for f in rows:
        by_sev.setdefault(f['severity'], 0)
        by_sev[f['severity']] += 1
    print('%s: %d findings %s' % (rel, len(rows), by_sev))
    for f in rows:
        print('%-7s %-5s line %-5s %s' % (f['rule'], f['severity'], f['line'], f['message']))


if __name__ == '__main__':
    main()
