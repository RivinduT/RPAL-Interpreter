# Defined the Core object definitions for our RPAL-Interpreter project

class Delta:
    def __init__(self, number):
        self.number = number

class Tau:
    def __init__(self, number):
        self.number = number

class Lambda:
    def __init__(self, number, boundedVariable=None, environment=None):
        self.number = number
        self.boundedVariable = boundedVariable
        self.environment = environment

class Eta:
    def __init__(self, number, boundedVariable=None, environment=None):
        self.number = number
        self.boundedVariable = boundedVariable
        self.environment = environment
