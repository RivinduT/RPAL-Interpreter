import unittest
import sys, os

# ─── Ensure "<project_root>/src" is on sys.path ───
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
        # Default flags
        self.assertFalse(t.isFirstToken)
        self.assertFalse(t.isLastToken)

    def test_mark_methods(self):
        t = Token("world", "<ID>", 1)

        # markAsFirst
        t.markAsFirst()
        self.assertTrue(t.isFirstToken)

        # markAsLast
        t.markAsLast()
        self.assertTrue(t.isLastToken)

        # markAsKeyword
        t.markAsKeyword()
        self.assertEqual(t.tokenType, "<KEYWORD>")

    def test_chained_marking(self):
        # If we call markAsFirst() then markAsLast(), both flags should be set
        t = Token("foo", "<ID>", 2)
        t.markAsFirst()
        t.markAsLast()
        self.assertTrue(t.isFirstToken)
        self.assertTrue(t.isLastToken)

        # Calling markAsKeyword afterward overwrites tokenType but does not clear flags
        t.markAsKeyword()
        self.assertEqual(t.tokenType, "<KEYWORD>")
        self.assertTrue(t.isFirstToken)
        self.assertTrue(t.isLastToken)

    def test_content_mutability(self):
        # Ensure that Token.content can be read and that we can manually reassign it if desired
        t = Token("bar", "<ID>", 4)
        self.assertEqual(t.content, "bar")
        t.content = "baz"
        self.assertEqual(t.content, "baz")

if __name__ == '__main__':
    unittest.main()
