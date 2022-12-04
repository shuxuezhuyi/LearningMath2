#!/usr/bin/python3
# 用 preamble-for-plasTeX.tex 的内容替换掉各 tex 文档的导言(preamble)部分
import os
from pathlib import Path
from pprint import pprint

here = os.path.dirname(os.path.realpath(__file__))
preamble_path = here + '/preamble-for-plasTeX.tex'
with open(preamble_path, 'r', encoding='utf-8') as preamble_file:
    new_preamble = preamble_file.readlines()
new_preamble.append('\n') # 追加空行, 免得下边加的 \begin{document} 被加到行尾

p = Path(here) # 在这个文件夹里面的所有 lyx 文档对应的 tex 文档都会被处理
for lyx_path in list(p.glob('**/*.lyx')):
    str_path = str(lyx_path)
    if here + r'/temp/' in str_path: continue
    if here + r'/template/' in str_path: continue
    if here + r'/Other/MathMacros/' in str_path: continue
    if here + r'/LearningMath.lyx' in str_path: continue
    tex_path = str_path.replace('.lyx', '.tex')
    write_lines = new_preamble
    with open(tex_path, 'r', encoding='utf-8') as tex_file:
        lines = tex_file.readlines()
    with open(tex_path, 'w', encoding='utf-8') as tex_file:
        write_sign = False
        for line in lines:
            if not write_sign:
                if r'\begin{document}' in line: 
                    write_sign = True
                    write_lines.append(line)
                continue
            else: write_lines.append(line.replace(r'\checkmark ', '✓')) # 在这里查找替换也是拓展 plasTeX 功能的方法(大概)
        if write_sign == False: # LyX 子文档被导出为 tex 文档时并没有 preamble, 就不用修改 preamble 了
            write_lines = []
            for line in lines: write_lines.append(line.replace(r'\checkmark ', '✓')) # 在这里查找替换也是拓展 plasTeX 功能的方法(大概)
        tex_file.writelines(write_lines)