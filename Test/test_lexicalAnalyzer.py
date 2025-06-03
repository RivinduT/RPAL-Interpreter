# File: Test/test_lexicalAnalyzer.py

import unittest
import sys, os

# ─── Make sure "<project_root>/src" is on sys.path so that:
#     from src.lexicalAnalyzer import extractTokens
#     and from src.tokenDefinitions import Token
#     both resolve correctly.
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)

from src.lexicalAnalyzer import extractTokens
from src.tokenDefinitions import Token

class TestLexicalAnalyzer(unittest.TestCase):

    def test_extract_tokens_simple(self):
        # Input: "A 123 +"
        # extractTokens returns five tokens: ['A', ' ', '123', ' ', '+'],
        # where the spaces are tokenized as <DELETE>.
        tokens = extractTokens("A 123 +")
        self.assertEqual(len(tokens), 5)

        # Check that the sequence of contents is exactly as given:
        contents = [tok.content for tok in tokens]
        self.assertEqual(contents, ['A', ' ', '123', ' ', '+'])

        # Check types: 
        #   - 'A'      → <IDENTIFIER>
        #   - ' '      → <DELETE>
        #   - '123'    → <INTEGER>
        #   - ' '      → <DELETE>
        #   - '+'      → <OPERATOR>
        self.assertEqual(tokens[0].tokenType, "<IDENTIFIER>")
        self.assertEqual(tokens[1].tokenType, "<DELETE>")
        self.assertEqual(tokens[2].tokenType, "<INTEGER>")
        self.assertEqual(tokens[3].tokenType, "<DELETE>")
        self.assertEqual(tokens[4].tokenType, "<OPERATOR>")

        # Exactly one <IDENTIFIER>, one <INTEGER>, one <OPERATOR>, and two <DELETE>
        types_count = {}
        for tok in tokens:
            types_count[tok.tokenType] = types_count.get(tok.tokenType, 0) + 1

        self.assertEqual(types_count.get("<IDENTIFIER>", 0), 1)
        self.assertEqual(types_count.get("<INTEGER>", 0), 1)
        self.assertEqual(types_count.get("<OPERATOR>", 0), 1)
        self.assertEqual(types_count.get("<DELETE>", 0), 2)

        # The very first token ('A') should have isFirstToken = True
        self.assertTrue(tokens[0].isFirstToken)
        # The very last token ('+') should have isLastToken = True
        self.assertTrue(tokens[-1].isLastToken)

    def test_mark_first_and_last_single_token(self):
        # If input has exactly one token "X", extractTokens yields a single Token.
        single_tok_list = extractTokens("X")

        # There should be exactly one returned Token
        self.assertEqual(len(single_tok_list), 1)
        tok = single_tok_list[0]

        # Check that it is marked as first—but not as last (per current implementation)
        self.assertTrue(tok.isFirstToken, "Single token should be marked as first")
        self.assertFalse(tok.isLastToken, "Single token is not marked as last in this version")

        # And its content/type should be <IDENTIFIER>
        self.assertEqual(tok.content, "X")
        self.assertEqual(tok.tokenType, "<IDENTIFIER>")

if __name__ == '__main__':
    unittest.main()
