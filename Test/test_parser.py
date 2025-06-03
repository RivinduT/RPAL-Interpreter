import unittest
from src.parser import parse
from src.node import Node
import os

class TestParser(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for testing
        self.test_file = "test_input.txt"

    def tearDown(self):
        # Clean up the temporary file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def write_test_input(self, content):
        with open(self.test_file, "w") as f:
            f.write(content)

    def test_simple_expression(self):
        self.write_test_input("5 + 3")
        ast = parse(self.test_file)
        
        self.assertIsInstance(ast, Node)
        self.assertEqual(ast.value, "+")
        self.assertEqual(ast.children[0].value, "<INT:5>")
        self.assertEqual(ast.children[1].value, "<INT:3>")

    def test_let_expression(self):
        self.write_test_input("let x = 5 in x + 3")
        ast = parse(self.test_file)
        
        self.assertIsInstance(ast, Node)
        self.assertEqual(ast.value, "let")
        self.assertEqual(ast.children[0].value, "<ID:x>")
        self.assertEqual(ast.children[1].value, "=")

    def test_lambda_expression(self):
        self.write_test_input("fn x.x + 1")
        ast = parse(self.test_file)
        
        self.assertIsInstance(ast, Node)
        self.assertEqual(ast.value, "lambda")
        self.assertEqual(ast.children[0].value, "<ID:x>")
        self.assertEqual(ast.children[1].value, "+")

    def test_where_expression(self):
        self.write_test_input("x + y where x = 5; y = 3")
        ast = parse(self.test_file)
        
        self.assertIsInstance(ast, Node)
        self.assertEqual(ast.value, "where")
        self.assertEqual(ast.children[0].value, "+")

    def test_recursive_expression(self):
        self.write_test_input("rec f = fn x.if x=0 then 1 else x*f(x-1)")
        ast = parse(self.test_file)
        
        self.assertIsInstance(ast, Node)
        self.assertEqual(ast.value, "rec")
        self.assertEqual(ast.children[0].value, "<ID:f>")
        self.assertEqual(ast.children[1].value, "lambda")

if __name__ == '__main__':
    unittest.main() 