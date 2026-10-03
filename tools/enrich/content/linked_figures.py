"""Lecture pointer diagrams placed beside the operations they explain."""
import re
from html import escape

FIGURES = {
    'add': {
        'file': 'add_list.png', 'width': 620, 'height': 187,
        'alt': '原串列為 93、17、77、31；步驟 1 讓新節點 26 的 next 指向 93，步驟 2 讓 head 指向 26。',
        'caption': '從 93 → 17 → 77 → 31 開始插入 26：先把 temp 的 next 接到 93，再讓 head 指向 26。兩步完成後，原來的後段仍完整連在新節點後面。',
    },
    'wrong': {
        'file': 'add_list2.png', 'width': 640, 'height': 231,
        'alt': 'head 與 temp 都指向新節點 26；原本的 93、17、77、31 被圈起來，標示沒有外部指標可以到達。',
        'caption': '先改 head 的結果：head 與 temp 都指向新節點 26，原本的 93 → 17 → 77 → 31 被圈在 no external reference 中，沒有任何指標能到達它們。圖中 26 的 next 還是空的；接著執行 temp->setNext(head)，它就會指向自己。',
    },
    'remove': {
        'file': 'remove_unorder_list3.png', 'width': 680, 'height': 150,
        'alt': '原串列為 54、26、93、17、77、31；previous 位於 93，current 位於 17，93 的 next 跨過 17 接到 77。',
        'caption': '從 54 → 26 → 93 → 17 → 77 → 31 刪除 17：previous 位於 93，current 位於 17。讓 93 的 next 改指向 77，串列便跳過 17；接好後再釋放 17 的節點。',
    },
    'sentinels': {
        'file': 'double_list.png', 'width': 1100, 'height': 193,
        'alt': 'header 與 trailer 哨兵之間依序是 54、26、93，每個資料節點有 prev、data、next，鄰居以雙向箭頭連接。',
        'caption': '資料節點依序為 54、26、93，左右另有 header 與 trailer 哨兵。每個資料節點都有前後兩個鄰居；刪除第一項或最後一項時，也能把兩側鄰居接回。哨兵本身不代表資料。',
    },
}

STYLE = '''<style id="linked-figures-style">
.linked-figure{margin:1rem 0 1.4rem;max-width:100%;}
.linked-figure-scroll{max-width:100%;overflow-x:auto;background:#fff;border:1px solid var(--card-border);border-radius:8px;}
.linked-figure img{display:block;height:auto;max-width:none;width:var(--figure-width);margin:0 auto;}
.linked-figure figcaption{margin-top:.65rem;font-size:.9rem;line-height:1.8;color:var(--ink);}
</style>'''


def figure(fid):
    spec = FIGURES[fid]
    alt = escape(spec['alt'], quote=True)
    return (f'<figure class="linked-figure" id="linked-figure-{fid}">'
            f'<div class="linked-figure-scroll" tabindex="0" role="region" aria-label="{alt}">'
            f'<img src="assets/figures/ch4/{spec["file"]}" alt="{alt}" '
            f'width="{spec["width"]}" height="{spec["height"]}" style="--figure-width:{spec["width"]}px" loading="lazy"></div>'
            f'<figcaption>{escape(spec["caption"], quote=False)}</figcaption></figure>')


def apply_figures(page):
    """Figures are emitted inline by linked_depth; only the shared style lives here."""
    page = re.sub(r'<!-- linked-figure:[^>]+ -->.*?<!-- /linked-figure -->', '', page, flags=re.S)
    page = re.sub(r'<style id="linked-figures-style">.*?</style>', '', page, flags=re.S)
    return page.replace('</head>', STYLE + '</head>', 1)
