"""Lecture figures for chapter 7 (searching_sorting.html), stored in assets/figures/ch7/."""
from html import escape

# fid: (file, display width, natural width, natural height, alt, caption)
_SPECS = {
    'seqsearch': ('seqsearch.png', 424, 424, 90,
                  '十格的 vector：54, 26, 93, 17, 77, 31, 44, 55, 20, 65，從標示 Start 的第一格開始，箭頭一格一格往右連到最後一格。',
                  '循序搜尋從索引 0 開始，沿著箭頭一格一格往右比對，直到找到目標或走完整個 vector。資料不需要排序。'),
    'seqsearch2': ('seqsearch2.png', 441, 441, 90,
                   '已排序的 vector：17, 20, 26, 31, 44, 54, 55, 65, 77, 93。箭頭從 17 一路走到 54，54 那格加上陰影，之後沒有箭頭。',
                   '在有序的 vector 裡找 50：17 到 44 都比 50 小，只能繼續往右；走到 54 時已經比 50 大，後面的數只會更大，所以在 54 停下並回傳 false。'),
    'binsearch': ('binsearch.png', 384, 384, 117,
                  '已排序的 vector：17, 20, 26, 31, 44, 54, 55, 65, 77, 93。Start 箭頭指向中間的 44，再彎到 65，最後彎回 54。',
                  '用二分搜尋找 54：先比中間的 44，54 比較大，左半邊連同 44 都可以丟掉；再比右半邊中間的 65，54 比較小，丟掉 65 和它右邊的數；第三次比到 54，找到了。'),
    'hashtable': ('hashtable.png', 720, 2208, 384,
                  '大小 11 的雜湊表，slot 0 到 10 都存 -1。下方程式碼：vector<int> hashTable(11, -1); // -1 = empty slot。',
                  '大小 11 的空雜湊表。每個 slot 都先放 -1，表示這一格還沒有資料，所以 -1 不能拿來當作要存的值。'),
    'hashtable2': ('hashtable2.png', 720, 2208, 384,
                   '雜湊表 slot 0 是 77，4、5、6 是 26、93、17，9、10 是 31、54，其餘是 -1。下方寫著 h(item) = item % 11 與各數的雜湊值。',
                   '用餘數法 h(item) = item % 11 放入六個數：每個數直接放到自己的雜湊值那一格。11 格中有 6 格有資料，負載因子 λ = 6/11。'),
    'stringhash': ('stringhash.png', 335, 335, 132,
                   'c、a、t 三個字元往下對應 99、97、116，相加等於 312，312 % 11 得到 4。',
                   '字串 "cat" 的雜湊值：把三個字元的 ASCII 值 99、97、116 加起來得到 312，再用餘數法 312 % 11 = 4。'),
    'stringhash2': ('stringhash2.png', 560, 1920, 648,
                    'c、a、t 在索引 0、1、2，權重是 1、2、3；99*1 + 97*2 + 116*3 = 641，641 % 11 = 3。',
                    '以位置當權重：索引 i 的字元乘上 i + 1 再相加，"cat" 得到 641，641 % 11 = 3。字母相同但順序不同的 "act"、"tac" 會得到不同的總和，不會全部撞在同一格。'),
    'linearprobing1': ('linearprobing1.png', 720, 2208, 384,
                       '雜湊表依序為 77, 44, 55, 20, 26, 93, 17, -1, -1, 31, 54；44、55、20 三格是橘色。下方寫著 collision → try the next slot: (pos + 1) % 11。',
                       '用線性探查放入九個數。44 和 55 的雜湊值都是 0，20 的雜湊值是 9，三個都撞到已經有資料的格子，只好一格一格往後找，最後落在 1、2、3（橘色）。'),
    'clustering': ('clustering.png', 720, 2208, 384,
                   '同一張表，slot 0、1、2 的 77、44、55 是橘色。下方寫著 items hashing to 0 pile up in neighbouring slots。',
                   '群聚（clustering）：雜湊值都是 0 的 77、44、55 擠在相鄰的 0 到 2 格。之後雜湊到這一段的數，都要先走過整段才找得到空位，20 就是這樣被推到 3。'),
    'linearprobing2': ('linearprobing2.png', 720, 2208, 384,
                       '雜湊表依序為 77, 55, -1, 44, 26, 93, 17, 20, -1, 31, 54；55、44、20 三格是橘色。下方寫著 collision → (pos + 3) % 11。',
                       '「加 3」探查：碰撞後每次跳 3 格。44 從 0 跳到 3；55 依序試 3、6、9，最後落在 1；20 依序試 1、4，最後落在 7。碰撞的數分散開來，不再擠成一段。'),
    'quadratic': ('quadratic.png', 720, 2208, 384,
                  '雜湊表依序為 77, 44, 20, 55, 26, 93, 17, -1, -1, 31, 54；44、20、55 三格是橘色。下方寫著 collision → (h + 1), (h + 4), (h + 9), … % 11。',
                  '平方探查：碰撞後依序試 h + 1、h + 4、h + 9……。44 試一次就落在 1；55 試過 1、4、9、5 都有資料，最後落在 (0 + 25) % 11 = 3；20 試過 10 之後落在 (9 + 4) % 11 = 2。'),
    'chaining': ('chaining.png', 720, 2208, 888,
                 '11 格的表，每格是一條 list：slot 0 接著 77 → 44 → 55，slot 9 接著 31 → 20，slot 4、5、6、10 各接一個數，其餘是空的 {}。下方寫著 vector<list<int>> table(11);。',
                 '鏈結法（chaining）：每個 slot 存一條 list，碰撞的數直接接在同一條 list 後面，不會占用別的格子。搜尋時先算出 slot，再在那條 list 裡循序找。'),
    'bubblepass': ('bubblepass.png', 420, 542, 498,
                   '九列陣列，每列有兩格陰影表示正在比較的一對，右邊標示 Exchange 或 No Exchange；最後一列 93 在最右邊，標示 93 in place after first pass。',
                   '氣泡排序的第一輪：每次比較相鄰的兩個數（陰影），左邊比較大就交換。54 和 93 這一對順序正確，不交換。93 一路被換到最右邊，這一輪共比較 8 次。'),
    'selectionsortnew': ('selectionsortnew.png', 400, 494, 610,
                         '九列陣列，每列一個陰影格是最大值，箭頭把它換到未排序部分的最後一格；右邊依序標示 93、77、55、54、44（stays in place）、31、26、20 is largest，最後 17 ok list is sorted。',
                         '選擇排序：每一輪掃過未排序的部分，找出最大值（陰影），和未排序部分的最後一格交換。每輪最多交換一次；44 那一輪已經在正確位置，不用換。'),
    'insertionsort': ('insertionsort.png', 400, 484, 458,
                      '九列陣列，左邊的陰影格逐列增加一格；右邊標示 Assume 54 is a sorted list of 1 item，以及 inserted 26、93、17、77、31、44、55、20。',
                      '插入排序：陰影是左邊已排序的子清單，一開始只有 54。每一輪把下一個數插進子清單中正確的位置，子清單就多一個數。'),
    'insertionpass': ('insertionpass.png', 400, 473, 322,
                      '五列：要把 31 插回已排序的 17, 26, 54, 77, 93；93、77、54 依序往右移一格，最後 26 < 31，把 31 放進空出的位置。',
                      '插入 31 的細節：93、77、54 都比 31 大，依序往右移一格；碰到 26 比 31 小就停下，把 31 放進空出來的位置。每次移動只做一次指定，不是交換。'),
    'shellsortA': ('shellsortA.png', 406, 406, 174,
                   '三列陣列 54, 26, 93, 17, 77, 31, 44, 55, 20，每列標出相隔 3 格的三個數，分別是 sublist 1、2、3。',
                   '增量（gap）為 3：每隔 3 個取一個數，組成三個子清單。第一個子清單是 54、17、44。'),
    'shellsortB': ('shellsortB.png', 465, 465, 262,
                   '三個子清單各自排好之後合併成 17, 26, 20, 44, 55, 31, 54, 77, 93，標示 after sorting sublists at increment 3。',
                   '三個子清單各自用插入排序排好後的結果。整個 list 還沒排序完成，但大部分的數已經靠近最終位置。'),
    'shellsortC': ('shellsortC.png', 429, 429, 317,
                   '四列：1 shift for 20、2 shifts for 31、1 shift for 54，最後一列是排好的 17, 20, 26, 31, 44, 54, 55, 77, 93。',
                   '最後用增量 1，也就是一般的插入排序收尾。因為前面已經把數移到附近，只需要 4 次移動。'),
    'shellsortD': ('shellsortD.png', 406, 406, 224,
                   '四列陣列，分別標出 sublist 1 到 4：相隔 4 格的數，第一個子清單是 54、77、20。',
                   '程式實際用的增量從 n / 2 開始。9 個數時第一輪的增量是 4，形成四個子清單；之後增量依序是 2、1。'),
    'mergesortA': ('mergesortA.png', 460, 528, 346,
                   '樹狀圖：54, 26, 93, 17, 77, 31, 44, 55, 20 切成兩半，再一路切到每份只剩一個數。',
                   '切分：每一層從中間把 list 切成兩半，直到每一份只剩一個數。只有一個數的 list 本身就是排好的。'),
    'mergesortB': ('mergesortB.png', 420, 458, 404,
                   '由上往下的合併圖：單一的數兩兩合併成 26 54、17 93、31 77、20 55，再合併成 17 26 54 93 與 20 31 44 55 77，最後是 17, 20, 26, 31, 44, 54, 55, 77, 93。',
                   '合併：把兩個已排序的 list 合併成一個，從最小的片段開始，一層一層合併回完整的排序結果。'),
    'firstsplit': ('firstsplit.png', 437, 437, 74,
                   '陣列 54, 26, 93, 17, 77, 31, 44, 55, 20，第一格 54 加上陰影，標示 54 will be the first pivot value。',
                   '以第一個數 54 當作第一個 pivot。'),
    'partitionA': ('partitionA.png', 640, 2640, 1920,
                   '七列 partition 過程：leftMark、rightMark 從兩端出發；93 > 54 且 20 < 54 時停下並交換；77 > 54 且 44 < 54 時停下並交換；rightMark < leftMark 時停止，split point 為 5；最後 pivot 54 與 31 交換。',
                   'partition 的過程：leftMark 往右找比 54 大的數，rightMark 往左找比 54 小的數，兩個都停下就交換（93 和 20、77 和 44）。rightMark 跑到 leftMark 左邊時停止，rightMark 所在的索引 5 就是分割點，再把 pivot 54 和那一格的 31 交換。'),
    'partitionB': ('partitionB.png', 472, 472, 204,
                   '31, 26, 20, 17, 44, 54, 77, 55, 93，54 加上陰影；左邊五個數標示 <54，右邊三個標示 >54，下方分成 quicksort left half 與 quicksort right half。',
                   '54 已經在最終位置：左邊都比 54 小，右邊都比 54 大。接下來對左右兩半各自遞迴做 quicksort。'),
}

