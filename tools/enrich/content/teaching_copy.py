"""Reviewed wording for preserved chapter sections, applied on regeneration."""
EDITS = {'arrays': [('。攤平索引 0,1,2,…連續前進：cache line 一路吃到飽。', '。攤平索引 0,1,2,…連續前進，有利於利用快取。'),
            ('10¹⁰ × 4B = 40GB，記憶體先陣亡。', '10¹⁰ × 4B = 40GB，需要大量記憶體。'),
            ('先看正面術語，心中默想定義再翻面對答案；洗牌後再過一輪，直到每張都能不假思索說出來。', '先看正面術語，試著說出定義，再翻面核對；不熟的詞可以洗牌後再練習。')],
 'linked_lists': [
                  ('先看正面術語，心中默想定義再翻面對答案；洗牌後再過一輪，直到每張都能不假思索說出來。',
                   '先看正面術語，試著說出定義，再翻面核對；不熟的詞可以洗牌後再練習。')],
 'linear_structures': [], 'recursion': [], 'searching_sorting': [], 'graphs': [], 'trees': []}

def polish_preserved(page, text):
    for old, new in EDITS[page]:
        text = text.replace(old, new)
    return text
