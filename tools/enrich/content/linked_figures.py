"""Selected pointer diagrams placed beside the operations they explain."""
import re
from html import escape

FIGURES = [
    {
        'id': 'add', 'file': 'add_list.png', 'width': 620, 'height': 187,
        'anchor': '只有入口切換，後段不必搬移。',
        'alt': '原串列為93、17、77、31；步驟1讓新節點26的next指向93，步驟2讓head指向26。',
        'caption': '從 93 → 17 → 77 → 31 開始插入 26：先把 temp 的 next 接到 93，再讓 head 指向 26。兩步完成後，原來的後段仍完整連在新節點後面。',
    },
    {
        'id': 'remove', 'file': 'remove_unorder_list3.png', 'width': 680, 'height': 150,
        'anchor': 'delete 之後不能再讀 current 的欄位。',
        'alt': '原串列54、26、93、17、77、31；previous位於93，current位於17，93的next跨過17接到77。',
        'caption': '這張圖從 54 → 26 → 93 → 17 → 77 → 31 刪除 17：previous 位於 93，current 位於 17。讓 93 的 next 改指向 77，串列便跳過 17；接好後再釋放 17 的節點。',
    },
    {
        'id': 'sentinels', 'file': 'double_list.png', 'width': 1100, 'height': 193,
        'anchor': '走訪停在 trailer，不能把哨兵當資料讀取或刪除。</p>',
        'alt': 'header與trailer哨兵之間依序是54、26、93，每個資料節點有prev、data、next，鄰居以雙向箭頭連接。',
        'caption': '資料節點依序為 54、26、93，左右另有 header 與 trailer 哨兵。每個資料節點都有前後兩個鄰居；刪除第一項或最後一項時，也能把兩側鄰居接回。哨兵本身不代表資料。',
    },
]

STYLE = '''<style id="linked-figures-style">
.linked-figure{margin:1rem 0 1.4rem;max-width:100%;}
.linked-figure-scroll{max-width:100%;overflow-x:auto;background:#fff;border:1px solid var(--card-border);border-radius:8px;}
.linked-figure img{display:block;height:auto;max-width:none;width:var(--figure-width);margin:0 auto;}
.linked-figure figcaption{margin-top:.65rem;font-size:.9rem;line-height:1.8;color:var(--ink);}
</style>'''


def apply_figures(page):
    page = re.sub(r'<!-- linked-figure:[^>]+ -->.*?<!-- /linked-figure -->', '', page, flags=re.S)
    for spec in FIGURES:
        anchor = spec['anchor']
        if page.count(anchor) != 1:
            raise ValueError(f"Expected one figure anchor for {spec['id']}")
        figure = (f'<!-- linked-figure:{spec["id"]} -->'
                  f'<figure class="linked-figure" id="linked-figure-{spec["id"]}">'
                  f'<div class="linked-figure-scroll" tabindex="0" role="region" aria-label="{escape(spec["alt"], quote=True)}">'
                  f'<img src="assets/figures/ch4/{spec["file"]}" alt="{escape(spec["alt"], quote=True)}" '
                  f'width="{spec["width"]}" height="{spec["height"]}" style="--figure-width:{spec["width"]}px" loading="lazy"></div>'
                  f'<figcaption>{spec["caption"]}</figcaption></figure><!-- /linked-figure -->')
        page = page.replace(anchor, anchor + figure, 1)
    page = re.sub(r'<style id="linked-figures-style">.*?</style>', '', page, flags=re.S)
    return page.replace('</head>', STYLE + '</head>', 1)
