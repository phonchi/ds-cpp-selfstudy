#!/usr/bin/env python3
"""全站結構檢查：錨點、頁面連結、注入腳本的前置條件。無外部相依。"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errs, warns = [], []

pages = sorted(ROOT.glob("*.html"))
names = {p.name for p in pages}

for p in pages:
    s = p.read_text()
    tag = p.name

    # 注入腳本的前置條件
    for pat, want in [(r"</head>", 1), (r'<div class="container">', 1), (r"</body>", 1)]:
        n = len(re.findall(pat, s))
        if n != want:
            errs.append(f"{tag}: `{pat}` 出現 {n} 次（應為 {want}）")

    ids = set(re.findall(r'\bid="([^"]+)"', s))

    # 頁內錨點
    for a in set(re.findall(r'href="#([^"]+)"', s)):
        if a != "top" and a not in ids:
            errs.append(f"{tag}: 錨點 #{a} 找不到對應 id")

    # float-nav 的 data-target 必須等於 href
    for href, dt in re.findall(r'<a href="#([^"]+)" data-target="([^"]+)"', s):
        if href != dt:
            errs.append(f"{tag}: float-nav href=#{href} 與 data-target={dt} 不一致")

    # 站內頁面連結
    for h in set(re.findall(r'href="([^"#:]+\.html)(?:#[^"]*)?"', s)):
        if h not in names:
            errs.append(f"{tag}: 連到不存在的頁面 {h}")

    # float-nav / TOC 項目數應一致
    nav = re.search(r'<nav class="float-nav".*?</nav>', s, re.S)
    toc = re.search(r'<div class="toc">.*?</div>\s*</div>', s, re.S)
    if nav and toc:
        n_nav = len(re.findall(r'data-target="', nav.group(0)))
        n_toc = len(re.findall(r'href="#', toc.group(0)))
        if n_nav != n_toc:
            warns.append(f"{tag}: float-nav {n_nav} 項 vs TOC {n_toc} 項")

    # 逃逸檢查：data-fb 與 FLASHCARDS 內不該出現未 mangle 的字樣
    for m in re.findall(r'data-fb="[^"]*"', s):
        for bad in ("self.", "None", "elif", "def ", "print("):
            if bad in m:
                warns.append(f"{tag}: data-fb 含未逃逸的 `{bad}`")
                break
    fc = re.search(r"const FLASHCARDS = \[.*?\];", s, re.S)
    if fc:
        for bad in ("self.", "None", "elif", "def ", "print("):
            if bad in fc.group(0):
                warns.append(f"{tag}: FLASHCARDS 含未逃逸的 `{bad}`")
                break

print(f"檢查 {len(pages)} 頁")
for w in warns: print("WARN", w)
for e in errs: print("FAIL", e)
print(f"\n{len(errs)} 個錯誤 / {len(warns)} 個警告")
sys.exit(1 if errs else 0)
