import unittest
from src.cseMachine import generateControlStructure, applyRules, getResult
from src.parser import parse
import os

class TestCSEMachine(unittest.TestCase):
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

    def evaluate_expression(self, expression):
        # Helper method to evaluate expressions using CSE machine
        self.write_test_input(expression)
        ast = parse(self.test_file)
        generateControlStructure(ast, 0)
        applyRules()
        return getResult()

    def test_simple_arithmetic(self):
        # Test basic arithmetic operation evaluation
        result = self.evaluate_expression("5 + 3")
        self.assertEqual(result, 8)

    def test_let_expression(self):
        # Test evaluation of let-in binding expression
        result = self.evaluate_expression("let x = 5 in x + 3")
        self.assertEqual(result, 8)

    def test_lambda_application(self):
        # Test evaluation of lambda function application
        result = self.evaluate_expression("(fn x.x + 1) 5")
        self.assertEqual(result, 6)

    def test_where_expression(self):
        # Test evaluation of where clause with multiple bindings
        result = self.evaluate_expression("x + y where x = 5; y = 3")
        self.assertEqual(result, 8)

    def test_recursive_function(self):
        # Test evaluation of recursive factorial function
        factorial = """
        let factorial = rec f = fn x.
            if x=0 then 1 else x*f(x-1)
        in factorial 5
        """
        result = self.evaluate_expression(factorial)
        self.assertEqual(result, 120)

    def test_nested_expressions(self):
        # Test evaluation of nested let expressions
        result = self.evaluate_expression("let x = 5 in let y = 3 in x + y")
        self.assertEqual(result, 8)

    def test_conditional_expression(self):
        # Test evaluation of if-then-else expression
        result = self.evaluate_expression("if 5 > 3 then 10 else 20")
        self.assertEqual(result, 10)

    def test_environment_management(self):
        # Test proper environment management with variable shadowing
        result = self.evaluate_expression("""
        let x = 5 in
        let f = fn y.x + y in
        let x = 10 in
        f 3
        """)
        self.assertEqual(result, 8)  # Should use the outer x (5)

if __name__ == '__main__':
    unittest.main() 