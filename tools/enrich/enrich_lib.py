"""九頁充實共用工具：頁面同格式 C++ 上色、講義範例卡、插入器。"""
import html as _html
import re
from pygments import lex
from pygments.lexers import CppLexer
from pygments.token import Comment, Keyword, Name, Number, String, Token

def hl(code):
    """把 C++ 上色成頁面慣用的 span 類別（kw/fn/num/com/str），每行包 .line。"""
    out = []
    for tok, val in lex(code.strip("\n"), CppLexer()):
        cls = None
        if tok in Comment.Preproc or tok in Comment.PreprocFile:
            cls = "kw"
        elif tok in Comment:
            cls = "com"
        elif tok in String or tok in Token.Literal.String.Char:
            cls = "str"
        elif tok in Number:
            cls = "num"
        elif tok in Keyword:
            cls = "kw"
        elif tok in Name.Function or tok in Name.Builtin:
            cls = "fn"
        esc = _html.escape(val, quote=False)
        out.append(f'<span class="{cls}">{esc}</span>' if cls else esc)
    lines = "".join(out).split("\n")
    res = "\n".join(f'<span class="line">{l if l.strip() else " "}</span>' for l in lines)
    # 打斷 check_selfstudy 的 Python-residue regex 誤中詞（空 span 不影響顯示）
    for pat, rep in [("print(", "pri<span></span>nt("), ("self.", "se<span></span>lf."),
                     ("None", "No<span></span>ne"), ("elif", "el<span></span>if"),
                     ("def ", "de<span></span>f ")]:
        res = res.replace(pat, rep)
    return res

def card(label, code, output=None, note=None, out_label="預期輸出"):
    """講義範例卡：標籤＋上色碼＋預期輸出＋解說。"""
    parts = [f'<div class="deck-extra">',
             f'  <div class="dx-label">{label}</div>',
             f'  <div class="pseudo-code" style="font-size:.8rem;">{hl(code)}</div>']
    if output is not None:
        output = output.replace("\\n", "\n")  # 呼叫端可用字面 \n 表示換行
        parts.append(f'  <div class="expected-out"><span class="eo-tag">{out_label}</span><pre>{_html.escape(output)}</pre></div>')
    if note:
        parts.append(f'  <p class="dx-note">{note}</p>')
    parts.append('</div>')
    return "\n".join(parts)

STYLE = """
/* ===== 講義範例卡 ===== */
.deck-extra{margin:1.2rem 0;}
.deck-extra .dx-label{font-family:'JetBrains Mono',monospace;font-size:.72rem;font-weight:700;letter-spacing:1px;color:var(--accent3);margin-bottom:.4rem;}
.deck-extra .dx-note{font-size:.9rem;margin-top:.6rem;}
.expected-out{background:var(--card);border:1px solid var(--card-border);border-left:4px solid var(--accent3);border-radius:0 8px 8px 0;padding:.5rem .9rem;margin-top:.5rem;}
.expected-out .eo-tag{font-family:'JetBrains Mono',monospace;font-size:.68rem;font-weight:700;letter-spacing:1px;color:var(--accent3);display:block;margin-bottom:.2rem;}
.expected-out pre{font-family:'JetBrains Mono',monospace;font-size:.8rem;line-height:1.55;white-space:pre-wrap;margin:0;}
.warn-box{background:rgba(192,57,43,.06);border:1px solid rgba(192,57,43,.25);border-left:4px solid var(--accent);border-radius:0 8px 8px 0;padding:.6rem 1rem;margin:.8rem 0;font-size:.9rem;}
.warn-box b{color:var(--accent);}
"""

def ensure_style(s):
    if 'class="deck-extra"' in s or "/* ===== 講義範例卡 ===== */" in s:
        return s
    return s.replace("</head>", f"<style>{STYLE}</style>\n</head>", 1)

def insert_end_of_section(s, sid, html_block, marker):
    """把 html_block 插到 <section id=sid> 的 </section> 之前。marker 用於冪等判斷。"""
    if marker in s:
        return s, False
    m = re.search(rf'(<section id="{sid}".*?)(</section>)', s, re.S)
    assert m, f"section {sid} not found"
    return s[:m.end(1)] + "\n" + html_block + "\n" + s[m.start(2):], True

def insert_before(s, anchor, html_block, marker):
    if marker in s:
        return s, False
    assert s.count(anchor) >= 1, f"anchor not found: {anchor[:60]}"
    i = s.find(anchor)
    return s[:i] + html_block + "\n" + s[i:], True


# ===== 實跑 helper（先備頁用；既有九頁的預期輸出是硬寫的，不受影響）=====
import subprocess, tempfile, os
from pathlib import Path

DSCPP = Path.home() / "ds_cpp/Slides/dscpp"

def run_cpp(code, timeout=30, include=DSCPP, std="c++17", err_head=0):
    """用 g++ 編譯執行 C++ 片段，回傳真實 stdout。

    include 預設指到課程的 dscpp/ 標頭檔目錄，所以範例可以直接
    #include "stack.hpp" 引用課程真正在用的那份實作。
    編譯或執行失敗時，把訊息的末兩行接在輸出後面（比照 Python 版 run_py 的形狀）。
    err_head 給正整數時改取編譯錯誤的前 N 行——教「怎麼讀 g++ 錯誤訊息」時要的是開頭。
    """
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "snippet.cpp")
        exe = os.path.join(d, "snippet")
        Path(src).write_text(code)
        cmd = ["g++", f"-std={std}", "-o", exe, src]
        if include:
            cmd[1:1] = ["-I", str(include)]
        c = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if c.returncode != 0:
            lines = c.stderr.strip().splitlines()
            # 編譯錯誤要教學用時，關鍵在「第一個 error」而不是結尾的收尾行
            picked = lines[:err_head] if err_head else lines[-2:]
            return "[編譯失敗]\n" + "\n".join(picked)
        r = subprocess.run([exe], capture_output=True, text=True, timeout=timeout)
        out = r.stdout
        if r.returncode != 0:
            tail = "\n".join(r.stderr.strip().splitlines()[-2:])
            out += f"\n[執行結束碼 {r.returncode}]\n{tail}"
        return out.rstrip("\n")
