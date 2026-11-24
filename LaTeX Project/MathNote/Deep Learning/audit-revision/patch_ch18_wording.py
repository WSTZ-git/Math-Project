from pathlib import Path
p = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/Chapter-18/section-02.tex')
t = p.read_text(encoding='utf-8')
t = t.replace('它们可以并行计算', '它们可并行计算')
t = t.replace('因此也可以高效计算', '因此也可高效计算')
t = t.replace('后可以并行。', '后可并行。')
p.write_text(t, encoding='utf-8')
print('done')
