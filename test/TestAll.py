import unittest
from blahtex import Blahtex, BlahtexException

class TestAll(unittest.TestCase):

    def test_convert(self):
        bt = Blahtex()
        self.assertEqual(
            bt.convert("\sqrt{3}"),
            '<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><msqrt><mn>3</mn></msqrt></math>')

    def test_plane1(self):
        bt = Blahtex(mathml_version1_fonts=True)
        self.assertEqual(
            bt.convert("\mathfrak{ABCDEF}"),
            '<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline">'
            '<mrow><mi>\U0001D504</mi>'
            '<mi>\U0001D505</mi>'
            '<mi>\U0000212D</mi>'
            '<mi>\U0001D507</mi>'
            '<mi>\U0001D508</mi>'
            '<mi>\U0001D509</mi></mrow>'
            '</math>')
        
    def test_options(self):
        bt = Blahtex(japanese_font='ipaex.ttf')
        options = bt.get_options()
        self.assertEqual(options['japanese_font'], 'ipaex.ttf')
        options['indented'] = not options['indented']
        bt.set_options(options)
        self.assertEqual(bt.get_options(), options)

    def test_bad_option_value(self):
        bt = Blahtex()
        with self.assertRaises(ValueError):
            bt.not_exist_key = True

    def test_bad_option_value(self):
        bt = Blahtex()
        bt.other_encoding = Blahtex.ENCODING.NUMERIC
        with self.assertRaises(ValueError):
            bt.other_encoding = 100

    def test_exception_no_input(self):
        bt = Blahtex()
        with self.assertRaises(ValueError):
            bt.get_mathml()
            
    def test_exception_bad_tex(self):
        bt = Blahtex()
        with self.assertRaises(BlahtexException):
            bt.convert(r'\badcommand')
    
if __name__ == '__main__':
    unittest.main()
