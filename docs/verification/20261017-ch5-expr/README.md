# 第 5 章：運算式動機、轉換補充、[ ] 標示、deque 實作（2026-10-17）

修改：`tools/enrich/content/linear_depth.py`、`tools/enrich/content/linear_programs.py`，經 `docs/verification/20261008-ch5/pipeline.sh` 重建 `linear_structures.html`（gen 區內，無手改）。

新增內容：
- #infix 正文：h3「為什麼需要前序與後序」（比較表、後序 O(n) stack 求值、應用表、連到 trees.html#parse-tree）；Shunting-yard 一段。
- #infix 收合（補充）：isalnum(token[0]) 與空白、stod、h3「其他轉換與前序求值」下四個 fold（後序轉中序、前序轉中序、中序轉前序〔反轉＋Shunting-yard，`>`〕、前序求值）。
- #stack、#queue info-box：[ ] 表示法要標 top/base、front/rear；qStack1、qQueue 回饋補方向；recap 加兩條。
- #deque 收合（補充）：std::deque 區塊＋索引表、std::queue 底層、環狀陣列。

驗證（`run.log`）：
- pipeline 跑兩次 sha256 相同。
- `check_content.py`：23 個 run 區塊全部編譯（-Wall -Wextra -pedantic 無警告）且輸出相符，0 錯誤；新 6 支程式含其中。另以 `>=` 版 infixToPrefix 實測得 `- A - B C`（正文所述錯誤結果）。
- `check_links_cpp.py` 0/0、`check_contrast.py` 0 失敗。
- `check_browser.py` 1440／390：40 個 details、16 圖、15 案例播放、16 quiz、無溢出、無 page error。
- `shots.py` 截圖 `new-*.png`（人工檢視過）。

限制：deque 示意 pre 的中文標題字寬不等，但格子與箭頭對齊；窄螢幕下 pre 與對照表需橫向捲動。MathJax 未在瀏覽器測試中載入。

潤稿（speak-human-tw，使用者確認 6 條全改）：stack info-box、Shunting-yard 側線比喻、isalnum 轉場、中序轉前序設問、deque 攤銷常數時間與 push_back 句序。套用後重跑 pipeline（兩次 sha256 相同）與上列全部檢查，結果不變。
