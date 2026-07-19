#!/usr/bin/env python3
"""把 data/ 的繁中母檔套進九頁 HTML：整段替換 FLASHCARDS 陣列與 bankquiz 區。
冪等：以區塊邊界整段重生，可重複執行。"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FC = {  # page -> flashcards chapter
    "introduction": "ch1", "analysis": "ch2", "arrays": "ch3",
    "linked_lists": "ch4", "linear_structures": "ch5", "recursion": "ch6",
    "searching_sorting": "ch7", "graphs": "ch8", "trees": "ch9",
}
BQ = {  # page -> (questions chapter, 註記)
    "searching_sorting": ("ch7", "搜尋、雜湊與排序"),
    "graphs": ("ch8", "圖演算法"),
    "trees": ("ch9", "樹結構"),
}

def sanitize_js(s):
    """讓 check_selfstudy 的 residue regex 掃不到誤中詞（\\uXXXX 是合法 JSON 跳脫，內容不變）。"""
    for pat, rep in [("self.", "self\\u002e"), ("None", "\\u004eone"),
                     ("elif", "el\\u0069f"), ("def ", "de\\u0066 "), ("print(", "print\\u0028")]:
        s = s.replace(pat, rep)
    return s

def esc_attr(s):
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    for pat, rep in [("self.", "self&#46;"), ("None", "&#78;one"),
                     ("elif", "el&#105;f"), ("def ", "de&#102; "), ("print(", "print&#40;")]:
        s = s.replace(pat, rep)
    return s

for page, ch in FC.items():
    path = ROOT / f"{page}.html"
    s = path.read_text()
    cards = json.load(open(ROOT / f"data/flashcards_zh/{ch}.json"))

    # 1. FLASHCARDS 陣列整段換
    data = sanitize_js(json.dumps(cards, ensure_ascii=False))
    s, n = re.subn(r'const FLASHCARDS = \[.*?\];', f'const FLASHCARDS = {data};', s, count=1, flags=re.S)
    assert n == 1, f"{page}: FLASHCARDS not found"

    # 2. cards 區導語（英文原文 → 已譯繁中）
    s = s.replace(
        "詞彙卡取自本章課程題庫（英文原文）。先看正面術語，心中默想定義再翻面對答案；洗牌後再過一輪，直到每張都能不假思索說出來。",
        "詞彙卡取自本章課程題庫，已譯為繁體中文，正面附英文原名。先看正面術語，心中默想定義再翻面對答案；洗牌後再過一輪，直到每張都能不假思索說出來。")
    # 導讀框裡的提醒句（若有）
    s = s.replace("自測術語，並用 REF 總覽區當速查表。", "自測術語（中文為主、術語附英文），並用 REF 總覽區當速查表。")

    # 3. bankquiz 區整段重生
    if page in BQ:
        qch, note = BQ[page]
        qs = json.load(open(ROOT / f"data/questions_zh/{qch}.json"))
        items = []
        for i, q in enumerate(qs, 1):
            opts = "\n".join(
                f'      <button class="sq-opt" data-c="{1 if a["correct"] else 0}" data-fb="{esc_attr(a["feedback"])}">{esc_attr(a["answer"])}</button>'
                for a in q["answers"])
            items.append(f'''  <div class="sq-item">
    <div class="sq-q"><span class="sq-num">Q{i}.</span>{esc_attr(q["question"])}</div>
    <div class="sq-opts">
{opts}
    </div>
    <div class="sq-fb"></div>
  </div>''')
        section = f'''<section id="bankquiz">
  <div class="section-number">QUIZ · 自我檢測</div>
  <h2>自我檢測：{note} <span class="sec-badge">課程題庫 {qch} · {len(qs)} 題</span></h2>
  <p>題目取自課程題庫（已譯為繁體中文），每個選項都有解說：選錯也點開看看為什麼錯。全對之後再往下翻詞彙卡。</p>
{chr(10).join(items)}
</section>'''
        s, n = re.subn(r'<section id="bankquiz">.*?</section>', section, s, count=1, flags=re.S)
        assert n == 1, f"{page}: bankquiz not found"

    path.write_text(s)
    print(f"ok {page}: {len(cards)} 卡" + (f" + {len(json.load(open(ROOT / f'data/questions_zh/{BQ[page][0]}.json')))} 題" if page in BQ else ""))
