# 任務：第 7 章教學頁的正確性審閱（唯讀）

## 背景

`/home/phonchi/ds-cpp-selfstudy` 是大學「資料結構（C++）」的自學教學網站。第 7 章頁面是 `searching_sorting.html`（搜尋、雜湊、六種排序）。頁面內容由產生器產生：

- `tools/enrich/content/search_depth.py`：各節組裝、重點回顧
- `tools/enrich/content/search_more.py`：補充段落與（補充）收合區
- `tools/enrich/content/search_legacy.py`：手寫的說明、側欄、比較表、資料結構對照表（`#depends`）、補充 A／B
- `tools/enrich/content/search_programs.py`：頁面上的 C++ 程式與預期輸出
- `tools/enrich/content/search_quizzes.py`：頁內 quiz
- `data/flashcards_zh/ch7.json`、`data/questions_zh/ch7.json`：詞彙卡與章末題庫

課程依據（頁面應與它們一致）：

- 講義：`/home/phonchi/ds_cpp/Slides/07_Searching and Sorting.ipynb`
- 課程標頭：`/home/phonchi/ds_cpp/Slides/pythonds3/cppds/searching.hpp`、`hashtable.hpp`、`sorting.hpp`

頁面規則：講義範圍內的內容放正文；超出講義的內容放在標題帶「（補充）」的 `<details>` 收合區。收合區一樣是給學生讀的，正確性要求相同。

## 要做什麼

找出頁面上（正文與所有收合區）**會讓學生學錯**的地方：

- 錯誤或不精確的時間／空間複雜度、比較次數、推導
- 演算法行為的錯誤描述，或和課程標頭實際程式不一致的說法
- C++ 語言與標準函式庫的錯誤說法
- 錯誤的數字、範例、程式輸出、quiz 正解或回饋、詞彙卡定義
- 表格裡的判斷（✓、△、✗、穩定與否等）是否站得住
- 同一頁不同地方互相矛盾的說法

使用者特別提出一個例子，請一併判斷：`#depends` 收合區的表「對照表：每個演算法需要的資料結構」把氣泡排序、選擇排序在 Linked List 上標成「△ 慢但可」，插入排序標成「△ 變體可行」。使用者質疑這些標示是否正確，因為這三種排序都能用循序走訪實作。請檢查這一列以及整張表、該節其他說法。

不要回報純措辭、風格或排版問題，除非它改變了意思。

## 限制

- **唯讀**：不要修改任何檔案。需要驗證時可以在記憶體中跑 Python，或推導、舉反例。
- 頁面很大。取可見文字的方法（保留 details 摘要，去掉 style／script）：

```bash
cd /home/phonchi/ds-cpp-selfstudy && python3 - <<'EOF'
from bs4 import BeautifulSoup
s = BeautifulSoup(open('searching_sorting.html').read(), 'html.parser')
for t in s(['style', 'script']): t.decompose()
print(s.get_text('\n'))
EOF
```

  公式是 MathJax 原始碼（`$…$`）。也可以直接讀產生器原始碼。

## 回覆格式（繁體中文）

1. **發現**：依嚴重度排序（錯誤 → 誤導 → 不精確）。每一條寫：
   - 位置：節（section id 或標題）＋引用原句；能找到的話附產生器的 `檔案:行號`
   - 頁面的說法
   - 為什麼不對：推導、反例、標準條文或課程程式的依據
   - 建議改成什麼
   - 信心（高／中／低）
2. **檢查過、確認正確的重點**：簡短列出，讓人知道涵蓋範圍。
3. **沒檢查到的部分**（如果有）。