FIGURES = {fid: {'file': f, 'width': w, 'height': round(w * nh / nw), 'alt': alt, 'caption': cap}
           for fid, (f, w, nw, nh, alt, cap) in _SPECS.items()}


def figure(fid):
    spec = FIGURES[fid]
    alt = escape(spec['alt'], quote=True)
    return (f'<figure class="srch-figure" id="srch-figure-{fid}">'
            f'<div class="srch-figure-scroll" tabindex="0" role="region" aria-label="{alt}">'
            f'<img src="assets/figures/ch7/{spec["file"]}" alt="{alt}" '
            f'width="{spec["width"]}" height="{spec["height"]}" style="--figure-width:{spec["width"]}px" loading="lazy"></div>'
            f'<figcaption>{escape(spec["caption"], quote=False)}</figcaption></figure>')


STYLE = '''<style id="search-figures-style">
.srch-figure{margin:1rem 0 1.4rem;max-width:100%;}
.srch-figure-scroll{max-width:100%;overflow-x:auto;background:#fff;border:1px solid var(--card-border);border-radius:8px;padding:.4rem 0;}
.srch-figure img{display:block;height:auto;max-width:100%;width:var(--figure-width);margin:0 auto;}
.srch-figure figcaption{margin-top:.65rem;font-size:.9rem;line-height:1.8;color:var(--ink);}
</style>'''
