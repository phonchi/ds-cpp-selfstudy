# 接力文件（ds-cpp-selfstudy）

姊妹站是 [`ds-python-selfstudy`](https://github.com/phonchi/ds-python-selfstudy)，兩站結構完全相同，
`recursion.html` 的整個 `<head>`（1–332 行）除了 `<title>` 之外逐位元組一致。改動任一站之前，
先看另一站有沒有已經解過同一個問題。

## 現況（2026-09-02）

站上共 22 頁：**三章課前準備 ＋ 九章正課 ＋ 九頁選讀先備知識**。

| 區塊 | 頁面 |
|---|---|
| 課前準備 | `00a_why_code`（為什麼還要學）、`00b_setup`（compiler + notebook）、`00c_vscode_windows`（Windows 作業） |
| 正課 | `introduction` → `trees` 九章（本次未改內容，只動了 introduction 的一行導覽） |
| 先備知識 | `p1_cpp_basics` … `p9_oop_advanced` |

先備頁合計 61 題題庫、195 張詞彙卡、16 個互動元件。**所有程式碼範例都以
`g++ -std=c++17` 實際編譯執行過**，並直接 `#include "pythonds3/cppds/…"` 引用課程的標頭檔（自 2026-09-02 起由 [phonchi/pythonds3](https://github.com/phonchi/pythonds3) 的 `cppds/*.hpp` 發布，學生 `git clone` 到啟動 Jupyter 的目錄；舊的 `dscpp/` 已全數移除）。

課程 notebook 需要打過 `-I.` patch 的 C++ kernel：
[phonchi/jupyter-cpp-kernel @ nsysu-math208](https://github.com/phonchi/jupyter-cpp-kernel/tree/nsysu-math208)
（fork 自 shiroinekotfs，MIT）。與上游的差異見下方「kernel fork 現況」；PyPI 原版缺 `-I.`，`#include "pythonds3/cppds/…"` 會找不到檔案。
安裝方式見 00B —— 注意該套件**沒有宣告任何相依**，要先自己裝 `jupyterlab`。

### 00B / 00C Windows 工具鏈契約（2026-09-02）

- 00B 完整保留 Jupyter + patched C++ kernel 教學，但用途改為 notebook；Windows 作業首選 00C 的 VS Code 流程。
- 00B 並列 MSYS2 UCRT64 與 WinLibs，兩者都必須能通過 `where.exe g++`、`where.exe gdb`、版本檢查；WSL 是進階選讀，Dev-C++ 可應急但不推薦。
- 00C 的 `tasks.json.command`、`launch.json.miDebuggerPath`、`c_cpp_properties.json.compilerPath` 必須指向同一套工具鏈。三個 JSON 區塊有固定 `id`，驗證腳本可抽出解析。
- 多檔範例只用匿名 `main.cpp`／`MyClass.cpp`，不揭露未發布作業；一般規則是 include header、明列來源檔，但教師模板若已 include 支援 `.cpp`，不可再重複編譯它。

### Windows 學生環境這一輪（2026-09-02）

學生（Windows + Anaconda + winlibs）實際回報後補的東西：

- **00B 新增**：PART 01 警告框「Anaconda Prompt 啟動 Jupyter 會載到 conda 的舊 `libstdc++-6.dll`」
  （症狀：對話框「無法找到程序輸入點 …seekpos…」；診斷 `where.exe libstdc++-6.dll`；修法 `activate.d\mingw64.bat`）；
  PART 01 `<details>` RISE 備註（Notebook 7 要 `jupyterlab_rise`，Ctrl+R）；FAQ ⑦（同 libstdc++）、⑧（`ERR_FILE_NOT_FOUND`，
  `file:///` 網址改貼終端機的 localhost URL）。FAQ 標題改為「六個 kernel 的、兩個 Windows 環境的」。
- **標頭路徑遷移** `dscpp/` → `pythonds3/cppds/`：自學站 22 頁 + `tools/enrich/`、`~/ds_cpp/Slides`（notebook、匯出 html、
  `tools/selfstudy_builders/`）、課程站 `static_files/presentations/`（含小寫自學頁鏡像，**那些頁不是本站的逐位元組鏡像**，
  只能就地替換不能覆蓋）。敘述中「dscpp 的 X」一律改「課程標頭的 X」；站內 `cppds` 一詞另指 Runestone 教科書（`cppds §8.x`），
  指標頭時寫「課程標頭」或完整路徑。**Slides 的 10 個 .pdf 未重做，仍印舊路徑。** include guard 仍叫 `DSCPP_*`，未改。
- **教材取得（學生零額外下載）**：學生只下載每週 .ipynb。課程標頭 `pythonds3/cppds/*.hpp` **內建在 kernel 套件**
  （`jcppkernel/resources/pythonds3/cppds/`，編譯自動加 `-I<resources>`，`-I.` 仍優先）；測驗與詞彙卡的 `path` 直接指向
  `https://raw.githubusercontent.com/phonchi/nsysu-math208/refs/heads/main/extra/{questions/chN,flashcards}/`，與上學期 Python 版相同。
  **標頭有兩份**：canonical 在 github.com/phonchi/pythonds3 的 `cppds/`（終端機／VS Code 用），kernel 內是複本，改標頭要兩邊都推。
  曾短暫放過 `quiz_data.zip`，已移除。
- **quiz JSON 去破折號**：`questions/`、`flashcards/` 的 13 個「—」換成 ASCII，因為 jupyterquiz 讀檔不指定 encoding，繁中 Windows
  以 cp950 解會炸。之後題目若要加中文：在 C++ kernel 下跑靠 kernel.json 的 `PYTHONUTF8=1`（見下）；用 Python kernel（例如 `rise` 環境放投影片）則要 `conda env config vars set PYTHONUTF8=1 -n rise`。

#### kernel fork 現況（`phonchi/jupyter-cpp-kernel@nsysu-math208`，commit `23263cd`）

與上游的差異已不只一行：
1. `-I.`（原有）。
2. 暫存 .cpp 以 UTF-8 寫入、子行程輸出 `decode("utf-8", errors="replace")` —— 修 Windows cp950 導致的 `UnicodeDecodeError` kernel 崩潰。
3. 7 個 `kernel.json`：`"{connection_file}"` 去掉多餘引號（消 traitlets FutureWarning）、加 `"env": {"PYTHONUTF8": "1"}`。
4. `jcppkernel/resources/pythonds3/cppds/*.hpp` 內建課程標頭，`_compile_with_gpp` 加 `-I<resDir>`（commit `44fbc22`）。
5. `jcppkernel/python_quiz_cells.py`：講義裡 `from jupyterquiz import display_quiz` / `display_quiz(...)` /
   `display_flashcards(...)` 這類 Python 測驗 cell 由 kernel 內嵌 Python 執行並送 `display_data`，notebook 不用改。
   辨識是保守白名單（每行都得是 import／字串賦值／display 呼叫／註解，且至少一行 import 或 display），其他一律走 g++。
   `path` 變數跨 cell 存活。jupyter_client 實測 10/10；**瀏覧器互動性未實測**（環境無瀏覽器）。
   已知：重開已存檔的 notebook 時 output 為 untrusted，要重跑該 cell 才會互動（與一般 ipykernel 行為相同）。
   需另裝 `pip install jupyterquiz jupytercards`（00B 安裝指令已加）。

學生端重裝（`kernel.json` 走 `data_files`，一般 upgrade 不會覆寫）：
```
pip install --force-reinstall --no-deps "git+https://github.com/phonchi/jupyter-cpp-kernel.git@nsysu-math208"
pip install jupyterquiz jupytercards
jupyter kernelspec list   # cpp17 應在 sys.prefix\share\jupyter\kernels；%APPDATA%\jupyter\kernels\cpp17 是舊殘留，刪掉
```

姊妹站 `ds-python-selfstudy`：RISE 備註與 `ERR_FILE_NOT_FOUND` 兩則同樣適用其 setup 頁，尚未同步；libstdc++ 與標頭遷移不適用。
- `assets/00c/` 的三張官方 VS Code 截圖需和 `README.md` attribution 同步保存；不得以熱連結替代。
- `.github/workflows/check-00c-windows.yml` 是 Windows 真實工具鏈 gate：MSYS2 UCRT64、GCC、GDB、`-lgdi32` 與三種匿名專案模式都必須通過。

## 工具鏈與它們的契約

| 腳本 | 做什麼 | 冪等靠什麼 |
|---|---|---|
| `tools/apply_zh.py` | 從 `data/` 重生各頁的 `const FLASHCARDS` 與 `<section id="bankquiz">` | 整段以邊界重生 |
| `tools/inject_prereq_cpp.py` | 課前章與先備頁的尾段注入（導讀框、bankquiz 錨點、詞彙卡區、上下頁導覽、CSS/JS、補 MathJax） | `<!-- prereq-injected -->` 標記 |
| `tools/check_links_cpp.py` | 錨點、站內連結、注入前置條件、Python 殘留 | — |
| `tools/check_00c.py` | 00C JSON／圖片／未發布內容守門，並以 g++ 編譯三種匿名專案模式 | — |
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

- `searching_sorting.html` 表頭裡的 `<code>put</code>` 看不見（同上第 4 點，兩站都有）。
- 全站在 375px 寬會橫向溢位 —— 這是既有特性，九章正課頁本來就這樣，不是新頁引入的。
- `enrich_search.py` 目前是手工把 C++ 翻成 Python 模擬跑來取得逐 pass 輸出。
  有了 `run_cpp()` 之後可以簡化，但會動到既有頁面，沒做。

---

## 深色底對比（2026-08-29）

`base.css` 的 `code{color:var(--accent2)}`（#2c3e7a）與 `strong{color:var(--ink)}`（#1a1a2e）
只要落進深色底容器就會消失。本站清查出 **62 處**，最嚴重的兩類是
`.info-box .info-label` 與表頭裡的 `<code>`——底色也是 #2c3e7a，**對比 1.00，完全同色**；
以及 `.status-banner` 裡的 `<strong>`（1.07，`introduction.html` 那個 `int` 就是）。

修正放在每頁 `</head>` 之前一個帶成對標記的 `<style>`（`<!-- contrast-fix v1 -->`），
由 `tools/contrast_fix.py` 冪等維護。**它完全不碰既有的 `<style>` 區塊**——
本站 CSS inline 在每頁而且有 8 種複本，靠層疊順序取勝就不必管複本差異。
`tools/inject_prereq_cpp.py` 在 MARKER 檢查之前呼叫 `contrast_fix.ensure()`，
所以新頁自帶修正、舊頁重跑也會回填。
`PRE_CSS` 裡原本那條 `.cmp-table th code` 變成惰性重複，留著不動。

`tools/check_contrast.py` 是守門員，**驗的是 CSS 合約不是內容**：
最嚴重的案例是 `setStatus()` 執行時才生出 `<strong>`，靜態走 DOM 看不到。
它掃出所有深色底選擇器，逐標籤確認被覆寫區塊涵蓋。改 CSS 之後記得跑它。

`tools/contrast_fix.py` 與 `tools/check_contrast.py` **與 `ds-python-selfstudy` 逐位元組相同**，
改一邊要記得同步另一邊（跟 `check_links_*.py` 一樣的雙胞胎慣例）。

**還沒處理的**：幾個容器自身的白字就已經不合格——`#fff` on `#d68910` = 2.82、
on `#8e44ad` = 4.42、on `#5b7eb8` = 4.10。這批修正只讓行內元素追平容器，
沒讓它們更差，但那幾個色票本身該另案調整。

---

## 視覺化全面 refine（2026-09-01）

使用者回饋「有些撥放太快、有些沒意義」後的一輪全站整修（21 個 HTML 全動到，
精確行數見這個 commit 的 diff stat）。

### player-v2（`tools/upgrade_player.py`）

17 頁 byte-identical 的 `class Player`（v1，寫死 700ms、無暫停）已由
`tools/upgrade_player.py` 冪等替換成 v2：成對 JS 註解標記
`/* player-v2 */ … /* /player-v2 */`，首次替換前 md5 核對 v1 原文（e885dbe62cca），
不符即 abort。v2 向下相容 v1 全部 API，新增 `pause()`／`playing`／`toggle(btn)`
（▶/⏸ 文字自動切換）／`setDelay(ms)`；`play()` 每 tick 重讀 `delayInput.value`，
滑桿拖了即時生效。graphs.html 原本沒有 Player，用 `--inject graphs.html` 注入同一區塊。
trees.html（Player B 變體，自帶 setDelay）與 searching_sorting.html（Animator）**不在
替換範圍**，SKIP 清單寫在腳本裡。升版 v2 時改 NEW_BLOCK 再重跑即可整段換新。

### 控制項慣例（新頁照抄）

每個 Player 實例的 controls-bar 標配：`▶`／`→ 單步`／`⏸ 暫停`
（`onclick="xxPlayer &amp;&amp; xxPlayer.toggle(this)"`，屬性裡 `&&` 必須寫實體）／
速度滑桿 `id="xxSpeed"`（range 120–1200，教學類預設 650）＋建構呼叫帶
`delayInput: $('xxSpeed')`。實例變數一律外層 `let xxPlayer = null;`，
⏸ 靠 `xxPlayer &&` 守衛在未播放時安全 no-op。

### 這輪動過的東西

- **27 個 Player 實例**全數補上 ⏸＋滑桿（11 頁）；trees 的 nrPlay/delPlay 補滑桿接
  setDelay；searching_sorting 四個排序預設 350/300→500；mazeSpeed 預設 180→300。
- **裸 timer 全數接上 Player**：arrays mdWalk（原 260ms 無控制）、linear_structures
  introDemo、p4 nodeTraverse、graphs 的 tsRunDFS/tsOrder/sccStep1/sccStep3。
  全站已無動畫用裸 setInterval。
- **11 處「過程無資訊量」的動畫改靜態**（數據都從原 frames 產生器抄出、非手寫）：
  introduction typeBtns/colDemo/fnDemo/frCalc、analysis sumcmpRun/hashRace、
  linear_structures s2Race/printerRun、p6 ordPlayer/brkLookup、p9 ltPlayer、
  recursion spiral（改一次畫完）。
- **P7/P8 補上第一個互動元件**（原待辦）：p7 excPlayer（try/catch 執行路徑＋stack
  unwinding）、p8 ovlPlayer（建構式多載解析，四種呼叫各 6 frames）。
- **7 張 inline SVG 圖解**（站內維持零 `<img>`，藍本是 `~/cppds/_sources/*/Figures/`
  與 `~/ds_cpp/Slides/imgs/`）：introduction 電路圖（gateRun 升級成 SVG、select
  onchange 即時重算）＋Fraction 深相等圖、p2 流程控制總圖、p4 指標語意×2、
  p5 擴容四格、linear_structures stack 單端進出＋全括號法。SVG 慣例：`viewBox`＋
  `style="max-width:100%;height:auto"`；**顏色變數必須寫在 style 屬性**
  （`fill="var(...)"` 這種 presentation attribute 不解析）；marker id 加頁面前綴。

### codex 審查後補的四個修正（同步姊妹站時會踩一樣的坑）

- **reset 類 handler 必須把 player 設回 null**，不能只 pause——frames 的 closure
  抓著已被清空的狀態（graphs 的 `tsClose`/`sccCloseT`），重設後按 ⏸/單步會喚醒殭屍。
  見 `tsReset`/`sccReset`/`sccStep2` 的寫法。
- **▶ handler 重建 player 前先 `pause()` 舊實例**，否則連按 ▶ 會留下失控的 timer
  （`introStart` 已修）。注意：**既有約 25 個實例的重建沒有這個守衛**，那是上線前就有的
  行為（連按 ▶ 會短暫交錯），這輪刻意只修新寫的程式碼，沒有回頭整批加。
- **動畫播放中改資料要先停 player**（p4 `nodeAdd` 已修），否則 frames 快照與畫面對不上。
- **v2.1 語意**：`onDone` 播畢只觸發一次；播畢後按 ⏸ ＝ 從頭重播（按鈕文字同步）。
- **v2.2（codex 二審後）**：Player 在 `toggle(btn)` 記住按鈕（`_btn`），之後
  `play()`/`pause()`（含單步、自然播畢）都經 `_sync()` 同步 ▶/⏸ 文字；
  p8 淘汰幀改為「先定生死再入幀」，畫面與訊息同幀。二審也確認全部 marker/id
  無衝突、p7/p8 frames 正確。

### 姊妹站待同步

`ds-python-selfstudy` 的 Player v1 應該也是同一份（先驗 md5）。`upgrade_player.py`
可直接搬過去；其餘（滑桿補齊、改靜態、SVG）是逐頁語意編輯，要照本節清單重做一輪。
