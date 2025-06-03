'''
This module defines the Node class and
'preOrderTraversal' function to recursively display the tree structure using pre-order traversal.
'''

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []  
        self.depth = 0

# Recursive function to print the tree in pre-order fashion with indentation (.) based on depth       
def preOrderTraversal(root):
    if root is None:
        return

    print("." * root.depth + root.value)

    for child in root.children:
        child.depth = root.depth + 1
        preOrderTraversal(child)  