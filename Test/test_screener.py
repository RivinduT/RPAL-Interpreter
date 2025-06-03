import unittest
import sys, os

# ─── Make sure "<project_root>/src" is on sys.path ───
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)

from src.screener import filterTokens
from src.tokenDefinitions import Token

class TestScreener(unittest.TestCase):
    def setUp(self):
        # Create a temporary RPAL file for testing
        self.test_file = os.path.join(os.path.dirname(__file__), 'temp_test.rpal')
        with open(self.test_file, 'w') as f:
            f.write("let X = 5 in X")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_filter_tokens_valid(self):
        tokens, invalid_flag, invalid_token = filterTokens(self.test_file)
        # No invalid tokens in "let X = 5 in X"
        self.assertFalse(invalid_flag)
        self.assertIsNone(invalid_token)

        # tokens should be a list of Token objects
        self.assertIsInstance(tokens, list)
        self.assertTrue(all(isinstance(tok, Token) for tok in tokens))

        # RPAL keywords "let" and "in" must be marked as <KEYWORD>
        keyword_contents = [tok.content for tok in tokens if tok.content in ("let", "in")]
        self.assertEqual(set(keyword_contents), {"let", "in"})

        for tok in tokens:
            if tok.content in ("let", "in"):
                self.assertEqual(tok.tokenType, "<KEYWORD>")

if __name__ == '__main__':
    unittest.main()
