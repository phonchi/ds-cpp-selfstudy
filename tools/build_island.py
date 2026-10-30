#!/usr/bin/env python3
"""由 tools/island_meta.py 產生 island/index.html（3D 資料結構矽晶群島）。冪等。

頁面是「DOM 優先」：三區的章節列表由這裡直接輸出成語意 HTML，沒有 JS、CDN 失效或 WebGL 不可用時
就是一張可點的 2D 地圖；WebGL 可用時，同一份列表變成 3D 場景旁的快速列表。
Three.js 以 importmap 釘版載入，integrity 涵蓋每一個會被抓的模組；three.module.min.js 內部 import 的
未壓縮 three.core.js 以 importmap 重新對應到 three.core.min.js。
"""
import html
import json
import re
import struct
import sys
import urllib.parse
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import island_meta as M  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "tools" / "template"
OUT = ROOT / "island" / "index.html"
FIG_DIR = ROOT / "island" / "figs"
BY = {p["stem"]: p for p in M.PAGES}

THREE_VER = "0.186.1"
_CDN = f"https://cdn.jsdelivr.net/npm/three@{THREE_VER}"
THREE_MAIN = f"{_CDN}/build/three.module.min.js"
THREE_ADDONS = f"{_CDN}/examples/jsm/"
# 升版時：下載這三個檔，以 `openssl dgst -sha384 -binary f | openssl base64 -A` 重算。
THREE_SRI = {
    THREE_MAIN: "sha384-EU5UWigB3OuXjAXooUegndJSqYber3YSJHDoMZs6rV96yY/ol/B4W8logw4CKWkA",
    f"{_CDN}/build/three.core.min.js": "sha384-ktZslgpl0L71WZcQ5wKV96Z04i9QSjtmiU/kYpjDQSfJ5NJ8B79qDF63oNTbQySl",
    f"{THREE_ADDONS}controls/OrbitControls.js": "sha384-LSqANrugPGTgf0eYsQTloqKWy926dOOXo2iZ9y6wLMIDEQoU9AaCLJF1Vcc7oJXr",
}
CORE_REMAP = {f"{_CDN}/build/three.core.js": f"{_CDN}/build/three.core.min.js"}

# 網頁字型只保留頂列標題：用 text= 只下載這幾個字；其餘一律用系統字型。
TITLE = "資料結構矽晶群島"
FONTS = ("https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@900&display=swap&text="
         + urllib.parse.quote(TITLE))

# 面板上阿迭的頭像：-> 形頭盔的小機器人，單眼（與 island-scene.js 的 3D 嚮導同色）
GUIDE_FACE = ('<rect x="1" y="1" width="46" height="46" rx="4" fill="#2c3e7a"/>'
              '<rect x="11" y="20" width="24" height="20" fill="#f7f3eb"/>'
              '<rect x="17" y="26" width="12" height="7" fill="#1a1a2e"/><rect x="24" y="27.5" width="4" height="4" fill="#f5b82e"/>'
              '<rect x="8" y="10" width="20" height="5" fill="#f5b82e"/><path d="M27 4 L41 12.5 L27 21 Z" fill="#f5b82e"/>')


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def check_meta():
    errs = []
    stems = [p["stem"] for p in M.PAGES]
    if len(stems) != len(set(stems)):
        errs.append("PAGES 有重複的 stem")
    on_disk = {f.stem for f in ROOT.glob("*.html")} - {"index"}
    for s in sorted(on_disk - set(stems)):
        errs.append(f"{s}.html 不在 PAGES 裡")
    for p in M.PAGES:
        s = p["stem"]
        if not (ROOT / f"{s}.html").exists():
            errs.append(f"PAGES 指向不存在的 {s}.html")
        for k in ("landmark", "blurb", "title", "code", "label"):
            if not p.get(k):
                errs.append(f"{s} 缺 {k}")
        for r in p.get("refs", []):
            if r not in BY:
                errs.append(f"{s} 的 refs 指向不存在的 {r}")
            elif BY[r]["grp"] != "dimm":
                errs.append(f"{s} 的 refs 只能指向先備頁，{r} 屬於 {BY[r]['grp']}")
        if not M.GUIDE.get(s):
            errs.append(f"{s} 缺阿迭的導覽詞（GUIDE）")
        if p["grp"] == "core":
            if not p.get("refs"):
                errs.append(f"正課 {s} 缺 refs")
            if s not in M.QUIZ:
                errs.append(f"正課 {s} 缺猜題（QUIZ）")
            f = M.FIGS.get(s)
            if not f:
                errs.append(f"正課 {s} 缺代表圖（FIGS）")
            elif not re.search(rf'id="{re.escape(f["fig"])}"', (ROOT / f"{s}.html").read_text(encoding="utf-8")):
                errs.append(f"{s}.html 裡沒有 id=\"{f['fig']}\"（FIGS 的深連結會失效）")
            elif not (FIG_DIR / f"{s}.webp").exists():
                errs.append(f"缺縮圖 island/figs/{s}.webp：跑 node tools/build_island_figs.js {s}")
    for r in M.TOUR["routes"]:
        for s in r["stems"]:
            if s not in BY:
                errs.append(f"導覽路線 {r['key']} 指向不存在的 {s}")
    for s, q in M.QUIZ.items():
        if s not in BY or BY[s]["grp"] != "core":
            errs.append(f"QUIZ 只放正課章節：{s}")
        if len(q["options"]) != 4 or not 0 <= q["answer"] < 4:
            errs.append(f"{s} 的猜題要有 4 個選項和有效的 answer")
    pos = Counter(q["answer"] for q in M.QUIZ.values())
    if pos and max(pos.values()) - min(pos.get(i, 0) for i in range(4)) > 1:
        errs.append(f"猜題正解位置不平衡：{dict(pos)}")
    grps = {p["grp"] for p in M.PAGES}
    if grps != set(M.ISLES):
        errs.append(f"ISLES 的鍵 {sorted(M.ISLES)} ≠ PAGES 的分區 {sorted(grps)}")
    vs = M.GRAPH["vertices"]
    for a, b in M.GRAPH["edges"]:
        if a not in vs or b not in vs:
            errs.append(f"GRAPH 的邊 {a}-{b} 指向不存在的頂點")
    for c in M.COMPARE["pairs"]:
        for s in c["stems"]:
            if s not in BY:
                errs.append(f"對比組 {c['key']} 指向不存在的 {s}")
    if errs:
        raise SystemExit("island_meta 不一致：\n  " + "\n  ".join(errs))


