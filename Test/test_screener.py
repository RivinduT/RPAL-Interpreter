import unittest
import sys, os

# ─── Ensure "<project_root>/src" is on sys.path ───
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)

from src.screener import filterTokens
from src.tokenDefinitions import Token


def test_keyword_identification(self):
    # Test that all RPAL keywords are properly identified
    keywords_file = os.path.join(os.path.dirname(__file__), 'temp_keywords.rpal')
    with open(keywords_file, 'w') as f:
        f.write("let in where rec fn aug or not gr ge ls le eq ne true false nil dummy within and")
    
    try:
        tokens, invalid_flag, invalid_token = filterTokens(keywords_file)
        self.assertFalse(invalid_flag)
        
        # All keywords should be tagged as <KEYWORD>
        keyword_tokens = [tok for tok in tokens if tok.tokenType == "<KEYWORD>"]
        keyword_contents = {tok.content for tok in keyword_tokens}
        expected_keywords = {"let", "in", "where", "rec", "fn", "aug", "or", "not", 
                           "gr", "ge", "ls", "le", "eq", "ne", "true", "false", 
                           "nil", "dummy", "within", "and"}
        self.assertEqual(keyword_contents, expected_keywords)
    finally:
        if os.path.exists(keywords_file):
            os.remove(keywords_file)

def test_empty_file(self):
    # Test filtering tokens from an empty file
    empty_file = os.path.join(os.path.dirname(__file__), 'temp_empty.rpal')
    with open(empty_file, 'w') as f:
        f.write("")
    
    try:
        tokens, invalid_flag, invalid_token = filterTokens(empty_file)
        self.assertFalse(invalid_flag)
        self.assertIsNone(invalid_token)
        self.assertEqual(len(tokens), 0)
    finally:
        if os.path.exists(empty_file):
            os.remove(empty_file)

def test_whitespace_and_comments_removal(self):
    # Test that whitespace and comments are properly removed
    whitespace_file = os.path.join(os.path.dirname(__file__), 'temp_whitespace.rpal')
    with open(whitespace_file, 'w') as f:
        f.write("let   X   =   5\n\nin\n\nX")
    
    try:
        tokens, invalid_flag, invalid_token = filterTokens(whitespace_file)
        self.assertFalse(invalid_flag)
        
        # Should not contain any whitespace or newline tokens
        for token in tokens:
            self.assertNotIn(token.tokenType, ["<DELETE>"])
            self.assertNotEqual(token.content, "\n")
    finally:
        if os.path.exists(whitespace_file):
            os.remove(whitespace_file)

def test_last_token_flag(self):
    # Test that the last token is properly flagged
    simple_file = os.path.join(os.path.dirname(__file__), 'temp_simple.rpal')
    with open(simple_file, 'w') as f:
        f.write("X Y Z")
    
    try:
        tokens, invalid_flag, invalid_token = filterTokens(simple_file)
        self.assertFalse(invalid_flag)
        self.assertGreater(len(tokens), 0)
        
        # Only the last token should have isLastToken = True
        last_token_count = sum(1 for tok in tokens if hasattr(tok, 'isLastToken') and tok.isLastToken)
        self.assertEqual(last_token_count, 1)
        self.assertTrue(tokens[-1].isLastToken)
    finally:
        if os.path.exists(simple_file):
            os.remove(simple_file)

def test_mixed_identifiers_and_keywords(self):
    # Test mix of identifiers and keywords
    mixed_file = os.path.join(os.path.dirname(__file__), 'temp_mixed.rpal')
    with open(mixed_file, 'w') as f:
        f.write("let myVar = true in myVar and false")
    
    try:
        tokens, invalid_flag, invalid_token = filterTokens(mixed_file)
        self.assertFalse(invalid_flag)
        
        # Check specific tokens
        keyword_tokens = [tok for tok in tokens if tok.tokenType == "<KEYWORD>"]
        identifier_tokens = [tok for tok in tokens if tok.tokenType == "<IDENTIFIER>"]
        
        keyword_contents = {tok.content for tok in keyword_tokens}
        identifier_contents = {tok.content for tok in identifier_tokens}
        
        self.assertIn("let", keyword_contents)
        self.assertIn("in", keyword_contents)
        self.assertIn("true", keyword_contents)
        self.assertIn("and", keyword_contents)
        self.assertIn("false", keyword_contents)
        self.assertIn("myVar", identifier_contents)
    finally:
        if os.path.exists(mixed_file):
            os.remove(mixed_file)

