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

# Display size: (file, display width, natural width, natural height); height keeps the aspect ratio.
_SIZES = {
    'scatter': ('unordered.png', 323, 269, 162),
    'linked': ('unordered2.png', 410, 342, 160),
    'node93': ('head_list.png', 246, 164, 41),
    'empty': ('head_list2.png', 600, 1200, 396),
    'chain': ('head_list3.png', 1000, 2640, 504),
    'size': ('size_list.png', 680, 541, 146),
    'search': ('search_list.png', 680, 512, 157),
    'remove-start': ('remove_unorder_list.png', 680, 521, 127),
    'remove-steps': ('remove_unorder_list2.png', 680, 545, 324),
    'remove-head': ('remove_unorder_list4.png', 680, 521, 138),
    'ordered': ('order_list.png', 680, 512, 41),
    'ordered-search': ('search_order_list.png', 680, 512, 136),
    'ordered-add': ('add_order_list.png', 680, 512, 202),
    'circular': ('circular_list.png', 900, 2400, 648),
    'd-ins-before': ('double_list2.png', 1100, 2736, 384),
    'd-ins': ('double_list3.png', 1100, 2832, 696),
    'd-ins-after': ('double_list4.png', 1100, 2832, 384),
    'd-del-before': ('double_list5.png', 1100, 2832, 384),
    'd-del': ('double_list6.png', 1100, 2832, 648),
    'd-del-after': ('double_list7.png', 1100, 2736, 384),
}

