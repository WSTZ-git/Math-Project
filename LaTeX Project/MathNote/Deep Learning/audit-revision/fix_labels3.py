from pathlib import Path
p = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/Chapter-18/section-01.tex')
t = p.read_text(encoding='utf-8')
needle = '\\label{align:ch18-耦合逆恒等}'
first = t.find(needle)
second = t.find(needle, first + 1)
if second == -1:
    print('no duplicate')
else:
    t = t[:second] + t[second + len(needle):]
    p.write_text(t, encoding='utf-8')
    print('removed second')
