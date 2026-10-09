# 子任務說明：speak-human-tw 潤稿（第 4–9 章）

Repo：`/home/phonchi/ds-cpp-selfstudy`，是給學生自學的繁體中文 C++ 資料結構教學網站。
先讀 repo 的 `AGENTS.md`，以及 `HANDOFF.md` 開頭的「第四到九章依講義擴充」一節。

## 任務
用 Skill 工具載入 `speak-human-tw`，對你負責的章節做整頁潤稿，範圍是學生可見的中文文字。

使用者已選擇「**跳過確認、事後摘要**」模式，所以直接套用，不要停下來等回覆。這一點已經使用者明確授權。

情境定為教學文件：力度中等，維持教學語域，不改成聊天口吻。

## 只改產生器來源，不直接改 HTML
各頁 HTML 由產生器重建。文字來源：

| 章 | 頁面 | 來源檔 | 重建腳本 |
|---|---|---|---|
| 4 | `linked_lists.html` | `tools/enrich/content/linked_depth.py`、`linked_figures.py`（圖說） | `docs/verification/20261008-ch4/pipeline.sh` |
| 5 | `linear_structures.html` | `tools/enrich/content/linear_depth.py`、`linear_figures.py` | `docs/verification/20261008-ch5/pipeline.sh` |
| 6 | `recursion.html` | `tools/enrich/content/recursion_depth.py`、`recursion_figures.py`、`recursion_widgets.py`（面板說明文字） | `docs/verification/20261008-ch6/pipeline.sh` |
| 7 | `searching_sorting.html` | `tools/enrich/content/search_depth.py`、`search_legacy.py`、`search_figures.py`、`search_quizzes.py` | `docs/verification/20261008-ch7/pipeline.sh` |
| 8 | `graphs.html` | `tools/enrich/content/graphs_depth.py`、`graphs_figures.py` | `docs/verification/20261008-ch8/pipeline.sh` |
| 9 | `trees.html` | `tools/enrich/content/trees_depth.py`、`trees_legacy.py`、`trees_figures.py`、`trees_quizzes.py` | `docs/verification/20261008-ch9/pipeline.sh` |

- 字卡在 `data/flashcards_zh/chN.json`；第 7–9 章的章末題在 `data/questions_zh/chN.json`。這兩種也可以潤稿。
- 少數文字在 gen 區之外，例如 h2 標題、使用方式框、主 script 裡動畫狀態列的訊息。
  - h2、使用方式框這類 HTML 可以直接改頁面，因為不會被重建覆蓋。
  - 主 script 的字串一律不要動。
- 第 4 章的動畫訊息在 `content/linked_interactions.js`，可以只改其中的中文說明。

## 保護清單（原封不動）
- 程式碼：`.pseudo-code`、`pre`、`<code>` 的內容，以及 Python 字串裡的 C++ 程式。
- 預期輸出。
- 數字與公式（`$…$`）。
- 函式、類別、標頭名稱與英文術語。
- 連結網址、id、class、`data-*` 屬性。
- 「（補充）」「（上課略過）」這類標示。
- 「講義 0N ·」這種程式卡標籤。
- quiz 的正確答案與選項的意思（只能調整措辭）。

## 重點
- 去掉 AI 腔，包括：
  - 誇張比喻；
  - 「不是 A，而是 B」連用；
  - 「值得注意的是」這類空泛導引句；
  - 三段式湊數；
  - 過多的破折號與粗體；
  - 罐頭結論。
- 校正中國用語與半形標點（中文句子用全形「，。：；（）」）。
- 不新增原文沒有的事實或例子。
- 不刪掉承擔教學內容的句子。
- 不寫製作歷程。

## 驗證（每章都要做）
1. 跑該章的 `pipeline.sh` 兩次，確認 `sha256sum` 相同（冪等）。
2. 跑該章的 `docs/verification/20261008-chN/check_content.py`；第 4 章改用 `DSCPP_PAGES=linked_lists python3 docs/verification/20261003-ch3-ch4/check_content.py`。程式輸出必須全部通過。
3. 保真比對：
   - 用 `git diff` 確認沒有改到程式碼區塊、輸出、數字、id、連結。
   - 寫一個小腳本，比對改前與改後頁面的所有 `.pseudo-code`、`pre`、`[data-expected]`、`href`、`id`，結果必須完全相同。
4. 執行 `python3 tools/check_links_cpp.py`，必須 0 錯誤。
5. inline script 都要通過 `node --check`。

## 產出
- 摘要寫在 `docs/verification/20261009-polish/chN-polish.md`。
  - 開頭寫總數「這次找到並修改了 N 處」。
  - 每條列：原句／為什麼要改／改成了什麼。
- 不要 commit，不要動其他章的檔案。
- 最後回報：每章改了幾處、驗證結果、任何疑慮。
