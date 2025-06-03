'''
Defines the Environment class used to manage variable scopes and 
hierarchical relationships between execution contexts in the RPAL-interpreter.
'''

class Environment:
    def __init__(self, envNumber, parentEnv):
        self.name = f"e_{envNumber}"
        self.variables = {}
        self.children = []
        self.parent = parentEnv

    # Store a variable in the current environment scope.
    def addVariable(self, key, value):
        self.variables[key] = value
        
    # Attach a new child environment and inherit current variables.
    def addChild(self, childEnv):
        self.children.append(childEnv)
        childEnv.variables.update(self.variables)

