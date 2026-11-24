#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract theorem-like environments from the Deep Learning LaTeX project.

Outputs audit-revision/environments.json and a human-readable summary.
Read-only: does not modify project sources.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX_FILES = sorted(p for p in ROOT.rglob('*.tex') if 'audit-revision' not in p.parts)

TARGET = {
    'definition', 'definition*', 'theorem', 'theorem*', 'proposition',
    'proposition*', 'lemma', 'lemma*', 'corollary', 'corollary*',
    'axiom', 'axiom*', 'postulate', 'postulate*', 'proof', 'solution',
    'remark', 'note', 'example', 'examples', 'exercise',
}

BEGIN_RE = re.compile(r'\\begin\{(?P<env>[A-Za-z@*]+)\}(?:\[(?P<opt>[^\]]*)\])?')
END_RE = re.compile(r'\\end\{(?P<env>[A-Za-z@*]+)\}')
LABEL_RE = re.compile(r'\\label\{(?P<label>[^}]*)\}')

COLLOQUIAL = ['我们', '可以', '其实', '显然', '注意', '这就', '也就是说', '换句话说',
              '不过', '当然', '例如', '直观', '不妨', '容易', '想想', '来看',
              '有趣', '重要', '有趣的是', '值得一提的是']
ASSUMPTION = ['设', '假设', '若', '如果', '其中', '给定', '对任意', '存在', '使得',
              '满足', '定义', '称']


def line_of(text: str, pos: int) -> int:
    return text.count('\n', 0, pos) + 1


def parse_file(path: Path):
    text = path.read_text(encoding='utf-8', errors='replace')
    stack = []
    out = []
    for m in BEGIN_RE.finditer(text):
        env = m.group('env')
        if env not in TARGET:
            continue
        stack.append((env, m.start(), m.end(), m.group('opt')))
    # A separate pass with a proper stack for all environments, to find matching ends
    stack_all = []
    matches = []
    token_re = re.compile(r'\\(begin|end)\{([A-Za-z@*]+)\}(?:\[([^\]]*)\])?')
    for m in token_re.finditer(text):
        kind, env, opt = m.group(1), m.group(2), m.group(3)
        if kind == 'begin':
            stack_all.append((env, m.start(), m.end(), opt))
        else:
            # pop until matching env
            for i in range(len(stack_all) - 1, -1, -1):
                if stack_all[i][0] == env:
                    b = stack_all.pop(i)
                    # any unclosed inner envs are malformed; drop them
                    del stack_all[i:]
                    matches.append((env, b[1], b[2], b[3], m.start(), m.end()))
                    break
    for env, bstart, bend, opt, estart, eend in matches:
        if env not in TARGET:
            continue
        body_start = bend
        body = text[body_start:estart]
        label = ''
        lm = LABEL_RE.search(body)
        if lm:
            label = lm.group('label')
        # strip label command for length metric
        plain = LABEL_RE.sub('', body)
        plain = re.sub(r'%.*', '', plain)
        metrics = {
            'chars': len(plain.strip()),
            'has_assumption_words': any(w in plain for w in ASSUMPTION),
            'colloquial_hits': [w for w in COLLOQUIAL if w in plain],
            'has_formula': bool(re.search(r'\$|\\begin\{align', plain)),
            'has_matrix': '矩阵' in plain,
            'has_dimension': bool(re.search(r'\d\s*\\times\s*\d|维|阶', plain)),
        }
        before = text[max(0, bstart - 500):bstart]
        after = text[eend:eend + 500]
        out.append({
            'file': str(path.relative_to(ROOT)),
            'env': env,
            'opt': opt or '',
            'label': label,
            'begin_line': line_of(text, bstart),
            'end_line': line_of(text, estart),
            'body': body,
            'before': before,
            'after': after,
            'metrics': metrics,
        })
    return out


def main():
    all_envs = []
    for p in TEX_FILES:
        all_envs.extend(parse_file(p))
    all_envs.sort(key=lambda e: (e['file'], e['begin_line']))
    outdir = ROOT / 'audit-revision'
    outdir.mkdir(exist_ok=True)
    (outdir / 'environments.json').write_text(
        json.dumps(all_envs, ensure_ascii=False, indent=1), encoding='utf-8')
    # summary
    from collections import Counter, defaultdict
    by_env = Counter(e['env'] for e in all_envs)
    by_file = defaultdict(lambda: Counter())
    for e in all_envs:
        by_file[e['file']][e['env']] += 1
    lines = ['# Environment inventory', '']
    lines.append('Total: %d' % len(all_envs))
    lines.append('')
    for env, n in by_env.most_common():
        lines.append(f'- {env}: {n}')
    lines.append('')
    lines.append('## Per file')
    for f in sorted(by_file):
        counts = ', '.join(f'{k}={v}' for k, v in sorted(by_file[f].items()))
        lines.append(f'- {f}: {counts}')
    lines.append('')
    lines.append('## Weak candidates (short bodies or no assumption words)')
    for e in all_envs:
        if e['env'] in {'definition', 'theorem', 'proposition', 'lemma', 'corollary'}:
            if e['metrics']['chars'] < 120 or not e['metrics']['has_assumption_words']:
                lines.append(f"- {e['file']}:{e['begin_line']} [{e['env']}] {e['label']} chars={e['metrics']['chars']} assumption={e['metrics']['has_assumption_words']}")
    (outdir / 'inventory.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('wrote', outdir / 'environments.json')
    print('total', len(all_envs))
    print(dict(by_env))


if __name__ == '__main__':
    main()
