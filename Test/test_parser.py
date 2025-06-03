import unittest
import sys, os

# ─── Make sure "<project_root>/src" is on sys.path ───
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)

from src.parser import parse
from src.node import Node

class TestParser(unittest.TestCase):
    def setUp(self):
        # Minimal valid RPAL snippet: "let A x = x in A 5"
        self.test_file = os.path.join(os.path.dirname(__file__), 'temp_parse.rpal')
        with open(self.test_file, 'w') as f:
            f.write("let A x = x in A 5")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_parse_returns_node(self):
        root = parse(self.test_file)
        self.assertIsInstance(root, Node)

    def test_invalid_syntax_returns_node(self):
        # Parser does NOT exit(1) for this content; it still returns a Node
        bad_file = os.path.join(os.path.dirname(__file__), 'temp_bad.rpal')
        with open(bad_file, 'w') as f:
            f.write("this is not a valid RPAL program")

        root = parse(bad_file)
        self.assertIsInstance(root, Node)
        os.remove(bad_file)

if __name__ == '__main__':
    unittest.main()
