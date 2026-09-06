"""Regression checks for the omission failures caught by the reader review."""
import unittest
from tools.check_prereq_fidelity import validate
SOURCE='''<div class="container"><section id="lesson"><h2>Topic</h2>
<p>A reference is an alias, not a snapshot.</p>
<table><tr><th>Mode</th><th>Copies</th></tr><tr><td>value</td><td>yes</td></tr><tr><td>reference</td><td>no</td></tr></table>
<svg viewBox="0 0 10 10"><rect width="4" height="4"/><path d="M4 2H8"/></svg>
</section></div>'''
class FidelityTests(unittest.TestCase):
 def check(self,changed,original=SOURCE):
  return validate(changed,original,{'required_terms':['A reference is an alias']})
 def test_exact_page_passes(self):self.assertEqual(self.check(SOURCE),[])
 def test_required_explanation_cannot_disappear(self):
  changed=SOURCE.replace('<p>A reference is an alias, not a snapshot.</p>','')
  self.assertTrue(any('required concept' in e for e in self.check(changed)))
 def test_missing_table_row_rejected(self):
  changed=SOURCE.replace('<tr><td>reference</td><td>no</td></tr>','')
  self.assertTrue(any('table' in e for e in self.check(changed)))
 def test_empty_svg_rejected(self):
  changed=SOURCE.replace('<rect width="4" height="4"/><path d="M4 2H8"/>','')
  self.assertTrue(any('SVG' in e for e in self.check(changed)))
 def test_expansion_allowed(self):
  self.assertEqual(self.check(SOURCE.replace('</section>','<p>Additional detail.</p></section>')),[])
 def test_section_reorder_rejected(self):
  first='<section id="first"></section>';last='<section id="last"></section>'
  self.assertTrue(self.check(last+SOURCE+first,first+SOURCE+last))
 def test_label_change_preserves_geometry(self):
  original=SOURCE.replace('</svg>','<text x="1" y="2">course</text></svg>')
  self.assertEqual(self.check(original.replace('>course<','>independent example<'),original),[])
 def test_reviewed_reorder_still_requires_all_sections(self):
  first='<section id="first"></section>';last='<section id="last"></section>'
  cfg={'section_order':['last','lesson','first']}
  self.assertEqual(validate(last+SOURCE+first,first+SOURCE+last,cfg),[])
  self.assertTrue(validate(SOURCE+first,first+SOURCE+last,cfg))
 def test_header_rename_does_not_allow_row_removal(self):
  cfg={'table_header_renames':{'Copies':'Copy behavior'}}
  changed=SOURCE.replace('>Copies<','>Copy behavior<')
  self.assertEqual(validate(changed,SOURCE,cfg),[])
  self.assertTrue(validate(changed.replace('<tr><td>reference</td><td>no</td></tr>',''),SOURCE,cfg))
if __name__=='__main__':unittest.main()
