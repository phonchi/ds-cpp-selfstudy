# 接力狀態（先備頁移植到 ds-cpp-selfstudy）

任何 session／subagent 接手前先讀這份，再讀
`~/.claude/plans/https-phonchi-github-io-scicomp-python-dazzling-wilkinson.md`（完整計畫）。

## 目標

把 `ds-python-selfstudy` 已上線的 11 個頁面（課前章 00A/00B ＋ 先備頁 P1–P9）
改寫移植到本 repo。**不是翻譯，是改寫**：結構與教學設計沿用，程式碼範例 100% 重寫成
C++ 並實際編譯執行過。

## 已完成（已 commit）

| commit | 內容 |
|---|---|
| `b67a6f7` | 工具：`inject_prereq_cpp.py`、`check_links_cpp.py`、`apply_zh.py` 三項修正、`enrich_lib.run_cpp()`、`.nojekyll` |
| `f27e006` | 課前準備 00A、00B；`index.html` 課前準備區；`introduction.html` 上一章接到 00B；README |
| `ae4149e` | 先備頁 P4（陣列、指標與動態記憶體）＋ 四個互動元件 |

## 進行中

| 頁 | stem | 狀態 |
|---|---|---|
| P8 物件導向（基礎） | `p8_oop_basics` | body 已組進 repo，**尚缺** `data/flashcards_zh/p8.json`、`data/questions_zh/p8.json`、FC/BQ 登記 |
| P9 物件導向（進階） | `p9_oop_advanced` | **未開始**（主 session 負責） |
| P1 C++ 基礎與編譯流程 | `p1_cpp_basics` | subagent 撰寫中 |
| P2 流程控制 | `p2_flow_control` | subagent 撰寫中 |
| P3 函式 | `p3_functions` | subagent 撰寫中 |
| P5 vector 與 string | `p5_vector_string` | subagent 撰寫中 |
| P6 map、set 與迭代器 | `p6_map_set` | subagent 撰寫中 |
| P7 檔案與例外 | `p7_files_exceptions` | **未開始** |

## 產出物在哪（這就是復原點）

subagent 的成果一律落在磁碟，不在對話裡：

```
SCRATCH = /tmp/claude-1000/-home-phonchi-ds-python/fba5eac3-b026-4053-96ab-a966384bd16d/scratchpad/cppsite/
  SPEC.md            撰寫規格（所有 subagent 的共同依據）
  head.frag          頁面 <head>（自 recursion.html 1–332 行擷取）
  sharedjs.frag      共用 JS（$ / quizCheck / hlLine / Player / setStatus / setupNav）
  assemble.py        組頁：head.frag + body_<stem>.html + sharedjs.frag + js_<stem>.js
  gen_<stem>.py      各頁的 body 產生器
  body_<stem>.html   產生出來的 body
  js_<stem>.js       各頁的互動元件
  out_<stem>.json    run_cpp() 跑出來的真實輸出（重跑很貴，別弄丟）

repo 內：
  data/flashcards_zh/<stem>.json
  data/questions_zh/<stem>.json
```

**只要 `gen_<stem>.py` 與兩個 JSON 還在，那一頁就救得回來**，不必重寫。

## 一頁完成的固定流程

```bash
cd SCRATCH && python3 gen_<stem>.py                      # 產生 body
python3 assemble.py <stem> <file>.html "<title>"          # 組頁進 repo
cd ~/ds-cpp-selfstudy
# 在 tools/apply_zh.py 的 FC 與 BQ 補上這一頁（要跟頁面同批 commit，先加會讓腳本中斷）
python3 tools/inject_prereq_cpp.py                        # 注入導讀框／詞彙卡區／上下頁導覽
python3 tools/apply_zh.py                                 # 從 data/ 灌入字卡與題庫
python3 tools/check_links_cpp.py                          # 錨點與連結
python3 ~/ds_cpp/Slides/tools/check_selfstudy.py <file>.html   # Python 殘留 gate
```

## 尚未做的收尾

1. `index.html` 補 `<section id="prereq">`（九張先備頁卡片）——**所有 P 頁齊了才做**，
   否則會連到不存在的頁面。現在 00A/00B 的導讀框已經指向 `index.html#prereq`，那個錨點還不存在。
2. README 補先備頁表格。
3. 全站驗收：冪等重跑、`check_links_cpp.py` 0 錯誤、headless Chrome dump-dom 確認元件渲染、
   既有九章正課頁除 `introduction.html` 一行 nav 外零 diff。
4. 尚未 push。

## 踩過的坑（別重犯）

- `apply_zh.py` 的 `FC`／`BQ` 條目**必須跟頁面同批進 commit**，先加會讓腳本找不到檔案而中斷。
- `.cmp-table` 的 `th` 是深藍底白字，而 `code` 預設也是深藍字 —— 表頭裡放 `<code>` 會看不見。
  注入器的 `PRE_CSS` 已補上覆寫規則。
- `Player` 動態更新的文字裡不能用 `$…$` 數學式，MathJax 不會重新排版，要寫成 `<code>O(n)</code>`。
- f-string 裡的單大括號會被當成運算式，程式碼範例含 `{` 要寫成 `{{`。
- `check_selfstudy.py` 掃 `<pre>`／`.pseudo-code`／`<script>` 裡的 Python 殘留
  （`def ` `self.` `None` `elif` `print(`），散文不掃。Python↔C++ 對照建議一律用表格。
