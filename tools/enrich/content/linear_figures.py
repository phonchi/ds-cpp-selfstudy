"""Lecture figures for chapter 5, placed beside the text they explain."""
from html import escape

# fid: (file, display width, natural width, natural height, alt, caption)
_SPECS = {
    'books': ('stack_b.png', 420, 1200, 744,
              '五本書由下往上疊成一疊：History、Music、Physics、Calculus，最上面是標成橘色的 C++；右上標 top，右下桌面旁標 base。',
              '一疊書就是一個 stack：只看得到、也只能拿到最上面的 C++，這一端叫 top；壓在最底下的 History 待得最久，那一端叫 base。要拿 Physics，得先把上面兩本拿走。'),
    'reverse': ('stack_c.png', 760, 2400, 864,
                '左欄 push order 依序是 "4"、"dog"、"true"、"8.4"；中間的 std::stack<string> 由下到上存放 "4"、"dog"、"true"、"8.4"，top 在 "8.4"；右欄 pop order 依序是 "8.4"、"true"、"dog"、"4"。',
                '依序 push "4"、"dog"、"true"、"8.4" 之後，最後放進去的 "8.4" 在 top。全部 pop 出來的順序是 "8.4"、"true"、"dog"、"4"，正好與放入的順序相反。'),
    'paren': ('paren.png', 361, 361, 116,
              '一串括號 ( ( ) ( ( ) ) ( ) )；上方箭頭指出中間最近的一個左括號與它後面第一個右括號配對，下方弧線把第一個左括號連到最後一個右括號。',
              '由左往右讀：遇到右括號時，要配的是最近一個還沒配對的左括號；最先出現的左括號，可能要等到最後一個右括號才配對。配對由內往外進行，順序與左括號出現的順序相反。'),
    'divide': ('convert_b.png', 720, 2400, 1200,
               '左欄列出 233/2=116、116/2=58、58/2=29、29/2=14、14/2=7、7/2=3、3/2=1、1/2=0；中欄是對應的餘數 1、0、0、1、0、1、1、1；右邊的 stack 由下到上是 1、0、0、1、0、1、1、1，旁邊標 push 向上、pop 向下，上方寫 "11101001"。',
               '把 233 一直除以 2：第一個餘數 1 是最低位，最後一個餘數 1 是最高位。餘數依產生順序 push，再從 top 一路 pop，就得到由高位到低位的 "11101001"。'),
    'post-move': ('convert_1.png', 271, 271, 64,
                  '( A + ( B * C ) )；* 的箭頭移到內層右括號，+ 的箭頭移到外層右括號。',
                  '轉成後序：每個運算子移到它那一對括號的右括號位置，再去掉括號，得到 A B C * +。'),
    'pre-move': ('convert_2.png', 271, 271, 72,
                 '( A + ( B * C ) )；* 的箭頭移到內層左括號，+ 的箭頭移到外層左括號。',
                 '轉成前序：運算子改移到左括號的位置，得到 + A * B C。'),
    'full-paren': ('convert_3.png', 900, 2640, 696,
                   '(A + B) * C - (D - E) * (F + G) 先寫成完全括號 (((A + B) * C) - ((D - E) * (F + G)))，左下得到前序 - * + A B C * - D E + F G，右下得到後序 A B + C * D E - F G + * -。',
                   '較長的例子也用同一套做法：先依優先權加上完全括號，運算子移到左括號得到前序，移到右括號得到後序。'),
    'i2p-trace': ('convert_4.png', 900, 2640, 888,
                  'infixToPostfix("A * B + C * D") 的追蹤表，欄位為 token、opStack（top 在右）、postfixList。讀到 + 時，* 先離開 stack；最後 pop 剩下的 + * ，結果是 A B * C D * +。',
                  '轉換 A * B + C * D：運算元直接放進 postfixList；讀到 + 時，stack 上的 * 優先權較高，先被 pop 到輸出，+ 才 push 進去；第二個 * 比 + 高，直接疊上去。讀完後把 stack 剩下的 * 與 + 依序 pop 出來。'),
    'eval-1': ('convert_5.png', 368, 368, 224,
               '由左到右求值 4 5 6 * +：4、5、6 依序 push；讀到 * 時 pop 兩次算出 30 再 push；讀到 + 時 pop 兩次算出 34。',
               '後序求值時，等待的是運算元：4、5、6 先 push；讀到 * 就取出最上面的 6 與 5，算出 30 放回；讀到 + 再取出 30 與 4，得到 34。'),
    'eval-2': ('convert_6.png', 420, 420, 185,
               '求值 7 8 + 3 2 + /：stack 依序變成 7；7 8；15；15 3；15 3 2；15 5；最後是 3。',
               '7 8 + 3 2 + / 的過程：stack 先變高、再變矮、又變高。讀到 / 時先 pop 出來的 5 是除數，後 pop 的 15 是被除數，所以結果是 15 / 5 = 3。'),
    'queue': ('queue_1.png', 760, 2400, 504,
              'std::queue<string> 中由左到右是 "8.4"、"true"、"dog"、"4"；左邊 rear: push 箭頭指入，右邊 front: pop 箭頭指出，下方寫 first in, first out。',
              '"4" 最早進入 queue，所以在 front，下一次 pop 就輪到它；新元素一律從 rear 加入，必須等前面的元素都離開才輪到自己。'),
    'potato-circle': ('queue_2.png', 378, 378, 289,
                      'Bill、David、Susan、Jane、Kent、Brad 圍成一圈，箭頭表示山芋傳給下一個人；Brad 是灰色，旁邊寫 After 5 passes, Brad is eliminated。',
                      '六個人圍成一圈依序傳山芋。圖中的例子傳了 5 次後停下，拿著山芋的 Brad 出局，剩下的人繼續玩，直到只剩一人。'),
    'potato-queue': ('queue_3.png', 504, 504, 234,
                     '上方的 queue 由 rear 到 front 是 Brad、Kent、Jane、Susan、David、Bill；箭頭表示 Bill 從 front dequeue 後回到 rear enqueue（Go to the rear, pass the potato）；下方的 queue 由 rear 到 front 變成 Bill、Brad、Kent、Jane、Susan、David。',
                     '用 queue 模擬圍圈：front 的人拿著山芋。傳一次山芋，就是把 front 的人移出，再放回 rear；Bill 從最前面移到最後面，下一個拿山芋的是 David。'),
    'printer': ('queue_4.png', 570, 570, 399,
                '左側六台 Lab Computers，箭頭把 task 送進中間的 print queue，佇列裡有五個 task，右端連到印表機。',
                '實驗室的電腦把列印工作送進同一個 print queue，印表機依先來先印的順序一次處理一個工作。學生等待的時間，就是工作在 queue 裡排隊的時間。'),
    'deque': ('deque.png', 760, 2400, 600,
              'std::deque<string> 中由左到右是 "dog"、"4"、"cat"、"true"；左邊 rear 端有 push_back 與 pop_back 兩個箭頭，右邊 front 端有 push_front 與 pop_front 兩個箭頭。',
              'deque 的兩端都能加入與移除：front 端用 push_front／pop_front，rear 端用 push_back／pop_back。只用同一端時它像 stack，一端進、另一端出時像 queue。'),
    'palindrome': ('deque_2.png', 587, 587, 397,
                   '上半部把 "radar" 的字元依序加到 rear，deque 中由 rear 到 front 為 r a d a r；下半部從 front 與 rear 各取出一個 r。',
                   '先把 radar 的每個字元依序加到 rear；接著同時從 front 與 rear 各取出一個字元比較。兩端都是 r，相同就繼續往中間比。'),
}

