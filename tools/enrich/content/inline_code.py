"""C++ identifiers in teaching prose, shared with the browser formatter."""
from html import escape, unescape
from pathlib import Path
import json
import re

TERMS = '''ArrayList SparseMatrix Node UnorderedList OrderedList Linear
array vector list forward_list map unordered_map reference_wrapper pair string size_t
int double char bool const private public template typename class struct
nullptr NULL true false new delete if return
sizeof strlen printf cout endl operator
at size empty capacity reserve grow push_back pop_back insert erase get append find
nnz sparsity fromDenseMatrix add search remove isEmpty index pop slice
getData getNext setData setNext begin end before_begin front back
push_front pop_front emplace_front insert_after erase_after remove_if unique sort
clear distance next ref move
head tail prev cur previous current temp next data header trailer count lastIndex maxSize
myArray bigger newCapacity newNode left right rows cols row col val value values pointers
refs primes names flat raw fixed dynamic result other item item1 item2 it pos inserted students start stop'''.split()
WORD = r'[A-Za-z_][A-Za-z_0-9]*'
VOCAB = '(?:' + '|'.join(re.escape(t) for t in sorted(set(TERMS),key=lambda t:(-len(t),t))) + ')'
PARENS = r'\((?:[^()\n]|\((?:[^()\n]|\([^()\n]*\))*\))*\)'
TEMPLATE = r'<(?:[^<>\n]|<[^<>\n]*>)*>'
BASE = (r'(?:operator(?:\[\]|\(\)|==|!=|\+|-|\*|/)|'
        + WORD + r'(?:(?:::|->|\.)'+WORD+r')+|'
        + WORD + r'(?=\()|'+WORD+r'(?=\[)|\.?'+VOCAB+')')
SYMBOL = r'(?:\+\+|--)?'+BASE+'(?:'+TEMPLATE+r')?(?:'+PARENS+r')?(?:\[[^\]\n]*\])*(?:\s*[*&](?![A-Za-z_]))?'
PATTERN = (r'(?<![A-Za-z_0-9.-])(?:'
           r'(?:[A-Za-z_0-9-]+/)*[A-Za-z_0-9-]+\.(?:hpp|cpp|h)|'
           +SYMBOL+r'(?:\s*(?:==|!=|=(?!=))\s*(?:'+SYMBOL+r'|[0-9]+))?'
           +r'|\*[A-Za-z_][A-Za-z_0-9]*|\[\]|->|\+\+)(?![A-Za-z_0-9-])')
TOKEN_RE = re.compile(PATTERN)
MATH_RE = re.compile(r'(\$\$.*?\$\$|\$[^$]*\$)',re.S)


def is_term_prose(token, before, after):
    if token=='string' and re.search(r'(?:C-style|C)\s+$',before):return True
    if token=='double' and re.match(r'\s+free\b',after):return True
    if token=='Linear' and re.match(r'\s+Linked\b',after):return True
    if token=='row' and re.search(r'\(\s*$',before) and re.match(r'\s*,\s*(?:col|column)\b',after):return True
    if token in {'col','column'} and re.search(r'\(\s*row\s*,\s*$',before) and re.match(r'\s*[,)]',after):return True
    if token in {'val','value'} and re.search(r'\(\s*row\s*,\s*(?:col|column)\s*,\s*$',before) and re.match(r'\s*\)',after):return True
    if token in {'Linear','list'} and (re.search(r'(?:Linear|linked)\s+$',before,re.I) or re.match(r'\s+list\b',after)):
        return True
    if token=='Node' and re.search(r'[（(]\s*$',before) and re.match(r'\s*[）)]',after):
        return True
    if token in {'row','col','column'} and re.match(r'\s*[＝=：:]\s*[列欄]',after):
        return True
    return False


def code_text(raw):
    out=[]
    for part in MATH_RE.split(raw):
        if part.startswith('$'):
            out.append(part);continue
        plain=unescape(part);last=0
        for match in TOKEN_RE.finditer(plain):
            out.append(escape(plain[last:match.start()],quote=False))
            token=match[0];safe=escape(token,quote=False)
            out.append(safe if is_term_prose(token,plain[:match.start()],plain[match.end():]) else '<code>'+safe+'</code>')
            last=match.end()
        out.append(escape(plain[last:],quote=False))
    return ''.join(out)


def browser_formatter():
    return (Path(__file__).parent/'inline_code.js').read_text().replace('/*TOKEN_PATTERN*/',json.dumps(PATTERN))


def clean_natural_code(text):
    text=re.sub(r'(C(?:-style)?\s+)<code>string</code>',r'\1string',text)
    text=text.replace('<code>double</code> free','double free')
    text=text.replace('<code>Linear</code> Linked Structures','Linear Linked Structures')
    text=re.sub(r'\((?:<code>)?row(?:</code>)?\s*,\s*(?:<code>)?(col|column)(?:</code>)?(\s*,\s*(?:<code>)?(val|value)(?:</code>)?)?\)',lambda m:re.sub(r'</?code>','',m[0]) if '<code>' in m[0] else m[0],text)
    return text
