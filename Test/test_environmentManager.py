import unittest
import sys, os

# ─── Ensure "<project_root>/src" is on sys.path ───
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)

from src.environmentManager import Environment

class TestEnvironment(unittest.TestCase):
    def test_add_variable(self):
        env = Environment(1, None)
        env.addVariable("a", 5)
        self.assertIn("a", env.variables)
        self.assertEqual(env.variables["a"], 5)

    def test_child_inheritance(self):
        parent = Environment(1, None)
        parent.addVariable("x", 100)

        child = Environment(2, parent)
        parent.addChild(child)

        # Child inherits 'x'
        self.assertIn("x", child.variables)
        self.assertEqual(child.variables["x"], 100)

    def test_override_in_child_does_not_affect_parent(self):
        parent = Environment(1, None)
        parent.addVariable("v", 42)

        child = Environment(2, parent)
        parent.addChild(child)

        # Child overrides 'v'
        child.addVariable("v", 99)
        self.assertEqual(child.variables["v"], 99)
        # Parent must remain unchanged
        self.assertEqual(parent.variables["v"], 42)

    def test_parent_and_children_links(self):
        parent = Environment(1, None)
        child = Environment(2, parent)
        parent.addChild(child)

        self.assertIn(child, parent.children)
        self.assertEqual(child.parent, parent)

    def test_grandchild_inherits_grandparent(self):
        grandparent = Environment(0, None)
        grandparent.addVariable("g", 7)

        parent = Environment(1, grandparent)
        grandparent.addChild(parent)
        child = Environment(2, parent)
        parent.addChild(child)

        # The child should have inherited "g" from grandparent
        self.assertIn("g", child.variables)
        self.assertEqual(child.variables["g"], 7)

if __name__ == '__main__':
    unittest.main()
