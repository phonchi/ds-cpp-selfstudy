# 接力文件（ds-cpp-selfstudy）

姊妹站是 [`ds-python-selfstudy`](https://github.com/phonchi/ds-python-selfstudy)，兩站結構完全相同，
`recursion.html` 的整個 `<head>`（1–332 行）除了 `<title>` 之外逐位元組一致。改動任一站之前，
先看另一站有沒有已經解過同一個問題。

## 現況（2026-08-28 已上線）

站上共 21 頁：**兩章課前準備 ＋ 九章正課 ＋ 九頁選讀先備知識**。

| 區塊 | 頁面 |
|---|---|
| 課前準備 | `00a_why_code`（為什麼還要學）、`00b_setup`（環境安裝） |
| 正課 | `introduction` → `trees` 九章（本次未改內容，只動了 introduction 的一行導覽） |
| 先備知識 | `p1_cpp_basics` … `p9_oop_advanced` |

先備頁合計 61 題題庫、195 張詞彙卡、16 個互動元件。**所有程式碼範例都以
`g++ -std=c++17` 實際編譯執行過**，並直接 `#include "dscpp/…"` 引用課程的標頭檔。

課程 notebook 需要打過 `-I.` patch 的 C++ kernel：
[phonchi/jupyter-cpp-kernel @ nsysu-math208](https://github.com/phonchi/jupyter-cpp-kernel/tree/nsysu-math208)
（fork 自 shiroinekotfs，MIT，與上游只差一行）。PyPI 原版缺這一行，`#include "dscpp/…"` 會找不到檔案。
安裝方式見 00B —— 注意該套件**沒有宣告任何相依**，要先自己裝 `jupyterlab`。

## 工具鏈與它們的契約

| 腳本 | 做什麼 | 冪等靠什麼 |
|---|---|---|
| `tools/apply_zh.py` | 從 `data/` 重生各頁的 `const FLASHCARDS` 與 `<section id="bankquiz">` | 整段以邊界重生 |
| `tools/inject_prereq_cpp.py` | 課前章與先備頁的尾段注入（導讀框、bankquiz 錨點、詞彙卡區、上下頁導覽、CSS/JS、補 MathJax） | `<!-- prereq-injected -->` 標記 |
| `tools/check_links_cpp.py` | 錨點、站內連結、注入前置條件、Python 殘留 | — |
| `tools/enrich/enrich_lib.py` | `hl()` C++ 上色、`card()` 範例卡、`run_cpp()` 編譯實跑 | — |
| `tools/enrich/enrich_*.py` | 九章正課頁的一次性充實，已全部注入完畢 | `dx-*` 標記 |
| `~/ds_cpp/Slides/tools/check_selfstudy.py` | 外部 gate：掃 Python 殘留、quiz 單一正解、錨點 | — |

`inject_prereq_cpp.py` 的 `SITE_CSS`／`QUIZ_CSS`／`SITE_JS`／`QUIZ_JS` 四個常數是用**標記字串**
從 `recursion.html` 與 `searching_sorting.html` 抽出來的（本 repo 沒有保存當初網站化的注入腳本）。
不綁行號，那兩頁重排也不會壞。

## 新增一頁的流程

產出物落在 `SCRATCH = /tmp/.../scratchpad/cppsite/`：`gen_<stem>.py`、`body_<stem>.html`、
`js_<stem>.js`、`out_<stem>.json`（`run_cpp` 的實跑輸出，重跑很貴）。撰寫規格見該目錄的 `SPEC.md`。

```bash
cd SCRATCH && python3 gen_<stem>.py && python3 assemble.py <stem> <file>.html "<title>"
cd ~/ds-cpp-selfstudy
# 在 tools/apply_zh.py 的 FC 與 BQ 補上這一頁
python3 tools/inject_prereq_cpp.py && python3 tools/apply_zh.py
python3 tools/check_links_cpp.py
python3 ~/ds_cpp/Slides/tools/check_selfstudy.py <file>.html
```

## 踩過的坑

1. **`FC`／`BQ` 的條目必須跟頁面同批進 commit。** `apply_zh.py` 對每個 `FC` key 無條件讀檔並
   assert，先加會讓腳本一路中斷。
2. **`apply_zh.py` 的 `re.subn` 不能用 f-string 當替換字串。** 資料裡 `sanitize_js` 產生的
   `\uXXXX` 會被 `re` 當成模板跳脫，Python 3.13 直接拋 `bad escape \u`。已改用 `lambda`。
3. **badge 措辭要分流。** `ch*`（課程題庫）沿用原本的「課程題庫 chN · N 題」，先備頁才用
   「隨堂自測」。直接套姊妹站的腳本會靜默改寫既有三頁。
4. **`.cmp-table` 的 `th` 是深藍底白字，而 `code` 預設也是深藍字** —— 表頭裡放 `<code>` 會看不見。
   注入器的 `PRE_CSS` 已補覆寫規則。`searching_sorting.html` 還有一個未修的舊案例。
5. **`Player` 動態更新的文字不能用 `$…$`**，MathJax 不會重新排版，要寫成 `<code>O(n)</code>`。
   靜態內文可以用。
6. **f-string 裡的單大括號會被當成運算式**，程式碼範例含 `{` 要寫成 `{{`。
7. **`check_selfstudy.py` 只掃 `<pre>`、`.pseudo-code`、`<script>` 的 Python 殘留**
   （`def ` `self.` `None` `elif` `print(`），**散文不掃**。所以 Python↔C++ 對照放在
   `.cmp-table` 表格裡零成本，做成並排程式碼區塊才要插空 span 打斷。
8. **`hl()` 一定要輸出 `data-l`**（2026-08 已修）。頁面的 `hlLine(rootId, n)` 是用
   `.line[data-l="n"]` 找行的，少了它高亮會**靜默失效**。既有九章是手寫 `data-l` 所以看不出來。

## 已知待辦

- **P7 與 P8 沒有 `.viz-panel` 互動元件。** P8 最適合的題材是建構式多載的解析過程，
  P7 則是 `try`／`catch` 的執行路徑。
- `searching_sorting.html` 表頭裡的 `<code>put</code>` 看不見（同上第 4 點，兩站都有）。
- 全站在 375px 寬會橫向溢位 —— 這是既有特性，九章正課頁本來就這樣，不是新頁引入的。
- `enrich_search.py` 目前是手工把 C++ 翻成 Python 模擬跑來取得逐 pass 輸出。
  有了 `run_cpp()` 之後可以簡化，但會動到既有頁面，沒做。
