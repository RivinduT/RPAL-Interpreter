import unittest
import sys, os

# ─── Make sure "<project_root>/src" is on sys.path ───
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)

from src.stack import Stack

class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack("Test")

    def test_push_and_pop(self):
        # New stack should be empty
        self.assertTrue(self.stack.is_empty())

        # Push 10, then pop it
        self.stack.push(10)
        self.assertFalse(self.stack.is_empty())
        value = self.stack.pop()
        self.assertEqual(value, 10)
        self.assertTrue(self.stack.is_empty())

    def test_top_element_via_getitem(self):
        # Since peek() does not exist, we use indexing:
        self.stack.push("hello")
        # __getitem__(0) is the top when there's only one
        self.assertEqual(self.stack[0], "hello")
        self.assertFalse(self.stack.is_empty())

    def test_underflow(self):
        # Popping from empty stack → exit(1) → raises SystemExit
        with self.assertRaises(SystemExit):
            self.stack.pop()

if __name__ == '__main__':
    unittest.main()
