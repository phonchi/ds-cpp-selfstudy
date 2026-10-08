"""Lecture figures for chapter 6 (recursion.html), stored in assets/figures/ch6/."""
from html import escape

# fid: (file, display width, natural width, natural height, alt, caption)
_SPECS = {
    'eq1': ('recursion_eq1.png', 300, 364, 60,
            '(1 + (3 + (5 + (7 + 9))))',
            '把 {1, 3, 5, 7, 9} 的加總寫成完全括號化的運算式：每一對括號裡只有一次「兩個數相加」，最裡面的 (7 + 9) 不需要迴圈就能直接算。'),
    'eq2': ('recursion_eq2.png', 380, 499, 234,
            '五行算式：total = (1 + (3 + (5 + (7 + 9))))，接著依序化簡為 (1 + (3 + (5 + 16)))、(1 + (3 + 21))、(1 + 24)，最後 total = 25。',
            '從最裡面的括號往外化簡：先算 7 + 9 = 16，再算 5 + 16 = 21、3 + 21 = 24、1 + 24 = 25。每一步都只處理一組括號，剩下的式子形狀不變、只是變短。'),
    'eq3': ('recursion_eq3.png', 1000, 3120, 336,
            'listSumFrom(numList, i) 的分段定義：i < numList.size() 時等於 numList[i] + listSumFrom(numList, i + 1)；i == numList.size() 時等於 0。',
            'listSumFrom 的分段定義。上面一行是遞迴的情況：目前這一項加上「從下一個索引開始的總和」；下面一行是 base case：索引走到尾端時，剩下的範圍是空的，總和為 0。'),
    'sum': ('recursion_sum.png', 300, 340, 360,
            'sum(1,3,5,7,9) = 1 + sum(3,5,7,9)，再往下展開為 3 + sum(5,7,9)、5 + sum(7,9)、7 + sum(9)，最後 sum(9) = 9。',
            '展開的過程：每一層都把第一個數留下來，剩下的部分交給下一層。問題一層比一層短，直到只剩一個數，可以直接回答。'),
    'sum2': ('recursion_sum2.png', 360, 428, 360,
             '由下往上的回傳：sum(9) = 9，sum(7,9) = 7 + 9，sum(5,7,9) = 5 + 16，sum(3,5,7,9) = 3 + 21，sum(1,3,5,7,9) = 1 + 24 = 25。',
             '回傳的過程：最下面一層先得到 9，每一層把下一層的結果加上自己留下的那個數，再交回上一層：16、21、24，最後得到 25。'),
    'num2str': ('num2str.png', 420, 1200, 924,
                'toStr(769, 10) 呼叫 toStr(76, 10)，餘數 9；toStr(76, 10) 呼叫 toStr(7, 10)，餘數 6；7 < 10 是 base case，得到 7。回傳 "7"、"76"、"769"。',
                'toStr(769, 10) 的分解：每次除以 10，商交給下一層遞迴，餘數記在右邊。7 小於 10 時停止。右欄的餘數由下往上讀，就是 "769"。'),
    'num2str2': ('num2str2.png', 420, 1200, 1164,
                 'toStr(10, 2) 依序呼叫 toStr(5, 2)、toStr(2, 2)、toStr(1, 2)，餘數依序為 0、1、0；1 < 2 是 base case。回傳 "1"、"10"、"101"、"1010"。',
                 'toStr(10, 2) 的追蹤：餘數由上往下產生的順序是 0、1、0，最後才得到 base case 的 1。字串卻是從最下層往上組成的，所以結果是 "1010"，不是倒過來的 "0101"。'),
    'stack': ('recursion_stack.png', 160, 202, 204,
              '一個堆疊，由下而上依序是 \'0\'、\'1\'、\'0\'、\'1\'。',
              '改用顯式堆疊轉換 10：除了四次之後，堆疊由下而上存著 \'0\'、\'1\'、\'0\'、\'1\'。依序 pop 出來接成字串，就是 "1010"。'),
    'stack2': ('recursion_stack2.png', 400, 1200, 1176,
               '呼叫堆疊，最上面是 toStr(2, 2)：n = 2，正在計算 std::string("1") + convertString[2 % 2]，結果 "10"；下面的 toStr(5, 2) 與 toStr(10, 2) 標示 waiting。上方註明 toStr(1, 2) 已回傳 "1"。',
               'toStr(1, 2) 回傳 "1" 之後的呼叫堆疊。最上面的 frame 屬於 toStr(2, 2)，它把收到的 "1" 接上 convertString[2 % 2]，得到 "10"；下面兩個 frame 還在等待，各自保存自己的 n 與 base。'),
    'viz1': ('recursion_viz1.png', 300, 589, 589,
             '一條從底部往上、不斷向右彎的線段，只畫出樹最右邊的一支。',
             'tree 一開始的樣子：每次都先處理右邊的小樹，所以程式一路往右畫，直到最短的小枝才停下。'),
    'viz2': ('recursion_viz2.png', 300, 589, 589,
             '樹幹加上右半邊的所有分枝已經畫完，左半邊還是空的。',
             '右半邊畫完了：程式沿著樹幹往回退，每退到一個分岔點才開始畫那裡的左子樹。左半邊會用同樣的方式，先畫各自的右邊。'),
    'triangle': ('recursion_triangle.png', 460, 1250, 1041,
                 'degree 為 5 的 Sierpinski 三角形：大三角形中間是紫色倒三角形，三個角各有一個同樣圖案的小三角形，越小的三角形顏色依序不同。',
                 'Sierpinski 三角形：中間的倒三角形不再分割，三個角落的小三角形各自又是一個 Sierpinski 三角形。顏色代表畫出這個三角形時的 degree。'),
    'triangle2': ('recursion_triangle2.png', 330, 430, 399,
                  '呼叫樹：每個節點有 left、top、right 三個子節點；最左邊一路往下的節點是白色（正在執行），其餘 top 與 right 子節點是灰色（尚未執行）。',
                  'sierpinski 的呼叫圖。白色是目前正在執行的呼叫，灰色是還沒輪到的呼叫：程式先一路鑽到左下角最小的三角形，左邊整支做完才輪到 top，最後才是 right。'),
    'hanoi': ('Hanoi.png', 760, 2400, 840,
              '三根柱子 fromPole、withPole、toPole。最大的盤子留在 fromPole，四個較小的盤子疊在 withPole，toPole 是空的。',
              '五盤河內塔進行到一半：上面四個盤子已經搬到 withPole，fromPole 只剩最大的盤子，下一步就是把它搬到 toPole。每根柱子上都是小盤在上、大盤在下。'),
    'maze': ('maze.png', 440, 1331, 1250,
             '迷宮格子圖：橘色是牆，白色是通道；藍色烏龜在起點，綠點標出走到出口的路線，紅點是試過之後退回的格子。',
             '迷宮探索的結果：綠點連成從起點到出口的路，紅點是走進去之後發現是死路、又退回來的格子。退回來的動作，在程式裡就是遞迴呼叫回傳 false。'),
    'dp1': ('dp1.png', 760, 947, 403,
            '以 26 為根的呼叫樹：箭頭上標示用掉的硬幣 1、5、10、25，節點是剩下的金額，例如 25、21、16、1；第二層的 21 又展開成 20、16、11，16 展開成 15、11、6。15、11、16、6 等節點在樹中重複出現多次。',
            'makeChange1 計算 26 分時的一小部分呼叫。節點是要找零的金額，箭頭上的數字是剛用掉的硬幣。同一個金額會在不同分支重複出現，例如 15 至少出現三次，每次都從頭重算。'),
    'dp2': ('dp2.png', 420, 457, 397,
            '表格的欄是 1 到 11 分，每一列是演算法的一個步驟；第 5 列填到 5 分時值是 1，最後一列為 1 2 3 4 1 2 3 4 5 1 2。',
            '由下往上填 11 分的表：每一列多填一格。1 到 4 分只能用 1 分硬幣；5 分可以用一枚 5 分，所以是 1。最後一列是 1 到 11 分各自的最少硬幣數。'),
    'dp3': ('dp3.png', 420, 456, 156,
            '1 到 10 分的值為 1 2 3 4 1 2 3 4 5 1，11 分那格是問號；三條弧線從 11 分連到 11−1、11−5、11−10 三格。',
            '計算 11 分時要比較的三格：拿一枚 1 分之後剩 10 分（1 枚），拿一枚 5 分之後剩 6 分（2 枚），拿一枚 10 分之後剩 1 分（1 枚）。最少的是 1 枚再加上剛拿的那一枚，所以 11 分需要 2 枚。'),
}

