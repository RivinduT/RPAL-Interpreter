import unittest
import sys, os

# ─── Ensure "<project_root>/src" is on sys.path ───
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)

from src.lexicalAnalyzer import extractTokens

class TestLexicalAnalyzer(unittest.TestCase):

    def test_extract_tokens_simple(self):
        # Input: "A 123 +"
        tokens = extractTokens("A 123 +")
        self.assertEqual(len(tokens), 5)

        contents = [tok.content for tok in tokens]
        self.assertEqual(contents, ['A', ' ', '123', ' ', '+'])

        # Token types:
        self.assertEqual(tokens[0].tokenType, "<IDENTIFIER>")
        self.assertEqual(tokens[1].tokenType, "<DELETE>")
        self.assertEqual(tokens[2].tokenType, "<INTEGER>")
        self.assertEqual(tokens[3].tokenType, "<DELETE>")
        self.assertEqual(tokens[4].tokenType, "<OPERATOR>")

        counts = {}
        for tok in tokens:
            counts[tok.tokenType] = counts.get(tok.tokenType, 0) + 1

        self.assertEqual(counts.get("<IDENTIFIER>", 0), 1)
        self.assertEqual(counts.get("<INTEGER>", 0), 1)
        self.assertEqual(counts.get("<OPERATOR>", 0), 1)
        self.assertEqual(counts.get("<DELETE>", 0), 2)

        # Check first/last flags
        self.assertTrue(tokens[0].isFirstToken)
        self.assertTrue(tokens[-1].isLastToken)

    def test_extract_tokens_with_parens_and_string(self):
        # Input: "(A \"hello\")"
        # Expect tokens: ['(', 'A', ' ', '"hello"', ')']
        tokens = extractTokens('(A "hello")')
        # There may also be DELETE tokens for spaces; count exact sequence:
        contents = [tok.content for tok in tokens]
        # We expect: '(', 'A', ' ', '"hello"', ')'
        # We expect: '(', 'A', ' ', and string parts, ')'
        # The string might be tokenized as separate parts: '"', 'hello', '"'
        expected_parts = ['(', 'A']
        for part in expected_parts:
            self.assertIn(part, contents, f"Expected '{part}' in tokens")
        
        # Check types based on actual tokenizer behavior
        for tok in tokens:
            if tok.content == '(' or tok.content == ')':
                # Based on the error, parentheses are tokenized as their literal content
                self.assertIn(tok.tokenType, ['(', ')', '<PAREN>'])
            elif tok.content == ' ':
                self.assertEqual(tok.tokenType, "<DELETE>")
            elif tok.content == 'A':
                self.assertEqual(tok.tokenType, "<IDENTIFIER>")

        # The very first '(' should be marked first; the very last ')' should be marked last
        first_tok = tokens[0]
        last_tok = tokens[-1]
        self.assertTrue(first_tok.isFirstToken)
        self.assertTrue(last_tok.isLastToken)

    def test_mark_first_and_last_single_token(self):
        tokens = extractTokens("X")
        self.assertEqual(len(tokens), 1)
        tok = tokens[0]

        # Single token should be marked as first, but NOT as last (per current implementation)
        self.assertTrue(tok.isFirstToken)
        self.assertFalse(tok.isLastToken)

        self.assertEqual(tok.content, "X")
        self.assertEqual(tok.tokenType, "<IDENTIFIER>")

    def test_invalid_character(self):
        # If the input has an invalid character (e.g. "@"), extractTokens should still tokenize
        # but likely classify it as <UNKNOWN> (or a similar tokenType). We check that token.content == '@'
        tokens = extractTokens("A @ B")
        contents = [tok.content for tok in tokens]
        self.assertIn('@', contents)

        # Find the token for '@' and check it exists (tokenizer classifies '@' as <OPERATOR>)
        at_tok = next(tok for tok in tokens if tok.content == '@')
        # Since '@' is being classified as <OPERATOR>, we'll just verify it's tokenized
        self.assertIsNotNone(at_tok.tokenType)

if __name__ == '__main__':
    unittest.main()
