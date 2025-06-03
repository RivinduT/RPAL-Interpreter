import unittest
import sys, os

# ─── Make sure "<project_root>/src" is on sys.path ───
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

        # Child should have inherited variable 'x'
        self.assertIn("x", child.variables)
        self.assertEqual(child.variables["x"], 100)

    def test_parent_and_children_links(self):
        parent = Environment(1, None)
        child = Environment(2, parent)
        parent.addChild(child)

        self.assertIn(child, parent.children)
        self.assertEqual(child.parent, parent)

if __name__ == '__main__':
    unittest.main()
