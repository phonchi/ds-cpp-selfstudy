#!/usr/bin/env python3
"""把 contrast-fix 的覆寫 CSS 冪等地補進每一頁。兩站共用同一支（逐位元組相同）。

## 為什麼需要這支

base.css 的 code{color:var(--accent2)} 與 strong{color:var(--ink)} 一旦落進深色底
容器就會消失。最糟的是 .cmp-table th 與 .info-box .info-label——底色也是 #2c3e7a，
對比 1.00，字跟背景完全同色。使用者在 introduction 看到的
「int：4 byte｜範圍…」的 int 不見，就是 .status-banner 裡的 <strong>（對比 1.07）。

## 為什麼不改既有的 <style> 區塊

兩站的 CSS 是 inline 在每一頁的，而且不只一種複本（C++ 8 種、Python 12 種）。
這支**完全不碰既有的 style 區塊**，只在 </head> 之前追加最後一個 <style>，
靠層疊順序取勝——複本幾種都無所謂。

注入器（inject_prereq_*.py）碰到已注入的頁面會整頁 skip，
所以它們沒辦法回填 CSS；這支用自己的成對標記，而且是「換掉」不是「跳過」，
所以升版時重跑就會更新。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER_BEGIN = "<!-- contrast-fix v1 -->"
MARKER_END = "<!-- /contrast-fix -->"

CSS = """/* ══ contrast-fix v1 ═══════════════════════════════════════════════
   base.css 有兩條全域規則：code{color:var(--accent2)}（#2c3e7a）與
   strong{color:var(--ink)}（#1a1a2e）。它們一旦落進深色底容器就會消失——
   最糟的是 .cmp-table th 與 .info-box .info-label，底色也是 #2c3e7a，
   對比 1.00，字跟背景完全同色。

   下面把「深色底容器裡的行內元素」統一改掉。chip 用 rgba(26,26,46,.7)
   配 #ffe9a8：對本設計系統的每一個深色底，最差的對比是 7.84（在 #f39c12 上），
   全部過 WCAG AA。單一組值、不分層，才驗得動。

   只列 code/kbd/a/strong/b/em/i 七個標籤，**從不用 * 、從不碰 span**——
   .pseudo-code 的 .kw/.str/.fn/.com/.num 與 .status-banner 的 .status-icon
   本來就是為深底調好的，不能被蓋掉。

   容器清單是三站的聯集（多列的在該站只是無效的死規則，漏列才會出事）。
   真正的把關者是 tools/check_contrast.py，它會逐站掃出所有深色底選擇器再比對這份清單。
   ═══════════════════════════════════════════════════════════════════════ */
