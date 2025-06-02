class Stack:
    def __init__(self, stackType):
        self.stack = []
        self.stackType = stackType
        
    # Returns the stack as a String for debugging purposes if required
    def __repr__(self):
        return str(self.stack)
        
    # Allows indexing into the stack
    def __getitem__(self, index):
        return self.stack[index]
    
    # Allows setting an element at a specific index
    def __setitem__(self, index, value):
        self.stack[index] = value
        
    # Supports iterating over the stack in reverse order
    def __reversed__(self):
        return reversed(self.stack)

    # Adds an item to the top of the stack
    def push(self, item):
        self.stack.append(item)

    # Removes and returns the top item of the stack
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            if self.stackType == "CSE":
                # This means the stack used in the CSE machine has become empty unexpectedly
                print("Error: CSE machine stack underflow.")
            else:
                # This means the stack used for AST generation has become empty unexpectedly
                print("Error: AST stack underflow.")
            exit(1)

    # Checks if the stack is empty
    def is_empty(self):
        return len(self.stack) == 0
