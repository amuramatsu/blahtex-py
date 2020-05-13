import unittest
from blahtex import Blahtex

class TestAll(unittest.TestCase):

    def test_convert(self):
        bt = Blahtex()
        self.assertEqual(
            bt.convert("\sqrt{3}").replace("\n", ""),
            '<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline"><msqrt><mn>3</mn></msqrt></math>')

    def test_options(self):
        bt = Blahtex()
        options = bt.get_options()
        bt.set_options(options)
        
if __name__ == '__main__':
    unittest.main()
