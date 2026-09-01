#!/usr/bin/env python3
"""把 17 頁 byte-identical 的 Player（v1）冪等地升級成 player-v2。

## 背景

全站的逐步動畫由每頁 inline 的 `class Player` 驅動。v1 沒有暫停、沒有
playing 狀態、速度只認建構時傳入的 delayInput（多數實例沒傳，寫死 700ms）。
v2 是 v1 的超集：建構參數與 play/step/stop/reset 語意完全相容（27 個既有
實例不需要改呼叫），新增 pause()/playing/toggle(btn)/setDelay(ms)，
且 play 的每個 tick 重讀 delayInput.value——接上速度滑桿即時生效。

## 冪等機制（仿 tools/contrast_fix.py）

類別在 <script> 裡，不能用 HTML 註解標記，改用成對 JS 註解
`/* player-v2 */ … /* /player-v2 */`。首次替換前先 md5 核對 v1 原文
（e885dbe62cca…），不符就 abort 該頁——寧可失敗也不誤傷手改過的頁面。
已升級的頁面重跑會整段換新（升版即重跑）。

## 適用範圍

*.html 排除 trees（Player B 變體，自帶 setDelay）、searching_sorting
（Animator，功能已完整）、graphs（無 Player 類別）、index。
graphs 之後要接 Player 時用 `--inject graphs.html` 把 v2 注入主 script。

trees/searching_sorting 不動；此腳本目前只在 cpp 站（姊妹站待同步，見 HANDOFF）。
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER_BEGIN = "/* player-v2 */"
MARKER_END = "/* /player-v2 */"

V1_RE = re.compile(
    r"/\* step player: frames = \[\{\.\.\.\}\], apply\(frame\) renders \*/\n"
    r"class Player \{.*?\n\}\n",
    re.S,
)
V1_MD5 = "e885dbe62cca"  # md5 前 12 碼，upgrade 前核對

SKIP = {"trees.html", "searching_sorting.html", "graphs.html", "index.html"}

# 注意：內含大括號，維持普通字串（HANDOFF 坑 #6：不要改成 f-string）
NEW_BLOCK = MARKER_BEGIN + """
/* 逐步動畫播放器 v2：frames = [{...}]，apply(frame) 負責渲染。
   與 v1 相容：建構子 {frames, apply, delayInput, onDone}、play/step/stop/reset。
   新增：pause()、playing 狀態、toggle(btn)（▶/⏸ 按鈕一行接線）、setDelay(ms)。
   每個 tick 重讀 delayInput.value，速度滑桿拖了即時生效。 */
class Player {
  constructor({frames, apply, delayInput, onDone}) {
    this.frames = frames; this.apply = apply;
    this.delayInput = delayInput; this.i = -1; this.timer = null;
    this.playing = false; this._delay = null; this._done = false;
    this._btn = null;  // toggle 按過的 ⏸/▶ 按鈕，之後狀態變化都同步文字
    this.onDone = onDone || (()=>{});
  }
  _sync() { if (this._btn) this._btn.textContent = this.playing ? '⏸ 暫停' : '▶ 繼續'; }
  _d() {
    if (this._delay != null) return this._delay;
    return this.delayInput ? parseInt(this.delayInput.value, 10) : 700;
  }
  setDelay(ms) { this._delay = ms; }
  _advance() {
    if (this.i + 1 >= this.frames.length) {
      this.pause();
      if (!this._done) { this._done = true; this.onDone(); }  // 播畢只通知一次
      return false;
    }
    this.i += 1; this.apply(this.frames[this.i]);
    return true;
  }
  step() { this.pause(); this._advance(); }
  play() {
    this.pause(); this.playing = true;
    const tick = () => {
      if (!this.playing) return;
      if (!this._advance()) return;
      this.timer = setTimeout(tick, this._d());
    };
    tick();
    this._sync();
  }
  pause() {
    if (this.timer) { clearTimeout(this.timer); this.timer = null; }
    this.playing = false;
    this._sync();
  }
  toggle(btn) {
    if (btn) this._btn = btn;
    if (this.playing) this.pause();
    else {
      if (this._done && this.frames.length) { this.i = -1; this._done = false; }  // 播畢後再按＝重播
      this.play();
    }
  }
  stop() { this.pause(); }
  reset() { this.stop(); this.i = -1; this._done = false; if (this.frames.length) this.apply(this.frames[0]); }
}
""" + MARKER_END + "\n"

# graphs.html 的注入錨點：主 <script>（L1699 起）開頭的工具區註解
GRAPHS_ANCHOR = "/* =============================================================\n   通用：SVG 圖渲染工具"


def ensure(path: Path) -> bool:
    """升級或更新一頁。有改動回 True。"""
    s = path.read_text(encoding="utf-8")
    if MARKER_BEGIN in s:
        i = s.index(MARKER_BEGIN)
        j = s.index(MARKER_END, i) + len(MARKER_END)
        j = s.index("\n", j) + 1 if s[j:j + 1] == "\n" else j
        if s[i:j] == NEW_BLOCK:
            return False
        s = s[:i] + NEW_BLOCK + s[j:]
    else:
        m = V1_RE.search(s)
        assert m, f"{path.name}: 找不到 Player v1 原文"
        got = hashlib.md5(m.group(0).encode()).hexdigest()[:12]
        assert got == V1_MD5, f"{path.name}: Player v1 原文 md5 不符（{got}），不敢動"
        s = s[:m.start()] + NEW_BLOCK + s[m.end():]
    path.write_text(s, encoding="utf-8")
    return True


def inject(path: Path) -> bool:
    """把 v2 注入沒有 Player 類別的頁（graphs）。"""
    s = path.read_text(encoding="utf-8")
    if MARKER_BEGIN in s:
        return ensure(path)
    assert "class Player" not in s, f"{path.name}: 已有 Player 類別，不該用 --inject"
    assert GRAPHS_ANCHOR in s, f"{path.name}: 找不到注入錨點"
    s = s.replace(GRAPHS_ANCHOR, NEW_BLOCK + "\n" + GRAPHS_ANCHOR, 1)
    path.write_text(s, encoding="utf-8")
    return True


def main(argv):
    if len(argv) >= 2 and argv[0] == "--inject":
        for name in argv[1:]:
            p = ROOT / name
            print(f"  {p.name:34s} {'已注入' if inject(p) else '已是最新'}")
        return 0
    n = 0
    for f in sorted(ROOT.glob("*.html")):
        if f.name in SKIP:
            continue
        if ensure(f):
            print(f"  {f.name:34s} 已升級")
            n += 1
        else:
            print(f"  {f.name:34s} 已是最新")
    print(f"\n{n} 個檔案更新")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
