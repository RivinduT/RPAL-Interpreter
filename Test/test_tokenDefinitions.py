import unittest
import sys, os

# ─── Make sure "<project_root>/src" is on sys.path ───
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)

from src.tokenDefinitions import Token

class TestToken(unittest.TestCase):
    def test_token_properties(self):
        t = Token("hello", "<ID>", 3)
        self.assertEqual(t.content, "hello")
        self.assertEqual(t.tokenType, "<ID>")
        self.assertEqual(t.lineNumber, 3)

        # By default, flags are False
        self.assertFalse(t.isFirstToken)
        self.assertFalse(t.isLastToken)

    def test_mark_methods(self):
        t = Token("world", "<ID>", 1)

        # markAsFirst → isFirstToken = True
        t.markAsFirst()
        self.assertTrue(t.isFirstToken)

        # markAsLast → isLastToken = True
        t.markAsLast()
        self.assertTrue(t.isLastToken)

        # markAsKeyword → tokenType changes to "<KEYWORD>"
        t.markAsKeyword()
        self.assertEqual(t.tokenType, "<KEYWORD>")

if __name__ == '__main__':
    unittest.main()