FIGURES = {fid: {'file': f, 'width': w, 'height': round(w * nh / nw), 'alt': alt, 'caption': cap}
           for fid, (f, w, nw, nh, alt, cap) in _SPECS.items()}


def figure(fid):
    spec = FIGURES[fid]
    alt = escape(spec['alt'], quote=True)
    return (f'<figure class="rec-figure" id="rec-figure-{fid}">'
            f'<div class="rec-figure-scroll" tabindex="0" role="region" aria-label="{alt}">'
            f'<img src="assets/figures/ch6/{spec["file"]}" alt="{alt}" '
            f'width="{spec["width"]}" height="{spec["height"]}" style="--figure-width:{spec["width"]}px" loading="lazy"></div>'
            f'<figcaption>{escape(spec["caption"], quote=False)}</figcaption></figure>')


STYLE = '''<style id="recursion-figures-style">
.rec-figure{margin:1rem 0 1.4rem;max-width:100%;}
.rec-figure-scroll{max-width:100%;overflow-x:auto;background:#fff;border:1px solid var(--card-border);border-radius:8px;padding:.4rem 0;}
.rec-figure img{display:block;height:auto;max-width:100%;width:var(--figure-width);margin:0 auto;}
#rec-figure-eq3 img,#rec-figure-dp1 img{min-width:640px;}
.rec-figure figcaption{margin-top:.65rem;font-size:.9rem;line-height:1.8;color:var(--ink);}
</style>'''
