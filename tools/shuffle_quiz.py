#!/usr/bin/env python3
"""頁內自測題選項洗牌（quiz-shuffle v1）。

背景：各頁 .quiz-opt / .sq-opt 是靜態 DOM，正解位置嚴重偏向 (A)。這支腳本在 </body> 前
注入一段 JS：載入時對每個 .quiz-options / .sq-opts 容器用「頁面路徑＋容器序號」當種子的
固定排列重排子節點（每次載入同順序，學生可以說「選 B」），再依新順序重寫 .opt-letter。
quizCheck 走 parentElement.querySelectorAll＋data-correct、sq-opt 走 dataset.c，與位置無關。

冪等：成對標記 MARKER_BEGIN / MARKER_END；版本升級改 JS 後重跑即整段換新。
用法：python3 tools/shuffle_quiz.py            # 全站
      由 inject_prereq_cpp.py 呼叫 ensure(path)  # 單頁
"""
import glob, os, re, sys
from pathlib import Path

MARKER_BEGIN = "/* quiz-shuffle v1 */"
MARKER_END = "/* /quiz-shuffle v1 */"

JS = r"""(function () {
  function hash(str) {
    var h = 2166136261;
    for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
    return h || 1;
  }
  function run() {
    var page = (location.pathname.split('/').pop() || 'index');
    var groups = document.querySelectorAll('.quiz-options, .sq-opts');
    Array.prototype.forEach.call(groups, function (g, gi) {
      var kids = Array.prototype.filter.call(g.children, function (c) {
        return c.classList.contains('quiz-opt') || c.classList.contains('sq-opt');
      });
      if (kids.length < 2) return;
      var seed = hash(page + '#' + gi);
      function rnd() {  // xorshift32，固定種子 → 固定排列
        seed ^= seed << 13; seed >>>= 0; seed ^= seed >>> 17; seed ^= seed << 5; seed >>>= 0;
        return seed / 4294967296;
      }
      for (var i = kids.length - 1; i > 0; i--) {
        var j = Math.floor(rnd() * (i + 1));
        var t = kids[i]; kids[i] = kids[j]; kids[j] = t;
      }
      kids.forEach(function (k, i) {
        g.appendChild(k);
        var L = k.querySelector('.opt-letter');
        if (L) L.textContent = '(' + String.fromCharCode(65 + i) + ')';
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();"""

BLOCK = f"<script>{MARKER_BEGIN}\n{JS}\n{MARKER_END}</script>\n"

def ensure(path) -> bool:
    """有 quiz 的頁面保證帶最新版洗牌 JS。回傳是否有改動。"""
    path = Path(path)
    s = path.read_text(encoding="utf-8")
    has_quiz = re.search(r'class="(quiz-options|sq-opts)"', s) is not None
    pat = re.compile(r"<script>" + re.escape(MARKER_BEGIN) + r".*?" + re.escape(MARKER_END) + r"</script>\n?", re.S)
    if not has_quiz:
        new, n = pat.subn("", s)
    elif pat.search(s):
        new, n = pat.subn(lambda m: BLOCK, s)
        if new == s:
            return False
    else:
        assert s.count("</body>") == 1, path
        new = s.replace("</body>", BLOCK + "</body>", 1)
    if new != s:
        path.write_text(new, encoding="utf-8")
        return True
    return False

def main():
    root = Path(__file__).resolve().parent.parent
    changed = 0
    for f in sorted(glob.glob(str(root / "*.html"))):
        if ensure(f):
            print(f"  {os.path.basename(f)} 注入/更新 quiz-shuffle")
            changed += 1
    print(f"共 {changed} 頁有改動")

if __name__ == "__main__":
    main()
