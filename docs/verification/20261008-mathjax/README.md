# 第 4–9 章 MathJax 實際排版（2026-10-08）

`check_mathjax.py` 以真實網路載入 MathJax CDN，展開所有 details 後等待 `MathJax.typesetPromise()`，統計 `mjx-container`、`mjx-merror`，以及正文（排除 pre/code/script）裡殘留的 `$…$`。

結果（`mathjax-results.json`）：六頁 MathJax 都載入，排版錯誤 0，殘留 `$` 0，page error 0。
`trees-aligned.png` 實際檢視 AVL 高度推導；另核對 $N_h=F_{h+3}-1$ 在 h=0..3 得 1、2、4、7，與圖說一致。
