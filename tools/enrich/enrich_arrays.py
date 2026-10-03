#!/usr/bin/env python3
"""Rebuild Chapter 3 sections and mapping assets only; repeatable, no external writes."""
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
CONTENT = Path(__file__).resolve().parent / 'content'
sys.path.insert(0, str(CONTENT))
from arrays_content import build

def replace_once(text, pattern, replacement):
    text, count = re.subn(pattern, lambda _: replacement, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f'Missing expected Chapter 3 boundary: {pattern}')
    return text

def main():
    page = ROOT / 'arrays.html'
    text = page.read_text()
    for sid, section in build().items():
        text = replace_once(text, rf'<section id="{sid}">.*?</section>', section)
    css = '<style id="arrays-depth-style">\n' + (CONTENT/'arrays.css').read_text() + '</style>'
    js = '<script id="arrays-mapping-script">\n' + (CONTENT/'arrays_mapping.js').read_text() + '</script>'
    if 'id="arrays-depth-style"' in text:
        text = replace_once(text, r'<style id="arrays-depth-style">.*?</style>', css)
    else:
        text = text.replace('</head>', css+'\n</head>', 1)
    if 'id="arrays-mapping-script"' in text:
        text = replace_once(text, r'<script id="arrays-mapping-script">.*?</script>', js)
    else:
        text = text.replace('</body>', js+'\n</body>', 1)
    # Small repairs to the preserved interaction code and exercise feedback.
    text = text.replace('…真正的物件散落在 heap 各處', '目標物件在其他位置，不一定在 heap')
    text = text.replace('referential：格子裡是指標，每次取值都要「跳」到 heap：位置分散，cache 常 miss。', 'referential：格子裡存連結，取值多一層間接存取。此圖假設指標 8 bytes；目標是否集中會影響快取。')
    text = text.replace('compact：值直接住在連續格子。走訪 = 順順地掃一條記憶體。', 'compact：值直接住在連續格子。此圖假設 int 佔 4 bytes，走訪可依序掃過。')
    text = text.replace('。攤平索引 0,4,8,1,5,9,…每步跳 4 格：大矩陣時 cache miss 連發。', '。攤平索引 0,4,8,1,5,9,…沿欄跨列跳 4 格，換欄時回到前方；可能較不利於快取。')
    text = text.replace("$('spStore').innerHTML = `<strong>COO</strong>：${coo}<br><strong>DOK</strong>：${dok}`;", "const chain = entries.map(e => `(${e.r},${e.c},${e.v})`).join(' → ');\n  $('spStore').innerHTML = `<strong>COO</strong>：${coo}<br><strong>DOK</strong>：${dok}<br><strong>Linear list</strong>：head → ${chain ? chain + ' → ' : ''}nullptr`;")
    text = text.replace('隨機讀寫 O(log nnz) 或 O(1)；COO 要線性掃、密陣列 10¹⁰ 格根本放不下（40GB+）。', 'std::map 查找 O(log(nnz+1))；unordered_map 平均 O(1)。未排序 COO 需線性掃描；密矩陣需要 Rows×Cols 格。')
    text = text.replace('COO 隨機查 (r,c) 要掃整條列表：它是「建構/匯出」格式。', '未排序 COO 需線性掃描；排序後雖可二分查詢，插入仍可能搬移後續項目。')
    from content.teaching_copy import polish_preserved
    text = polish_preserved("arrays", text)
    page.write_text(text)
    print('Rebuilt arrays.html sections and mapping assets')

if __name__ == '__main__': main()
