import unittest
from src.lexicalAnalyzer import extractTokens

class TestLexicalAnalyzer(unittest.TestCase):
    def test_identifier_token(self):
        # Test tokenization of identifier 'let'
        test_input = "let x = 5;"
        tokens = extractTokens(test_input)
        self.assertEqual(tokens[0].tokenType, "<IDENTIFIER>")
        self.assertEqual(tokens[0].content, "let")

    def test_number_token(self):
        # Test tokenization of integer literal
        test_input = "42"
        tokens = extractTokens(test_input)
        self.assertEqual(tokens[0].tokenType, "<INTEGER>")
        self.assertEqual(tokens[0].content, "42")

    def test_operator_token(self):
        # Test tokenization of arithmetic operator
        test_input = "+"
        tokens = extractTokens(test_input)
        self.assertEqual(tokens[0].tokenType, "<OPERATOR>")
        self.assertEqual(tokens[0].content, "+")

    def test_string_token(self):
        # Test tokenization of string literal
        test_input = "'hello'"
        tokens = extractTokens(test_input)
        self.assertEqual(tokens[0].tokenType, "<STRING>")
        self.assertEqual(tokens[0].content, "'hello'")

    def test_complex_expression(self):
        # Test tokenization of complex expression with multiple tokens
        test_input = "let x = 5 + 3;"
        tokens = extractTokens(test_input)
        
        # Filter out DELETE tokens
        tokens = [t for t in tokens if t.tokenType != "<DELETE>"]
        
        self.assertEqual(len(tokens), 5)  # let, x, =, 5, +, 3, ;
        self.assertEqual(tokens[0].content, "let")
        self.assertEqual(tokens[1].content, "x")
        self.assertEqual(tokens[2].content, "=")
        self.assertEqual(tokens[3].content, "5")
        self.assertEqual(tokens[4].content, "+")

if __name__ == '__main__':
    unittest.main() 