def webp_size(path: Path) -> tuple:
    """讀 WebP 檔頭的寬高（VP8／VP8L／VP8X），給 <img> 的 width/height，避免載入時版面跳動。"""
    b = path.read_bytes()[:30]
    kind = b[12:16]
    if kind == b"VP8 ":
        w, h = struct.unpack("<HH", b[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if kind == b"VP8L":
        v = int.from_bytes(b[21:25], "little")
        return (v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1
    if kind == b"VP8X":
        return int.from_bytes(b[24:27], "little") + 1, int.from_bytes(b[27:30], "little") + 1
    raise SystemExit(f"{path} 不是可辨識的 WebP")


def fig_record(s: str):
    f = M.FIGS.get(s)
    if not f:
        return None
    w, h = webp_size(FIG_DIR / f"{s}.webp")
    return dict(src=f"figs/{s}.webp", w=w, h=h, caption=f["caption"], href=f"../{s}.html#{f['fig']}")


def records():
    out = []
    for p in M.PAGES:
        s = p["stem"]
        out.append(dict(stem=s, grp=p["grp"], code=p["code"], title=p["title"], label=p["label"],
                        landmark=p["landmark"], blurb=p["blurb"], refs=list(p.get("refs", [])),
                        href=f"../{s}.html", guide=M.GUIDE[s], fig=fig_record(s), quiz=M.QUIZ.get(s)))
    return out


def item(r: dict) -> str:
    refs = ""
    if r["refs"]:
        names = "、".join(esc(BY[s]["title"]) for s in r["refs"])
        refs = f'            <span class="isl-refs">需要時可查閱：{names}</span>\n'
    return (f'        <li class="isl-item" data-stem="{r["stem"]}" data-grp="{r["grp"]}">\n'
            f'          <a class="isl-link" href="{esc(r["href"])}" data-stem="{r["stem"]}">\n'
            f'            <span class="isl-num">{r["code"]}</span>\n'
            f'            <span class="isl-title">{esc(r["title"])}</span>\n'
            f'            <span class="isl-landmark">{esc(r["landmark"])}</span>\n'
            f'            <span class="isl-blurb">{esc(r["blurb"])}</span>\n'
            f'{refs}'
            f'            <span class="isl-state" aria-hidden="true"></span>\n'
            f'          </a>\n'
            f'        </li>')


def isle_section(grp: str, recs: list) -> str:
    isle = M.ISLES[grp]
    rows = "\n".join(item(r) for r in recs if r["grp"] == grp)
    return (f'    <section class="isle isle-{grp}" id="isle-{grp}" data-grp="{grp}" aria-labelledby="isle-{grp}-h">\n'
            f'      <h2 id="isle-{grp}-h"><span class="isle-name">{esc(isle["name"])}</span>'
            f'<span class="isle-sub">{esc(isle["sub"])}</span></h2>\n'
            f'      <p class="isle-note">{esc(isle["note"])}</p>\n'
            f'      <ol class="isl-items">\n{rows}\n      </ol>\n'
            f'    </section>')


def build() -> str:
    check_meta()
    recs = records()
    css = (TEMPLATE / "island.css").read_text(encoding="utf-8").rstrip()
    # UI 層、對照台與場景層 inline 進同一個 module（共用頂層名稱）
    js = "\n\n".join((TEMPLATE / f).read_text(encoding="utf-8").rstrip()
                     for f in ("island.js", "island-compare.js", "island-scene.js"))
    data = dict(isles=[dict(grp=g, **v) for g, v in M.ISLES.items()], pages=recs, tour=M.TOUR,
                graph=M.GRAPH, compare=M.COMPARE)
    data_json = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    importmap = json.dumps({"imports": {"three": THREE_MAIN, "three/addons/": THREE_ADDONS, **CORE_REMAP},
                            "integrity": THREE_SRI}, indent=1)
    preload = "\n".join(f'<link rel="modulepreload" href="{u}" integrity="{h}" crossorigin="anonymous">'
                        for u, h in THREE_SRI.items())
    sections = "\n".join(isle_section(g, recs) for g in M.ISLES)
    jumps = "\n".join(f'      <button type="button" class="isl-jump-btn" data-grp="{g}">{esc(v["name"])}</button>'
                      for g, v in M.ISLES.items())
    n_core = sum(1 for r in recs if r["grp"] == "core")
    return f"""<!DOCTYPE html>
<!-- 產物：由 tools/build_island.py 產生，不要手改。文案在 tools/island_meta.py，樣式與程式在 tools/template/island* -->
<html lang="zh-Hant" data-mode="power">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="資料結構矽晶群島：以 3D 晶片群島導覽資料結構 × C++ 互動自學網站的 {len(recs)} 個單元，點晶片島即可前往教材，也能先猜下一步、對照不同資料結構。">
<title>{TITLE} — Data Structures in Silicon</title>
<script>
/* 有 WebGL 的瀏覽器先排 3D 版面並顯示載入中，避免 2D 卡片閃一下再切換；失敗時 island.js 會移除 */
if (window.WebGLRenderingContext) document.documentElement.classList.add('gl-pending');
try {{ if (localStorage.getItem('dscpp-island:mode') === 'print') document.documentElement.dataset.mode = 'print'; }} catch (e) {{}}
</script>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<style>
{css}
</style>
<script type="importmap">
{importmap}
</script>
{preload}
</head>
<body>
<header class="isl-bar">
  <a class="isl-home" href="../index.html">← 回到章節總覽</a>
  <div class="isl-brand">
    <h1>{TITLE}</h1>
    <span class="isl-brand-en">Data Structures in Silicon · NSYSU MATH208</span>
  </div>
  <div class="isl-actions">
    <button type="button" class="isl-btn is-strong" id="islCompare">同操作對比</button>
    <button type="button" class="isl-btn" id="islReset" hidden>重設視角</button>
    <button type="button" class="isl-btn" id="islClear">清除足跡</button>
  </div>
</header>
<main class="isl-main">
  <div class="isl-stage" id="islStage" hidden>
    <p class="isl-loading" aria-hidden="true">通電中…</p>
    <canvas id="islCanvas" tabindex="0" aria-label="3D 晶片群島：拖曳旋轉、滾輪縮放、點選晶片島；也可用右側列表操作"></canvas>
    <div class="isl-jumps" role="group" aria-label="跳到區域">
{jumps}
    </div>
    <div class="isl-labels" id="islLabels"></div>
    <button type="button" class="isl-bubble" id="islBubble" hidden>{esc(M.TOUR["hello"])}</button>
    <button type="button" class="isl-mode" id="islMode" aria-pressed="false">切到藍圖</button>
    <p class="isl-hint" aria-hidden="true">拖曳旋轉 · 滾輪或雙指縮放 · 點晶片島</p>
  </div>
  <nav class="isl-list" id="islList" aria-label="章節列表">
    <p class="isl-intro">三個區域、{len(recs)} 個單元，全部可以自由進入。正課 {n_core} 章依授課順序排列；
      先備模組是選讀，需要時再查閱。<span class="isl-trail-note">「足跡」只存在這台裝置的瀏覽器裡。</span></p>
{sections}
  </nav>
  <aside class="isl-panel" id="islPanel" hidden aria-labelledby="islPanelTitle">
    <button type="button" class="isl-panel-close" id="islPanelClose" aria-label="關閉">×</button>
    <div class="isl-guide" id="islGuide" hidden>
      <svg class="isl-guide-face" viewBox="0 0 48 48" aria-hidden="true">{GUIDE_FACE}</svg>
      <div class="isl-guide-body">
        <div class="isl-guide-who"><b>{esc(M.TOUR["name"])}</b><span id="islGuideStep"></span></div>
        <p class="isl-guide-text" id="islGuideText" aria-live="polite"></p>
        <div class="isl-guide-choices" id="islGuideChoices"></div>
      </div>
    </div>
    <div class="isl-panel-page" id="islPanelPage">
      <div class="isl-panel-kicker" id="islPanelKicker"></div>
      <h2 id="islPanelTitle"></h2>
      <div class="isl-panel-landmark" id="islPanelLandmark"></div>
      <div class="isl-tabs" id="islTabs" role="group" aria-label="切換內容" hidden>
        <button type="button" class="isl-tab" id="islTabInfo" aria-pressed="true">簡介</button>
        <button type="button" class="isl-tab" id="islTabQuiz" aria-pressed="false">先猜下一步</button>
      </div>
      <div id="islInfo">
        <p class="isl-panel-blurb" id="islPanelBlurb"></p>
        <figure class="isl-fig" id="islFig" hidden>
          <a class="isl-fig-img" id="islFigLink" href="#"><img id="islFigImg" alt="" loading="lazy" decoding="async"></a>
          <figcaption><span class="isl-fig-h">代表互動圖</span><span id="islFigCap"></span></figcaption>
          <a class="isl-fig-go" id="islFigGo" href="#">去操作這張圖 →</a>
        </figure>
        <div class="isl-panel-refs" id="islPanelRefs" hidden>
          <div class="isl-panel-refs-h">卡在語法時可查閱</div>
          <ul id="islPanelRefList"></ul>
        </div>
      </div>
      <div class="isl-quiz" id="islQuiz" hidden>
        <p class="isl-quiz-q" id="islQuizQ"></p>
        <div class="isl-quiz-opts" id="islQuizOpts"></div>
        <div class="isl-quiz-why" id="islQuizWhy" aria-live="polite" hidden></div>
      </div>
      <div class="isl-panel-cmp" id="islPanelCmp" hidden></div>
      <div class="isl-panel-actions">
        <a class="isl-go" id="islPanelGo" href="#">前往教材 →</a>
        <button type="button" class="isl-done" id="islPanelDone" aria-pressed="false">標記完成</button>
      </div>
    </div>
    <div class="isl-guide-nav" id="islGuideNav" hidden>
      <button type="button" class="isl-btn2" id="islGuidePrev">← 上一站 <code>--it</code></button>
      <button type="button" class="isl-btn2 is-primary" id="islGuideNext"></button>
      <button type="button" class="isl-btn2 is-quiet" id="islGuideEnd">結束導覽</button>
    </div>
  </aside>
</main>
<dialog class="cmp" id="cmpDialog" aria-labelledby="cmpTitle">
  <div class="cmp-head">
    <div>
      <div class="cmp-kicker">同操作對比</div>
      <h2 id="cmpTitle"></h2>
      <p class="cmp-op" id="cmpOp"></p>
    </div>
    <button type="button" class="isl-panel-close cmp-close" id="cmpClose" aria-label="關閉">×</button>
  </div>
  <div class="cmp-tabs" id="cmpTabs" role="group" aria-label="選擇對照組"></div>
  <div class="cmp-opts" id="cmpOpts"></div>
  <div class="cmp-sides">
    <section class="cmp-side" id="cmpLeft"></section>
    <section class="cmp-side" id="cmpRight"></section>
  </div>
  <p class="cmp-note" id="cmpNote" aria-live="polite"></p>
  <div class="cmp-ctrl">
    <button type="button" class="isl-btn2" id="cmpReset">重來</button>
    <button type="button" class="isl-btn2" id="cmpPrev">← 上一步</button>
    <button type="button" class="isl-btn2 is-primary" id="cmpNext">下一步 →</button>
    <button type="button" class="isl-btn2" id="cmpPlay">▶ 自動播放</button>
    <span class="cmp-step" id="cmpStep"></span>
  </div>
</dialog>
<script type="application/json" id="island-data">
{data_json}
</script>
<script type="module">
{js}
</script>
</body>
</html>
"""


def main():
    out = build()
    OUT.parent.mkdir(exist_ok=True)
    old = OUT.read_text(encoding="utf-8") if OUT.exists() else None
    if old != out:
        OUT.write_text(out, encoding="utf-8")
        print(f"寫入 {OUT.relative_to(ROOT)}（{len(out.encode()) // 1024} KB）")
    else:
        print(f"{OUT.relative_to(ROOT)} 已是最新")


if __name__ == "__main__":
    main()
