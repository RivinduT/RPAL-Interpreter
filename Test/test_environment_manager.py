import unittest
from src.environmentManager import Environment

class TestEnvironmentManager(unittest.TestCase):
    def setUp(self):
        self.env = Environment(0, None)

    def test_basic_binding(self):
        self.env.variables["x"] = 5
        value = self.env.variables["x"]
        self.assertEqual(value, 5)

    def test_nested_environment(self):
        self.env.variables["x"] = 5
        child_env = Environment(1, self.env)
        child_env.variables["y"] = 10
        
        # Should find both variables
        self.assertEqual(self.env.variables["x"], 5)
        self.assertEqual(child_env.variables["y"], 10)
        
        # Should not find y in parent
        with self.assertRaises(KeyError):
            _ = self.env.variables["y"]

    def test_shadowing(self):
        self.env.variables["x"] = 5
        child_env = Environment(1, self.env)
        child_env.variables["x"] = 10
        
        # Should find the shadowed value
        self.assertEqual(child_env.variables["x"], 10)
        
        # Should find the original value in parent
        self.assertEqual(self.env.variables["x"], 5)

    def test_multiple_bindings(self):
        self.env.variables["x"] = 5
        self.env.variables["y"] = 10
        self.env.variables["z"] = 15
        
        self.assertEqual(self.env.variables["x"], 5)
        self.assertEqual(self.env.variables["y"], 10)
        self.assertEqual(self.env.variables["z"], 15)

    def test_undefined_variable(self):
        with self.assertRaises(KeyError):
            _ = self.env.variables["undefined"]

    def test_environment_chain(self):
        # Create a chain of environments
        self.env.variables["x"] = 1
        child1 = Environment(1, self.env)
        child1.variables["x"] = 2
        child2 = Environment(2, child1)
        child2.variables["x"] = 3
        
        # Should find the most recent binding
        self.assertEqual(child2.variables["x"], 3)
        
        # Should find parent bindings
        self.assertEqual(child1.variables["x"], 2)
        self.assertEqual(self.env.variables["x"], 1)

if __name__ == '__main__':
    unittest.main() 