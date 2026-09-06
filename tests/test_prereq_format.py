"""Ensure the actual CLI rejects the format regressions seen in the rewrite."""
import contextlib,io,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import tools.check_prereq as checker
class FormatTests(unittest.TestCase):
 def run_case(self,options=4,front='參考（Reference）',hero=True):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder)
   for sub in ['flashcards_zh','questions_zh']:(root/'data'/sub).mkdir(parents=True)
   (root/'data/prereq_fidelity_contract.json').write_text('{}')
   cards=[{'front':front,'back':'物件的別名。'}]
   answers=[{'answer':str(i),'correct':i==0,'feedback':'理由 '+str(i)} for i in range(options)]
   (root/'data/flashcards_zh/p3.json').write_text(json.dumps(cards))
   (root/'data/questions_zh/p3.json').write_text(json.dumps([{'question':'何者正確？','answers':answers}]))
   buttons=''.join(f'<button class="sq-opt" data-c="{int(a["correct"])}" data-fb="{a["feedback"]}">{a["answer"]}</button>' for a in answers)
   svg='<svg class="hero-graph"><rect width="10" height="10"/></svg>' if hero else ''
   page='<html><body>'+svg+buttons+'<pre data-cpp="run" data-expected="">int main() { return 0; }</pre><script>const FLASHCARDS = '+json.dumps(cards)+'; /* quiz-shuffle v1 */</script></body></html>'
   (root/'p3_functions.html').write_text(page)
   out=io.StringIO()
   with patch.object(checker,'ROOT',root),patch('sys.argv',['check','--pages','p3']),contextlib.redirect_stdout(out):
    failed=checker.main()
   return failed,out.getvalue()
 def test_valid_fixture(self):self.assertFalse(self.run_case()[0])
 def test_two_choices_rejected(self):
  failed,out=self.run_case(options=2);self.assertTrue(failed);self.assertIn('exactly four',out)
 def test_missing_english_rejected(self):
  failed,out=self.run_case(front='參考');self.assertTrue(failed);self.assertIn('parenthesized English',out)
 def test_missing_hero_rejected(self):
  failed,out=self.run_case(hero=False);self.assertTrue(failed);self.assertIn('hero SVG',out)
if __name__=='__main__':unittest.main()