_TEXT = {
    'scatter': ('六個整數 54、26、93、17、77、31 散落在不同位置，彼此之間沒有任何連線。',
                '只看位置，這六個值像是隨意擺放：記憶體裡的相對位置沒有透露誰是第一項、誰是下一項。'),
    'linked': ('同樣六個值：Head 指向 54，接著依箭頭到 26、93、17、77，最後到標示 End 的 31。',
               '每個值多記一條「下一項在哪裡」的連結後，從 head 出發順著箭頭走，就得到 54、26、93、17、77、31 的順序。值本身的位置仍然分散，順序完全由連結決定；31 是最後一項，後面沒有下一項。'),
    'node93': ('指標 temp 指向一個節點，節點的資料是 93，next 欄位畫成接地符號。',
               'new Node<int>(93) 建立的節點：temp 存的是節點的位址，資料欄位是 93；next 由建構子設成 NULL，圖中以接地符號表示「後面沒有節點」。'),
    'empty': ('UnorderedList<int> myList; 之後，myList 物件裡只有一個 head 欄位，值是 NULL，旁邊註明 no nodes yet。',
              '剛建立的串列物件只有一個 head 欄位，值為 NULL：這時還沒有任何節點。串列物件本身不存放元素，只記住第一個節點在哪裡。'),
    'chain': ('myList 的 head 指向 54，之後依序是 26、93、17、77、31，31 的 next 指向 NULL；每個節點分成 data 與 next 兩格。',
              '六次 add 之後的串列：myList 只保存 head，head 指向資料為 54 的第一個節點；每個節點的 next 指向下一個節點，最後一個節點 31 的 next 是 NULL。'),
    'size': ('current 從 head 指向的 54 開始，依序停在 26、93、17、77、31，最後停在串列結尾的 NULL。',
             'size() 的走訪：current 每前進一次，count 就加一。current 在六個節點各停一次，走到 NULL 時迴圈結束，count 為 6。'),
    'search': ('current 依序停在 54、26、93，第四次停在 17，17 被圈起來；77 與 31 沒有被走到。',
               'search(17)：current 走過 54、26、93 都不相等，到 17 時相等，立刻回傳 true。後面的 77、31 不必再比較。'),
    'remove-start': ('previous 指向 NULL（接地符號），current 指向第一個節點 54；串列為 54、26、93、17、77、31。',
                     'remove 開始時的兩個指標：current 從 head 指向的 54 開始，previous 還沒有對應的節點，所以是 NULL。'),
    'remove-steps': ('四列圖：步驟 0 previous 為 NULL、current 在 54；步驟 1 previous 在 54、current 在 26；步驟 2 在 26 與 93；步驟 3 在 93 與 17。',
                     '尋找 17 的過程：每一步 previous 先移到 current 的位置，current 再前進一格，所以 previous 永遠落後 current 一個節點。步驟 3 時 current 停在 17，previous 正好停在要修改的前一個節點 93。'),
    'remove-head': ('previous 仍是 NULL，current 指向 54；head 原本指向 54 的箭頭改成虛線，新箭頭從 head 跨過 54 指向 26。',
                    '要刪的是第一個節點 54 時，迴圈一開始就找到目標，previous 仍是 NULL。這時沒有前一個節點可以修改，要改的是 head：讓 head 改指 54 的下一個節點 26。'),
    'ordered': ('head 依序指向 17、26、31、54、77、93，最後接地。',
                '遞增有序串列 17、26、31、54、77、93 的鏈結表示：節點與 next 的接法和無序串列相同，差別只在節點的順序由值的大小決定。'),
    'ordered-search': ('有序串列 17、26、31、54、77、93 中搜尋 45：current 依序停在 17、26、31，第四次停在 54，54 被圈起來。',
                       '搜尋 45：17、26、31 都比 45 小，繼續往後；到 54 時已經比 45 大。因為串列遞增，後面的 77、93 只會更大，搜尋可以在 54 停下並回傳 false。'),
    'ordered-add': ('在 17、26、54、77、93 中加入 31：previous 指向 26，current 指向 54，temp 指向新節點 31；Step 1 讓 31 的 next 指向 54，Step 2 讓 26 的 next 改指 31，26 到 54 的舊連結畫成虛線。',
                    '把 31 插在 26 與 54 之間。圖中以 previous、current 兩個指標標出插入點，課本的寫法也用這兩個名稱：Step 1 先讓新節點接上後段的 54，Step 2 再讓 26 改指新節點。講義的 add 只用一個 current，它停在 26，用 current->getNext() 看到 54，接線順序一樣是先接後段、再接前段。'),
    'circular': ('四個節點 54、26、93、17 依序相連，head 指向 54，tail 指向 17；17 的 next 以橘色箭頭繞回 54，標註 tail->next == head (no NULL at the end)。',
                 '環狀鏈結串列：最後一個節點 17 的 next 不是 NULL，而是指回第一個節點 54，所以 tail->next 就是 head。從任何一個節點出發，沿 next 走都會回到原點。'),
    'd-ins-before': ('header、54、26、93、trailer 以雙向箭頭相連，下方註明 before: insert 77 between 26 and 93。',
                     '插入前：準備把 77 放在 26 與 93 之間。'),
    'd-ins': ('pred 是 26、succ 是 93，新節點 newNode 為 77 放在兩者之間；下方列出四行：newNode->prev = pred; newNode->next = succ; pred->next = newNode; succ->prev = newNode;',
              '雙向串列插入 77：pred 是左邊的鄰居 26，succ 是右邊的鄰居 93。橘色的前兩步先設定新節點自己的 prev 與 next，藍色的後兩步再讓兩個鄰居改指新節點，原本 26 與 93 之間的兩條連結就被取代。'),
    'd-ins-after': ('header、54、26、77、93、trailer 以雙向箭頭相連，下方註明 after: 77 sits between 26 and 93。',
                    '插入後：77 的前後鄰居分別是 26 與 93，每一對相鄰節點都互相指向對方。'),
    'd-del-before': ('header、54、26、77、93、trailer 以雙向箭頭相連，77 以淡色標示，下方註明 before: delete the node holding 77。',
                     '刪除前：要刪的是存放 77 的節點。'),
    'd-del': ('77 的節點變成灰色，與左右的連線為虛線；藍色箭頭讓 26 的 next 直接指向 93、93 的 prev 直接指向 26；下方程式為 pred->next = succ; succ->prev = pred; delete node;',
              '雙向串列刪除 77：讓左鄰居 26 的 next 直接指向右鄰居 93，再讓 93 的 prev 指回 26。只改兩條連結，77 就不在串列中了，最後 delete 釋放它。'),
    'd-del-after': ('header、54、26、93、trailer 以雙向箭頭相連，下方註明 after: 26 and 93 are neighbours again。',
                    '刪除後：26 與 93 重新成為相鄰節點。因為兩端有哨兵，刪除第一項或最後一項時也一樣有左右鄰居。'),
}

for _fid, (_file, _w, _nw, _nh) in _SIZES.items():
    FIGURES[_fid] = {'file': _file, 'width': _w, 'height': round(_w * _nh / _nw),
                     'alt': _TEXT[_fid][0], 'caption': _TEXT[_fid][1]}

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


def steps(summary, fids):
    """Step-by-step lecture figures: collapsed so that only the representative figures stay visible."""
    body = ''.join(figure(f) for f in fids)
    return (f'<details class="linked-detail"><summary>{summary}</summary>'
            f'<div class="linked-detail-body">{body}</div></details>')


def apply_figures(page):
    """Figures are emitted inline by linked_depth; only the shared style lives here."""
    page = re.sub(r'<!-- linked-figure:[^>]+ -->.*?<!-- /linked-figure -->', '', page, flags=re.S)
    page = re.sub(r'<style id="linked-figures-style">.*?</style>', '', page, flags=re.S)
    return page.replace('</head>', STYLE + '</head>', 1)
