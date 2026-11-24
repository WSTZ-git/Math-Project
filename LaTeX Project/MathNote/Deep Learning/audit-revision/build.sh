#!/bin/bash
# Start a detached full build of the Deep Learning book.
cd "/home/sk2063/LaTeX Project/Math/MathNote/Deep Learning" || exit 1
rm -f audit-revision/build-full.log
nohup latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex \
  > audit-revision/build-full.log 2>&1 < /dev/null &
echo "started $!"