FIGURES = {fid: {'file': f, 'width': w, 'height': round(w * nh / nw), 'alt': alt, 'caption': cap}
           for fid, (f, w, nw, nh, alt, cap) in _SPECS.items()}

STYLE = '''<style id="linear-figures-style">
.linear-figure{margin:1rem 0 1.4rem;max-width:100%;}
.linear-figure-scroll{max-width:100%;overflow-x:auto;background:#fff;border:1px solid var(--card-border);border-radius:8px;padding:.4rem 0;}
.linear-figure img{display:block;height:auto;max-width:none;width:var(--figure-width);margin:0 auto;}
.linear-figure figcaption{margin-top:.65rem;font-size:.9rem;line-height:1.8;color:var(--ink);}
.linear-figure-pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:0 1.2rem;}
</style>'''


def figure(fid):
    spec = FIGURES[fid]
    alt = escape(spec['alt'], quote=True)
    return (f'<figure class="linear-figure" id="linear-figure-{fid}">'
            f'<div class="linear-figure-scroll" tabindex="0" role="region" aria-label="{alt}">'
            f'<img src="assets/figures/ch5/{spec["file"]}" alt="{alt}" '
            f'width="{spec["width"]}" height="{spec["height"]}" style="--figure-width:{spec["width"]}px" loading="lazy"></div>'
            f'<figcaption>{escape(spec["caption"], quote=False)}</figcaption></figure>')


def pair(*fids):
    """Two small figures side by side on wide screens, stacked on phones."""
    return '<div class="linear-figure-pair">' + ''.join(figure(f) for f in fids) + '</div>'
