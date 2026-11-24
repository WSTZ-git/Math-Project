from pathlib import Path
p = Path('/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning/contents/chapter-02.tex')
t = p.read_text(encoding='utf-8')
t = t.replace('其预测结果所携带的不确定性可以划分为两类', '其预测结果所携带的不确定性划分为两类')
t = t.replace('则称其为\\textbf{认知不确定性}', '则称为\\textbf{认知不确定性}')
t = t.replace('则称其为\\textbf{偶然不确定性}', '则称为\\textbf{偶然不确定性}')
p.write_text(t, encoding='utf-8')
print('done')
