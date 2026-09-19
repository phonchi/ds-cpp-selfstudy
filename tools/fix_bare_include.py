#!/usr/bin/env python3
"""把講義範例卡裡的裸檔名 #include "X.hpp" 改成 "pythonds3/cppds/X.hpp"。

講義 notebook 與 kernel 都只認 pythonds3/cppds/ 前綴；裸檔名學生照抄會 No such file。
只改 name 在課程標頭目錄裡存在的檔案；冪等（改過的帶了前綴就不再命中）。

課程標頭目錄預設是 ~/ds_cpp/Slides/pythonds3/cppds，可用環境變數 DSCPP_HEADERS 覆寫。
找不到目錄時分兩種情況：
  * DSCPP_HEADERS 有設但指到不存在的路徑 → 視為設定錯誤，報錯結束（exit 1）。
  * 沒設環境變數、預設目錄也不在（例如別台機器剛 clone）→ 印警告到 stderr、
    略過本步驟、正常結束（exit 0），不讓重生鏈
    （enrich_*.py → fix_bare_include.py → shuffle_quiz.py → apply_zh.py）整條斷掉。
"""
import glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENV_VAR = 'DSCPP_HEADERS'
DEFAULT_HDR_DIR = '~/ds_cpp/Slides/pythonds3/cppds'

def hdr_dir():
    """回傳 (課程標頭目錄, 是否由環境變數指定)。"""
    env = os.environ.get(ENV_VAR)
    if env:
        return os.path.expanduser(env), True
    return os.path.expanduser(DEFAULT_HDR_DIR), False

def known_headers(dirs):
    names = set()
    for d in dirs:
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
    d, from_env = hdr_dir()
    if not os.path.isdir(d):
        if from_env:
            sys.exit(f'{ENV_VAR} 指到的課程標頭目錄不存在：{d}')
        print(f'警告：找不到課程標頭目錄 {d}，略過裸檔名 include 修補'
              f'（需要時用 {ENV_VAR} 指定目錄）', file=sys.stderr)
        return
    names = known_headers([d])
    if not names:
        sys.exit(f'課程標頭目錄裡沒有任何 .hpp，無法判斷哪些裸檔名合法：{d}')
    total = 0
    for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        n = fix(f, names)
        if n:
            print(f'{os.path.basename(f)}: {n}')
            total += n
    print(f'共改 {total} 處')

if __name__ == '__main__':
    main()