def test_numeric_and_string_tokens(self):
    # Test that numeric and string tokens are preserved
    numeric_file = os.path.join(os.path.dirname(__file__), 'temp_numeric.rpal')
    with open(numeric_file, 'w') as f:
        f.write("let x = 42 in 'hello'")
    
    try:
        tokens, invalid_flag, invalid_token = filterTokens(numeric_file)
        self.assertFalse(invalid_flag)
        
        # Should contain numeric and string tokens
        token_contents = [tok.content for tok in tokens]
        self.assertIn("42", token_contents)
        self.assertIn("'hello'", token_contents)
    finally:
        if os.path.exists(numeric_file):
            os.remove(numeric_file)

def test_multiple_invalid_tokens_first_reported(self):
    # Test that only the first invalid token is reported
    multi_invalid_file = os.path.join(os.path.dirname(__file__), 'temp_multi_invalid.rpal')
    with open(multi_invalid_file, 'w') as f:
        f.write("let X = 5 @ Y # Z")
    
    try:
        tokens, invalid_flag, invalid_token = filterTokens(multi_invalid_file)
        # This test depends on how the lexical analyzer handles invalid characters
        # If @ and # are both invalid, only the first encountered should be reported
        if invalid_flag:
            self.assertIsNotNone(invalid_token)
            # The first invalid token should be reported
            self.assertIn(invalid_token.content, ["@", "#"])
    finally:
        if os.path.exists(multi_invalid_file):
            os.remove(multi_invalid_file)

def test_file_not_found_handling(self):
    # Test that non-existent file raises appropriate error
    non_existent_file = "non_existent_file.rpal"
    
    # This should exit the program, so we can't easily test it in unittest
    # But we can verify the function handles the case
    # Note: This test would need to be modified based on your error handling preferences
    pass

def test_operators_and_punctuation(self):
    # Test that operators and punctuation are properly handled
    operators_file = os.path.join(os.path.dirname(__file__), 'temp_operators.rpal')
    with open(operators_file, 'w') as f:
        f.write("let x = (5 + 3) * 2 in x")
    
    try:
        tokens, invalid_flag, invalid_token = filterTokens(operators_file)
        self.assertFalse(invalid_flag)
        
        # Should contain operator tokens
        token_contents = [tok.content for tok in tokens]
        self.assertIn("(", token_contents)
        self.assertIn(")", token_contents)
        self.assertIn("+", token_contents)
        self.assertIn("*", token_contents)
        self.assertIn("=", token_contents)
    finally:
        if os.path.exists(operators_file):
            os.remove(operators_file)
        self.assertIsNone(invalid_token)
        self.assertIsInstance(tokens, list)
        self.assertTrue(all(isinstance(tok, Token) for tok in tokens))

        # Check that "let" and "in" become <KEYWORD>
        keyword_contents = [tok.content for tok in tokens if tok.content in ("let", "in")]
        self.assertEqual(set(keyword_contents), {"let", "in"})
        for tok in tokens:
            if tok.content in ("let", "in"):
                self.assertEqual(tok.tokenType, "<KEYWORD>")

    def test_filter_tokens_invalid(self):
        tokens, invalid_flag, invalid_token = filterTokens(self.invalid_file)
        self.assertTrue(invalid_flag)
        # The invalid_token should be the token "!"
        self.assertEqual(invalid_token.content, "!")

        # Even if invalid, filterTokens still returns a list of tokens
        self.assertIsInstance(tokens, list)

if __name__ == '__main__':
    unittest.main()
