import unittest
import sys, os

# ─── Ensure "<project_root>/src" is on sys.path ───
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)


from src.stack import Stack

def test_stack_indexing_behavior(self):
    # Test that indexing follows list behavior (0 is bottom, -1 is top)
    self.stack.push("bottom")
    self.stack.push("middle")
    self.stack.push("top")
    
    # Index 0 is the bottom (first pushed)
    self.assertEqual(self.stack[0], "bottom")
    # Index -1 is the top (last pushed)
    self.assertEqual(self.stack[-1], "top")
    # Index 1 is the middle
    self.assertEqual(self.stack[1], "middle")

def test_stack_modification_via_setitem(self):
    # Test __setitem__ functionality
    self.stack.push("original")
    self.stack.push("value")
    
    # Modify the top element (last index)
    self.stack[-1] = "modified"
    self.assertEqual(self.stack.pop(), "modified")
    self.assertEqual(self.stack.pop(), "original")

def test_stack_iteration_reversed(self):
    # Test __reversed__ method
    items = [1, 2, 3, 4]
    for item in items:
        self.stack.push(item)
    
    # Reversed should give us items from top to bottom
    reversed_items = list(reversed(self.stack))
    self.assertEqual(reversed_items, [4, 3, 2, 1])

def test_stack_repr(self):
    # Test string representation
    self.stack.push("a")
    self.stack.push("b")
    expected = "['a', 'b']"
    self.assertEqual(repr(self.stack), expected)

def test_empty_stack_repr(self):
    # Test repr of empty stack
    self.assertEqual(repr(self.stack), "[]")

def test_different_stack_types_error_messages(self):
    # Test CSE stack error message
    cse_stack = Stack("CSE")
    with self.assertRaises(SystemExit):
        cse_stack.pop()
    
    # Test AST stack error message  
    ast_stack = Stack("AST")
    with self.assertRaises(SystemExit):
        ast_stack.pop()

def test_multiple_push_pop_cycles(self):
    # Test multiple push/pop cycles
    for i in range(5):
        self.stack.push(i)
        self.assertEqual(self.stack.pop(), i)
        self.assertTrue(self.stack.is_empty())

def test_stack_with_none_values(self):
    # Test pushing None values
    self.stack.push(None)
    self.stack.push("not_none")
    self.stack.push(None)
    
    self.assertEqual(self.stack.pop(), None)
    self.assertEqual(self.stack.pop(), "not_none")
    self.assertEqual(self.stack.pop(), None)

def test_stack_with_mixed_types(self):
    # Test with different data types
    items = [1, "string", [1, 2, 3], {"key": "value"}, True]
    for item in items:
        self.stack.push(item)
    
    # Pop in reverse order
    for item in reversed(items):
        self.assertEqual(self.stack.pop(), item)

        self.assertEqual(self.stack.pop(), 'third')
        self.assertEqual(self.stack.pop(), 'second')
        self.assertEqual(self.stack.pop(), 'first')
        self.assertTrue(self.stack.is_empty())

    def test_top_element_via_getitem(self):
        # Although peek() is not present, __getitem__(0) returns the top element
        self.stack.push("hello")
        self.stack.push("world")
        # The “top” is at index 0 of the underlying list
        self.assertEqual(self.stack[0], "world")
        # Confirm stack is still non‐empty after accessing
        self.assertFalse(self.stack.is_empty())

    def test_underflow(self):
        # Popping from an empty stack should call exit(1), raising SystemExit
        with self.assertRaises(SystemExit):
            self.stack.pop()

    def test_clear_and_is_empty(self):
        # Push then manually clear all elements
        self.stack.push(1)
        self.stack.push(2)
        # Clear by popping until empty
        self.stack.pop()
        self.stack.pop()
        self.assertTrue(self.stack.is_empty())

if __name__ == '__main__':
    unittest.main()
