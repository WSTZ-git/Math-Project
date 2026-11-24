#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compute revision statistics by comparing the pre-revision backup with current sources."""
import re
import zipfile
from pathlib import Path

ROOT = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning')
ZIP = ROOT / 'audit-revision' / 'original-tex-backup.zip'
ENVS = ('definition', 'theorem', 'proposition', 'lemma', 'corollary')
PAT = re.compile(r'\\begin\{(%s)\}(?:\[[^\]]*\])?(.*?)\\end\{\1\}' % '|'.join(ENVS), re.S)
LAB = re.compile(r'\\label\{([^}]*)\}')


def parse(text):
    out = {}
    for m in PAT.finditer(text):
        body = m.group(2)
        lm = LAB.search(body)
        key = lm.group(1) if lm else '<no-label>'
        out[key] = (m.group(1), body)
    return out


def main():
    orig = {}
    with zipfile.ZipFile(ZIP) as z:
        for name in z.namelist():
            if name.endswith('.tex'):
                orig.update(parse(z.read(name).decode('utf-8')))
    cur = {}
    for p in (ROOT / 'contents').rglob('*.tex'):
        cur.update(parse(p.read_text(encoding='utf-8')))
    changed = [k for k in cur if k in orig and cur[k][1] != orig[k][1]]
    added = [k for k in cur if k not in orig]
    removed = [k for k in orig if k not in cur]
    print('original statements', len(orig))
    print('current statements ', len(cur))
    print('changed bodies     ', len(changed))
    print('added labels       ', len(added), added[:10])
    print('removed labels     ', len(removed), removed[:10])
    # marker counts in current sources
    text = '\n'.join(p.read_text(encoding='utf-8') for p in (ROOT / 'contents').rglob('*.tex'))
    print('重构新增 in sources', text.count('重构新增'))
    print('solution envs      ', text.count('\\begin{solution}'))


if __name__ == '__main__':
    main()