.adj-matrix th code,.adj-matrix th kbd,.adj-matrix th a,.ai-box .ai-label code,.ai-box .ai-label kbd,
.ai-box .ai-label a,.bar code,.bar kbd,.bar a,.bar-fill code,.bar-fill kbd,.bar-fill a,.bq-item code,
.bq-item kbd,.bq-item a,.bs-hl code,.bs-hl kbd,.bs-hl a,.bs-item code,.bs-item kbd,.bs-item a,.btn code,
.btn kbd,.btn a,.btn-play code,.btn-play kbd,.btn-play a,.btn-shuffle code,.btn-shuffle kbd,.btn-shuffle a,
.btn-step code,.btn-step kbd,.btn-step a,.btn-toggle code,.btn-toggle kbd,.btn-toggle a,.chain-node code,
.chain-node kbd,.chain-node a,.char-bad code,.char-bad kbd,.char-bad a,.char-cur code,.char-cur kbd,
.char-cur a,.chess-cell.current code,.chess-cell.current kbd,.chess-cell.current a,.chess-cell.dark code,
.chess-cell.dark kbd,.chess-cell.dark a,.chess-cell.start code,.chess-cell.start kbd,.chess-cell.start a,
.chess-cell.visited code,.chess-cell.visited kbd,.chess-cell.visited a,.cmp-table th code,.cmp-table th kbd,
.cmp-table th a,.fib-card.memo .bar-fill code,.fib-card.memo .bar-fill kbd,.fib-card.memo .bar-fill a,
.heap-cell.active code,.heap-cell.active kbd,.heap-cell.active a,.token.active code,.token.active kbd,
.token.active a,.console code,.console kbd,.console a,.ds-item code,.ds-item kbd,.ds-item a,.eq-card code,
.eq-card kbd,.eq-card a,.eslx code,.eslx kbd,.eslx a,.fc-card .fc-front code,.fc-card .fc-front kbd,
.fc-card .fc-front a,.fc-controls button:hover code,.fc-controls button:hover kbd,
.fc-controls button:hover a,.float-nav a.active code,.float-nav a.active kbd,.float-nav a.active a,
.game-console code,.game-console kbd,.game-console a,.heap-cell.parent code,.heap-cell.parent kbd,
.heap-cell.parent a,.heap-cell.swap code,.heap-cell.swap kbd,.heap-cell.swap a,.hero code,.hero kbd,.hero a,
.info-box .info-label code,.info-box .info-label kbd,.info-box .info-label a,
.info-card .ic-title .ic-badge code,.info-card .ic-title .ic-badge kbd,.info-card .ic-title .ic-badge a,
.kv-pair .kv-key code,.kv-pair .kv-key kbd,.kv-pair .kv-key a,.num-cell.sel code,.num-cell.sel kbd,
.num-cell.sel a,.obj-box .obj-type code,.obj-box .obj-type kbd,.obj-box .obj-type a,.obj-box .tag code,
.obj-box .tag kbd,.obj-box .tag a,.preset-btn.active code,.preset-btn.active kbd,.preset-btn.active a,
.pseudo-code code,.pseudo-code kbd,.pseudo-code a,.quiz-box .quiz-code code,.quiz-box .quiz-code kbd,
.quiz-box .quiz-code a,.quiz-box .quiz-label .multi-badge code,.quiz-box .quiz-label .multi-badge kbd,
.quiz-box .quiz-label .multi-badge a,.sandbox .sandbox-label code,.sandbox .sandbox-label kbd,
.sandbox .sandbox-label a,.sandbox-result code,.sandbox-result kbd,.sandbox-result a,
.seq-cell .order-badge code,.seq-cell .order-badge kbd,.seq-cell .order-badge a,.sol-links a:hover code,
.sol-links a:hover kbd,.sol-links a:hover a,.sq-code code,.sq-code kbd,.sq-code a,.stack-frame code,
.stack-frame kbd,.stack-frame a,.status-banner code,.status-banner kbd,.status-banner a,
.strip .cell.held code,.strip .cell.held kbd,.strip .cell.held a,.strip .cell.picked code,
.strip .cell.picked kbd,.strip .cell.picked a,.strip .cell.train code,.strip .cell.train kbd,
.strip .cell.train a,.study-guide .sg-links a:hover code,.study-guide .sg-links a:hover kbd,
.study-guide .sg-links a:hover a,.t-node code,.t-node kbd,.t-node a,.tok code,.tok kbd,.tok a,.tok-op code,
.tok-op kbd,.tok-op a,.traceback code,.traceback kbd,.traceback a,.trav-mini .mini-output code,
.trav-mini .mini-output kbd,.trav-mini .mini-output a,.traversal-output code,.traversal-output kbd,
.traversal-output a,.tree-node.done code,.tree-node.done kbd,.tree-node.done a,.vert-table th code,
.vert-table th kbd,.vert-table th a{background:rgba(26,26,46,.7);color:#ffe9a8;}
.adj-matrix th strong,.adj-matrix th b,.ai-box .ai-label strong,.ai-box .ai-label b,.bar strong,.bar b,
.bar-fill strong,.bar-fill b,.bq-item strong,.bq-item b,.bs-hl strong,.bs-hl b,.bs-item strong,.bs-item b,
.btn strong,.btn b,.btn-play strong,.btn-play b,.btn-shuffle strong,.btn-shuffle b,.btn-step strong,
.btn-step b,.btn-toggle strong,.btn-toggle b,.chain-node strong,.chain-node b,.char-bad strong,.char-bad b,
.char-cur strong,.char-cur b,.chess-cell.current strong,.chess-cell.current b,.chess-cell.dark strong,
.chess-cell.dark b,.chess-cell.start strong,.chess-cell.start b,.chess-cell.visited strong,
.chess-cell.visited b,.cmp-table th strong,.cmp-table th b,.fib-card.memo .bar-fill strong,
.fib-card.memo .bar-fill b,.heap-cell.active strong,.heap-cell.active b,.token.active strong,.token.active b,
.console strong,.console b,.ds-item strong,.ds-item b,.eq-card strong,.eq-card b,.eslx strong,.eslx b,
.fc-card .fc-front strong,.fc-card .fc-front b,.fc-controls button:hover strong,.fc-controls button:hover b,
.float-nav a.active strong,.float-nav a.active b,.game-console strong,.game-console b,
.heap-cell.parent strong,.heap-cell.parent b,.heap-cell.swap strong,.heap-cell.swap b,.hero strong,.hero b,
.info-box .info-label strong,.info-box .info-label b,.info-card .ic-title .ic-badge strong,
.info-card .ic-title .ic-badge b,.kv-pair .kv-key strong,.kv-pair .kv-key b,.num-cell.sel strong,
.num-cell.sel b,.obj-box .obj-type strong,.obj-box .obj-type b,.obj-box .tag strong,.obj-box .tag b,
.preset-btn.active strong,.preset-btn.active b,.pseudo-code strong,.pseudo-code b,
.quiz-box .quiz-code strong,.quiz-box .quiz-code b,.quiz-box .quiz-label .multi-badge strong,
.quiz-box .quiz-label .multi-badge b,.sandbox .sandbox-label strong,.sandbox .sandbox-label b,
.sandbox-result strong,.sandbox-result b,.seq-cell .order-badge strong,.seq-cell .order-badge b,
.sol-links a:hover strong,.sol-links a:hover b,.sq-code strong,.sq-code b,.stack-frame strong,.stack-frame b,
.status-banner strong,.status-banner b,.strip .cell.held strong,.strip .cell.held b,
.strip .cell.picked strong,.strip .cell.picked b,.strip .cell.train strong,.strip .cell.train b,
.study-guide .sg-links a:hover strong,.study-guide .sg-links a:hover b,.t-node strong,.t-node b,.tok strong,
.tok b,.tok-op strong,.tok-op b,.traceback strong,.traceback b,.trav-mini .mini-output strong,
.trav-mini .mini-output b,.traversal-output strong,.traversal-output b,.tree-node.done strong,
.tree-node.done b,.vert-table th strong,.vert-table th b{color:#fff;}
.adj-matrix th em,.adj-matrix th i,.ai-box .ai-label em,.ai-box .ai-label i,.bar em,.bar i,.bar-fill em,
.bar-fill i,.bq-item em,.bq-item i,.bs-hl em,.bs-hl i,.bs-item em,.bs-item i,.btn em,.btn i,.btn-play em,
.btn-play i,.btn-shuffle em,.btn-shuffle i,.btn-step em,.btn-step i,.btn-toggle em,.btn-toggle i,
.chain-node em,.chain-node i,.char-bad em,.char-bad i,.char-cur em,.char-cur i,.chess-cell.current em,
.chess-cell.current i,.chess-cell.dark em,.chess-cell.dark i,.chess-cell.start em,.chess-cell.start i,
.chess-cell.visited em,.chess-cell.visited i,.cmp-table th em,.cmp-table th i,.fib-card.memo .bar-fill em,
.fib-card.memo .bar-fill i,.heap-cell.active em,.heap-cell.active i,.token.active em,.token.active i,
.console em,.console i,.ds-item em,.ds-item i,.eq-card em,.eq-card i,.eslx em,.eslx i,.fc-card .fc-front em,
.fc-card .fc-front i,.fc-controls button:hover em,.fc-controls button:hover i,.float-nav a.active em,
.float-nav a.active i,.game-console em,.game-console i,.heap-cell.parent em,.heap-cell.parent i,
.heap-cell.swap em,.heap-cell.swap i,.hero em,.hero i,.info-box .info-label em,.info-box .info-label i,
.info-card .ic-title .ic-badge em,.info-card .ic-title .ic-badge i,.kv-pair .kv-key em,.kv-pair .kv-key i,
.num-cell.sel em,.num-cell.sel i,.obj-box .obj-type em,.obj-box .obj-type i,.obj-box .tag em,.obj-box .tag i,
.preset-btn.active em,.preset-btn.active i,.pseudo-code em,.pseudo-code i,.quiz-box .quiz-code em,
.quiz-box .quiz-code i,.quiz-box .quiz-label .multi-badge em,.quiz-box .quiz-label .multi-badge i,
.sandbox .sandbox-label em,.sandbox .sandbox-label i,.sandbox-result em,.sandbox-result i,
.seq-cell .order-badge em,.seq-cell .order-badge i,.sol-links a:hover em,.sol-links a:hover i,.sq-code em,
.sq-code i,.stack-frame em,.stack-frame i,.status-banner em,.status-banner i,.strip .cell.held em,
.strip .cell.held i,.strip .cell.picked em,.strip .cell.picked i,.strip .cell.train em,.strip .cell.train i,
.study-guide .sg-links a:hover em,.study-guide .sg-links a:hover i,.t-node em,.t-node i,.tok em,.tok i,
.tok-op em,.tok-op i,.traceback em,.traceback i,.trav-mini .mini-output em,.trav-mini .mini-output i,
.traversal-output em,.traversal-output i,.tree-node.done em,.tree-node.done i,.vert-table th em,
.vert-table th i{color:inherit;}
"""


def block():
    return MARKER_BEGIN + "\n<style>\n" + CSS.rstrip() + "\n</style>\n" + MARKER_END + "\n"


def ensure(path: Path) -> bool:
    """插入或更新覆寫區塊。有改動回 True。"""
    s = path.read_text(encoding="utf-8")
    new = block()
    if MARKER_BEGIN in s:
        i = s.index(MARKER_BEGIN)
        j = s.index(MARKER_END, i) + len(MARKER_END)
        j = s.index("\n", j) + 1 if s[j:j + 1] == "\n" else j
        if s[i:j] == new:
            return False
        s = s[:i] + new + s[j:]
    else:
        # check_links_*.py 也倚賴這個前提，先斷言再寫
        assert s.count("</head>") == 1, f"{path.name}: </head> 不是恰好一個"
        s = s.replace("</head>", new + "</head>", 1)
    path.write_text(s, encoding="utf-8")
    return True


def main():
    n = 0
    for f in sorted(ROOT.glob("*.html")):
        if ensure(f):
            print(f"  {f.name:34s} 已補上")
            n += 1
        else:
            print(f"  {f.name:34s} 已是最新")
    print(f"\n{n} 個檔案更新")
    return 0


if __name__ == "__main__":
    sys.exit(main())
