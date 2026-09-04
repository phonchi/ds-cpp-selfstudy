#!/usr/bin/env python3
"""把講義範例卡裡的裸檔名 #include "X.hpp" 改成 "pythonds3/cppds/X.hpp"。

講義 notebook 與 kernel 都只認 pythonds3/cppds/ 前綴；裸檔名學生照抄會 No such file。
只改 name 在課程標頭目錄裡存在的檔案；冪等。
"""
import glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HDR_DIRS = [os.path.expanduser('~/ds_cpp/Slides/pythonds3/cppds')]

def known_headers():
    names = set()
    for d in HDR_DIRS:
        if os.path.isdir(d):
            names |= {f for f in os.listdir(d) if f.endswith('.hpp')}
    return names

PAT = re.compile(r'(#</span><span class="kw">include</span> <span class="kw">)"([a-z_]+\.hpp)"')

def fix(path, names, write=True):
    s = open(path, encoding='utf-8').read()
    def rep(m):
        return m.group(0) if m.group(2) not in names else f'{m.group(1)}"pythonds3/cppds/{m.group(2)}"'
    new, n = PAT.subn(rep, s)
    if n and write and new != s:
        open(path, 'w', encoding='utf-8').write(new)
    return sum(1 for m in PAT.finditer(s) if m.group(2) in names)

def main():
    names = known_headers()
    if not names:
        sys.exit('找不到課程標頭目錄，無法判斷哪些裸檔名合法')
    total = 0
    for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        n = fix(f, names)
        if n:
            print(f'{os.path.basename(f)}: {n}')
            total += n
    print(f'共改 {total} 處')

if __name__ == '__main__':
    main()
