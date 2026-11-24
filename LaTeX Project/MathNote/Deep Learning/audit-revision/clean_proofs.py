#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clean colloquial/meta narration inside proof and solution bodies.

Only proof/solution bodies are touched; prose, statements, labels and equations
are left unchanged. Applied to files that are not currently being edited by a
chapter agent.
"""
import re
import sys
from pathlib import Path

ROOT = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning')

TARGETS = [
    'contents/Chapter-01/section-01.tex',
    'contents/Chapter-01/section-02.tex',
    'contents/Chapter-01/section-03.tex',
    'contents/Chapter-02/section-01.tex',
    'contents/Chapter-02/section-02.tex',
    'contents/Chapter-02/section-03.tex',
    'contents/Chapter-02/section-04.tex',
    'contents/Chapter-03/section-01.tex',
    'contents/Chapter-03/section-02.tex',
    'contents/Chapter-03/section-03.tex',
    'contents/appendix-A.tex',
]

ENV_RE = re.compile(r'(\\begin\{(proof|solution)\})(.*?)(\\end\{\2\})', re.S)


def clean_body(body: str) -> str:
    # Remove whole meta sentences beginning with 原书/原文.
    body = re.sub(r'(?:原书|原文)[^。]{0,160}?。', '', body)
    # Remove common supplement lead-ins.
    body = body.replace('补全如下：', '')
    body = body.replace('补全细节：', '')
    body = body.replace('下面补全双向验证。', '')
    body = body.replace('下面补全。', '')
    body = body.replace('这里补全思路。', '')
    body = body.replace('这里补全。', '')
    # Colloquial connectors inside proofs.
    body = body.replace('这就', '由此')
    body = body.replace('也就是说', '即')
    body = body.replace('换句话说', '等价地')
    body = body.replace('其实', '')
    body = body.replace('我们', '')
    # Tidy spaces/punctuation left behind.
    body = re.sub(r'[ \t]{2,}', ' ', body)
    body = re.sub(r'。\s*。', '。', body)
    body = re.sub(r'：\s*：', '：', body)
    body = re.sub(r'\n\s*\n\s*\n+', '\n\n', body)
    return body


def main():
    dry = '--dry' in sys.argv
    for rel in TARGETS:
        p = ROOT / rel
        t = p.read_text(encoding='utf-8')
        cnt = [0]

        def repl(m):
            new = clean_body(m.group(3))
            if new != m.group(3):
                cnt[0] += 1
            return m.group(1) + new + m.group(4)

        t2 = ENV_RE.sub(repl, t)
        if cnt[0]:
            print(('would clean' if dry else 'cleaned'), rel, cnt[0])
            if not dry:
                p.write_text(t2, encoding='utf-8')


if __name__ == '__main__':
    main()
