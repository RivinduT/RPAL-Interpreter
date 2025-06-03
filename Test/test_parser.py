import unittest
import sys, os

# ─── Ensure "<project_root>/src" is on sys.path ───
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)

from src.parser import parse
from src.node import Node

class TestParser(unittest.TestCase):
    def setUp(self):
        # 1) Minimal valid RPAL snippet
        self.valid_file = os.path.join(os.path.dirname(__file__), 'temp_parse_valid.rpal')
        with open(self.valid_file, 'w') as f:
            f.write("let A x = x in A 5")

        # 2) Nested let with pure function application (no arithmetic)
        #    let A x = x in let B y = y in B (A 3)
        self.nested_file = os.path.join(os.path.dirname(__file__), 'temp_parse_nested.rpal')
        with open(self.nested_file, 'w') as f:
            f.write("let A x = x in let B y = y in B (A 3)")

        # 3) Incomplete snippet (missing 'in' clause)
        self.bad_file = os.path.join(os.path.dirname(__file__), 'temp_parse_bad.rpal')
        with open(self.bad_file, 'w') as f:
            f.write("let A x = x")  # no "in" part

    def tearDown(self):
        for path in (self.valid_file, self.nested_file, self.bad_file):
            if os.path.exists(path):
                os.remove(path)

    def test_parse_returns_node_on_valid(self):
        root = parse(self.valid_file)
        self.assertIsInstance(root, Node)

    def test_parse_nested_let(self):
        # Now without arithmetic—just nested lets and applications
        node = parse(self.nested_file)
        self.assertIsInstance(node, Node)

    def test_parse_incomplete_syntax_raises(self):
        # Incomplete 'let A x = x' should cause a SystemExit (syntax error)
        with self.assertRaises(SystemExit):
            parse(self.bad_file)

if __name__ == '__main__':
    unittest.main()
