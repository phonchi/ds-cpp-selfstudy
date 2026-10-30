#!/usr/bin/env python3
"""3D 群島 island/index.html 的靜態檢查。無外部相依。

產物同步、21 頁齊全、相對連結與代表圖 id、外部資源釘版＋SRI、學生可見文字的用語與縮寫。
--net 時重新下載 Three.js 模組，比對 sha384 與 importmap 的 integrity。

用法：python3 tools/check_island.py [--net]
"""
import base64
import hashlib
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_island as I  # noqa: E402

ROOT = I.ROOT
F = ROOT / "island" / "index.html"
fails = []


def fail(msg):
    fails.append(msg)


# 第一次出現必須寫全名：縮寫 → 第一次出現時前面要有的英文全名
ACRONYMS = {"BFS": "Breadth-First Search", "DFS": "Depth-First Search", "BST": "Binary Search Tree", "DOK": "Dictionary of Keys"}
# 學生頁不放製作歷程與工作紀錄；台灣用語
FORBIDDEN = ["本次更新", "已同步", "與新版講義相同", "中位數", "量測", "重現命令", "視頻", "軟件", "硬件", "數據結構", "鏈表", "隊列", "棧", "樣板", "晶片", "匯流排", "通電", "藍圖"]


class Text(HTMLParser):
    """只留學生看得到的文字：略過 style、module script 與 head"""
    def __init__(self):
        super().__init__()
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "head") or (tag == "script" and dict(attrs).get("type") != "application/json"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("style", "head", "script") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def main():
    net = "--net" in sys.argv
    if not F.exists():
        raise SystemExit("尚未產生，先跑 python3 tools/build_island.py")
    src = F.read_text(encoding="utf-8")
    try:
        built = I.build()
    except SystemExit as e:
        raise SystemExit(str(e))
    if built != src:
        fail("產物與產生器不一致（手改了，或改了 island_meta／template 後沒重跑 build_island.py）")

    m = re.search(r'<script type="application/json" id="island-data">\n(.*?)\n</script>', src, re.S)
    assert m, "找不到 island-data"
    data = json.loads(m.group(1).replace("<\\/", "</"))
    stems = [p["stem"] for p in data["pages"]]
    if len(stems) != 21:
        fail(f"單元數 {len(stems)} ≠ 21")
    links = re.findall(r'class="isl-link" href="([^"]+)"', src)
    if [f"../{s}.html" for s in stems] != links:
        fail("列表入口與 PAGES 不一致")
    for href in set(re.findall(r'href="(\.\./[^"#]+)', src)):
        if not (ROOT / "island" / href).resolve().exists():
            fail(f"連結指向不存在的 {href}")
    # 代表圖：檔案、深連結 id，且 island/figs 只放 FIGS 列出的章節
    figs = {f.stem for f in (ROOT / "island" / "figs").glob("*")}
    if figs != set(I.M.FIGS):
        fail(f"island/figs 與 FIGS 不一致：多 {sorted(figs - set(I.M.FIGS))}、缺 {sorted(set(I.M.FIGS) - figs)}")
    for p in data["pages"]:
        fg = p.get("fig")
        if fg:
            page, fid = fg["href"].split("#")
            if f'id="{fid}"' not in (ROOT / "island" / page).read_text(encoding="utf-8"):
                fail(f"{p['stem']} 的深連結 #{fid} 不存在")
    # 外部資源只能是 Three.js（釘版）與 Google Fonts
    for u in set(re.findall(r'https?://[^\s"\'<>)]+', src)):
        if not (u.startswith(I._CDN) or u.startswith("https://fonts.g") or u.startswith("http://www.w3.org")):
            fail(f"未允許的外部資源 {u}")
    m = re.search(r'<script type="importmap">\n(.*?)\n</script>', src, re.S)
    assert m, "找不到 importmap"
    imap = json.loads(m.group(1))
    if imap["integrity"] != I.THREE_SRI:
        fail("importmap 的 integrity 與 build_island.THREE_SRI 不一致")
    for spec in ("three",):
        if imap["imports"][spec] not in imap["integrity"]:
            fail(f"importmap 的 {spec} 缺 integrity")
    for frm, to in I.CORE_REMAP.items():
        if imap["imports"].get(frm) != to or to not in imap["integrity"]:
            fail(f"{frm} 沒有對應到有 integrity 的 {to}")
    if net:
        for url, want in I.THREE_SRI.items():
            try:
                body = urllib.request.urlopen(url, timeout=30).read()
            except Exception as e:  # noqa: BLE001
                fail(f"無法下載以驗證 SRI：{url}：{e}")
                continue
            got = "sha384-" + base64.b64encode(hashlib.sha384(body).digest()).decode()
            if got != want:
                fail(f"SRI 不符：{url}（CDN 實際為 {got}）")
    # 學生可見文字
    tp = Text()
    tp.feed(src)
    text = "\n".join(tp.out)
    for w in FORBIDDEN:
        if w in text:
            fail(f"用語：學生可見文字出現「{w}」")
    for ab, full in ACRONYMS.items():
        i = re.search(rf"\b{ab}\b", text)
        if i and full not in text[max(0, i.start() - 60):i.end()]:
            fail(f"縮寫 {ab} 第一次出現時沒有拼出全名（{full}）")
    # 首頁入口
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    if 'href="island/"' not in home:
        fail("首頁沒有群島入口")
    if fails:
        print("\n".join("✗ " + f for f in fails))
        sys.exit(1)
    print(f"check_island：通過（{len(stems)} 頁、{len(figs)} 張代表圖、SRI {'已對 CDN 比對' if net else '未連網比對'}）")


if __name__ == "__main__":
    main()
