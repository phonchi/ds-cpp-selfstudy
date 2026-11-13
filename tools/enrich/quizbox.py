"""Shared quiz-box markup for the chapter pages (the chapter 3-6 style: (A)-(D) options judged by quizCheck).

Chapters 7 and 9 render their in-text quizzes with quiz_box(); tools/apply_zh.py renders the chapter 7-9
self-test banks with it too. quizCheck writes data-fb into the feedback box with innerHTML, so plain-text
feedback is HTML-escaped once and then attribute-escaped (escape(escape(fb))). Leading 「正確。」/「不對。」
are dropped because quizCheck already prints 正確 ✓ / 不對 ✗.
"""
import re
from html import escape

LEAD = re.compile(r'^(正確|不對)。\s*')

QUIZ_CSS = """.quiz-box{background:var(--card);border:2px solid var(--accent2);border-radius:12px;padding:1.3rem 1.5rem;margin:1.5rem 0;}
.quiz-box .quiz-label{font-family:'JetBrains Mono',monospace;font-size:.78rem;color:var(--accent);font-weight:700;letter-spacing:.1em;margin-bottom:.5rem;}
.quiz-options{display:flex;flex-direction:column;gap:.5rem;margin:.8rem 0;}
.quiz-opt{display:flex;align-items:center;gap:.6rem;padding:.55rem .9rem;background:var(--paper);border:2px solid var(--card-border);border-radius:8px;cursor:pointer;transition:all .2s;font-family:'JetBrains Mono',monospace;font-size:.86rem;}
.quiz-opt:hover{border-color:var(--accent2);}
.quiz-opt .opt-letter{font-weight:700;color:var(--accent2);min-width:22px;}
.quiz-opt.correct{background:#eafaf1;border-color:var(--accent3);}
.quiz-opt.correct .opt-letter{color:var(--accent3);}
.quiz-opt.wrong{background:#fef5e7;border-color:var(--accent);}
.quiz-opt.wrong .opt-letter{color:var(--accent);}
.quiz-feedback{margin-top:.7rem;padding:.7rem 1rem;border-radius:8px;font-size:.88rem;display:none;}
.quiz-feedback.show{display:block;}
.quiz-feedback.correct{background:#eafaf1;color:var(--accent3);border-left:4px solid var(--accent3);}
.quiz-feedback.wrong{background:#fef5e7;color:var(--accent);border-left:4px solid var(--accent);}
.quiz-box .quiz-code{margin:.6rem 0;padding:.6rem .8rem;background:var(--paper);border:1px solid var(--card-border);border-radius:6px;font-size:.82rem;overflow-x:auto;white-space:pre;}"""

QUIZ_CHECK_JS = """<script id="quiz-check">
/* quiz-box handler (same as chapters 3-6 and 8) */
function quizCheck(quizId, optEl) {
  const isCorrect = optEl.dataset.correct === 'true';
  optEl.parentElement.querySelectorAll('.quiz-opt').forEach(o => o.classList.remove('correct', 'wrong'));
  optEl.classList.add(isCorrect ? 'correct' : 'wrong');
  const fb = document.getElementById(`${quizId}Feedback`);
  fb.classList.remove('correct', 'wrong');
  fb.classList.add('show', isCorrect ? 'correct' : 'wrong');
  fb.innerHTML = (isCorrect ? '<strong>正確 ✓</strong> ' : '<strong>不對 ✗</strong> ') + (optEl.dataset.fb || '');
}
</script>"""


def plain_fb(fb):
    """Feedback stored as plain text -> HTML for innerHTML (leading 正確。/不對。 removed)."""
    body = LEAD.sub('', fb.strip())
    assert body, fb
    return escape(body, quote=False)


def quiz_box(qid, label, question_html, answers, anchor='', code_html='', attr=escape):
    """answers: [(correct: bool, text_html, feedback_html)] x4, exactly one correct.

    attr turns the feedback HTML into an attribute value (apply_zh passes its own esc_attr)."""
    assert len(answers) == 4 and sum(bool(c) for c, _, _ in answers) == 1, qid
    opts = '\n'.join(
        f'    <div class="quiz-opt" data-correct="{"true" if c else "false"}" data-fb="{attr(fb)}" '
        f'onclick="quizCheck(\'{qid}\', this)"><span class="opt-letter">({chr(65 + j)})</span> '
        f'<span class="opt-text">{text}</span></div>'
        for j, (c, text, fb) in enumerate(answers))
    ident = f' id="{anchor}"' if anchor else ''
    return (f'<div class="quiz-box"{ident}>\n  <div class="quiz-label">{label}</div>\n  <p>{question_html}</p>{code_html}\n'
            f'  <div class="quiz-options" id="{qid}Options">\n{opts}\n  </div>\n'
            f'  <div class="quiz-feedback" id="{qid}Feedback"></div>\n</div>')


def lecture_quiz(bank, key, prefix='q'):
    """Render one entry of a LECTURE_QUIZ dict ({question, answers:[{answer, correct, feedback}], label?})."""
    q = bank[key]
    qid = prefix + ''.join(p[:1].upper() + p[1:] for p in re.split(r'[-_]', key))
    label = 'QUIZ' + (f' · {q["label"]}' if q.get('label') else '')
    answers = [(a['correct'], escape(a['answer'], quote=False), plain_fb(a['feedback'])) for a in q['answers']]
    return quiz_box(qid, label, escape(q['question'], quote=False), answers, anchor=f'quiz-{key}')


def ensure_quiz_check(s):
    """Idempotently keep one <script id="quiz-check"> before </body>."""
    if '<script id="quiz-check">' in s:
        return re.sub(r'<script id="quiz-check">.*?</script>', lambda _m: QUIZ_CHECK_JS, s, count=1, flags=re.S)
    k = s.rindex('</body>')
    return s[:k] + QUIZ_CHECK_JS + '\n' + s[k:]
