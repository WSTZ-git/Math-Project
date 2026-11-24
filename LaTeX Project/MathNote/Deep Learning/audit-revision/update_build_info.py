#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refresh plugin package/BUILD_INFO metadata after the 2026-11 policy update."""
import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

P = Path('/mnt/c/Users/32063/Desktop/PDF-LaTeX重构插件')
PKG = P / 'plugin' / 'package.json'
INFO = P / 'plugin' / 'assets' / 'BUILD_INFO.json'


def sha(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def main():
    pkg = json.loads(PKG.read_text(encoding='utf-8'))
    pkg['version'] = '1.1.0'
    PKG.write_text(json.dumps(pkg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    skill = P / 'plugin/skills/pdf-latex-rebuild/SKILL.md'
    info = json.loads(INFO.read_text(encoding='utf-8'))
    info['engine_version'] = '1.1.0'
    info['built_at'] = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%dT%H:%M:%S%z')
    info['engine_sha256'] = sha(P / 'engine/check.py')
    info['skill_sha256'] = sha(skill)
    info['skill_chars'] = len(skill.read_text(encoding='utf-8'))
    info['spec_v14_sha256'] = sha(P / 'plugin/skills/pdf-latex-rebuild/references/spec-v14.md')
    info['spec_v13_sha256'] = sha(P / 'plugin/skills/pdf-latex-rebuild/references/spec-v13.md')
    info['ledgers_sha256'] = sha(P / 'plugin/skills/pdf-latex-rebuild/references/LEDGERS.md')
    INFO.write_text(json.dumps(info, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
