"""Reviewed wording for preserved chapter sections, applied on regeneration."""
# 這幾章的詞彙卡除了課程題庫，還補了正文的關鍵術語
CARD_LEAD = [('詞彙卡取自本章課程題庫，已譯為繁體中文，正面附英文原名。先看正面術語，心中默想定義再翻面對答案；洗牌後再過一輪，直到每張都能不假思索說出來。',
              '詞彙卡涵蓋本章的關鍵術語，已譯為繁體中文，正面附英文原名。先看正面術語，試著說出定義，再翻面核對；不熟的詞可以洗牌後再練習。')]
EDITS = {'arrays': [('。攤平索引 0,1,2,…連續前進：cache line 一路吃到飽。', '。攤平索引 0,1,2,…連續前進，有利於利用快取。'),
            ('10¹⁰ × 4B = 40GB，記憶體先陣亡。', '10¹⁰ × 4B = 40GB，需要大量記憶體。'),
            ('先看正面術語，心中默想定義再翻面對答案；洗牌後再過一輪，直到每張都能不假思索說出來。', '先看正面術語，試著說出定義，再翻面核對；不熟的詞可以洗牌後再練習。')],
 'linked_lists': [
                  ('先看正面術語，心中默想定義再翻面對答案；洗牌後再過一輪，直到每張都能不假思索說出來。',
                   '先看正面術語，試著說出定義，再翻面核對；不熟的詞可以洗牌後再練習。')],
 'linear_structures': [], 'recursion': CARD_LEAD, 'searching_sorting': CARD_LEAD, 'graphs': CARD_LEAD, 'trees': CARD_LEAD}

def polish_preserved(page, text):
    for old, new in EDITS[page]:
        text = text.replace(old, new)
    return text
