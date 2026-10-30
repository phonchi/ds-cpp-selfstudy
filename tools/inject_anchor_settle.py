#!/usr/bin/env python3
"""在指定教材頁加入錨點校正：MathJax 與延後繪製的互動元件會在載入後改變版面，
讓 頁面.html#id 的落點偏掉（3D 群島的「去操作這張圖」就是這種連結）；偏移量隨載入時序變動，所以正課九章都加。冪等。

只在網址有 hash 時作用：頁面高度改變就把目標拉回距頂端 24 px；讀者一捲動或操作就停止，最多持續 5 秒。
區塊放在 </body> 前、所有 gen 區之外，重跑 enrich／apply_zh 不會影響它。

用法：python3 tools/inject_anchor_settle.py          # 依 PAGES 處理
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["introduction", "analysis", "arrays", "linked_lists", "linear_structures", "recursion",
         "searching_sorting", "graphs", "trees"]
OPEN, CLOSE = "<!-- anchor-settle -->", "<!-- /anchor-settle -->"
BLOCK = f"""{OPEN}
<script>
(function () {{
  var id = decodeURIComponent(location.hash.slice(1)), t = id && document.getElementById(id);
  if (!t || !window.ResizeObserver) return;
  var stop = false, end = function () {{ stop = true; ro.disconnect(); }};
  var pull = function () {{
    if (stop) return;
    var d = t.getBoundingClientRect().top - 24;
    if (Math.abs(d) > 2) window.scrollBy({{ top: d, behavior: 'instant' }});
  }};
  var ro = new ResizeObserver(pull);
  ro.observe(document.body);
  pull();
  ['wheel', 'touchstart', 'keydown', 'pointerdown'].forEach(function (e) {{ addEventListener(e, end, {{ passive: true, once: true }}); }});
  setTimeout(end, 5000);
}})();
</script>
{CLOSE}
"""


def main():
    for stem in PAGES:
        f = ROOT / f"{stem}.html"
        s = f.read_text(encoding="utf-8")
        if OPEN in s:
            a, b = s.index(OPEN), s.index(CLOSE) + len(CLOSE) + 1
            new = s[:a] + BLOCK + s[b:]
        else:
            i = s.rindex("</body>")
            new = s[:i] + BLOCK + s[i:]
        if new != s:
            f.write_text(new, encoding="utf-8")
            print("寫入", f.name)


if __name__ == "__main__":
    main()
