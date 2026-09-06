"""Regression checks for the omission failures caught by the reader review."""
import unittest
from tools.check_prereq_fidelity import Units, validate
SOURCE='''<div class="container"><section id="lesson"><h2>Topic</h2>
<p>A reference is an alias, not a snapshot.</p>
<table><tr><th>Mode</th><th>Copies</th></tr><tr><td>value</td><td>yes</td></tr><tr><td>reference</td><td>no</td></tr></table>
<svg viewBox="0 0 10 10"><rect width="4" height="4"/><path d="M4 2H8"/></svg>
</section></div>'''
class FidelityTests(unittest.TestCase):
 def setUp(self):self.expected=Units(SOURCE).records()
 def test_exact_page_passes(self):self.assertEqual(validate(SOURCE,self.expected),[])
 def test_same_heading_does_not_replace_explanation(self):
  changed=SOURCE.replace('<p>A reference is an alias, not a snapshot.</p>','')
  self.assertTrue(any('paragraphs' in e for e in validate(changed,self.expected)))
 def test_same_table_title_does_not_replace_missing_row(self):
  changed=SOURCE.replace('<tr><td>reference</td><td>no</td></tr>','')
  self.assertTrue(any('tables' in e for e in validate(changed,self.expected)))
 def test_generic_empty_svg_does_not_replace_diagram(self):
  changed=SOURCE.replace('<rect width="4" height="4"/><path d="M4 2H8"/>','')
  self.assertTrue(any('svgs' in e for e in validate(changed,self.expected)))
 def test_expansion_is_allowed(self):
  changed=SOURCE.replace('</section>','<p>Additional detail.</p></section>')
  self.assertEqual(validate(changed,self.expected),[])
 def test_units_outside_section_are_also_guarded(self):
  source=SOURCE.replace('</section></div>','</section><div id="restored"><p>Restored explanation.</p></div></div>')
  expected=Units(source).records()
  self.assertTrue(validate(source.replace('<p>Restored explanation.</p>',''),expected))
if __name__=='__main__':unittest.main()
