'''
This implements a control structure generator and evaluator 
for RPAL language using a CSE (Control Stack Environment) machine model. 

This parses the standardized abstract syntax tree (AST) into control structures, manages environments,
and evaluates expressions by applying reduction rules, including support for lambda functions, conditionals, tuples, and built-in operations.

The evaluator simulates the execution flow by manipulating a control list and stack,
supporting both user-defined and built-in functions within nested lexical scopes.
'''

from src.ASTtoST import standardize
from src.node import *
from src.environmentManager import Environment
from src.stack import Stack
from src.structures import *

controlStructures = []
controlIndex = 0
control = []
stack = Stack("CSE")  # Stack for the CSE machine
environments = [Environment(0, None)]
currentEnvironment = 0
builtInFunctions = [
    "Order", "Print", "print", "Conc", "Stern", "Stem",
    "Isinteger", "Istruthvalue", "Isstring", "Istuple",
    "Isfunction", "ItoS"
]
printPresent = False

# Function to generate control structures from the AST
def generateControlStructure(rootNode, index):
    global controlIndex

    # Ensure controlStructures list has enough sublists
    while len(controlStructures) <= index:
        controlStructures.append([])

    # Handle lambda expression node
    if rootNode.value == "lambda":
        controlIndex += 1
        leftChild = rootNode.children[0]

        if leftChild.value == ",":
            tempLambda = Lambda(controlIndex)

            boundVars = ""
            for child in leftChild.children:
                boundVars += child.value[4:-1] + ","
            boundVars = boundVars[:-1]

            tempLambda.bounded_variable = boundVars
            controlStructures[index].append(tempLambda)
        else:
            tempLambda = Lambda(controlIndex)
            tempLambda.bounded_variable = leftChild.value[4:-1]
            controlStructures[index].append(tempLambda)

        # Recursively generate for the rest of the children in the lambda
        for child in rootNode.children[1:]:
            generateControlStructure(child, controlIndex)

    # Handle conditional '->' node
    elif rootNode.value == "->":
        controlIndex += 1
        deltaThen = Delta(controlIndex)
        controlStructures[index].append(deltaThen)
        generateControlStructure(rootNode.children[1], controlIndex)

        controlIndex += 1
        deltaElse = Delta(controlIndex)
        controlStructures[index].append(deltaElse)
        generateControlStructure(rootNode.children[2], controlIndex)

        controlStructures[index].append("beta")
        generateControlStructure(rootNode.children[0], index)

    # Handle tuple constructor 'tau' node
    elif rootNode.value == "tau":
        childCount = len(rootNode.children)
        tauNode = Tau(childCount)
        controlStructures[index].append(tauNode)
        for child in rootNode.children:
            generateControlStructure(child, index)

    # Handle all other nodes (variables, operators, etc.)
    else:
        controlStructures[index].append(rootNode.value)
        for child in rootNode.children:
            generateControlStructure(child, index)


def lookup(nameToken):
    """
    Lookup and convert tokens beginning with '<' and ending with '>'
    into their corresponding internal values.
    """
    name = nameToken[1:-1]
    info = name.split(":")

    if len(info) == 1:
        value = info[0]
    else:
        dataType = info[0]
        value = info[1]

        if dataType == "INT":
            return int(value)
        elif dataType == "STR":
            return value.strip("'")
        elif dataType == "ID":
            if value in builtInFunctions:
                return value
            else:
                try:
                    value = environments[currentEnvironment].variables[value]
                except KeyError:
                    print(f"Undeclared Identifier: {value}")
                    exit(1)
                else:
                    return value

    if value == "Y*":
        return "Y*"
    elif value == "nil":
        return ()
    elif value == "true":
        return True
    elif value == "false":
        return False


def builtIn(functionName, argument):
    """
    Handles built-in functions like Order, Print, Conc, and type checks.
    Pushes results to the stack as needed.
    """
    global printPresent

    if functionName == "Order":
        # Returns length of a tuple
        stack.push(len(argument))

    elif functionName in ("Print", "print"):
        # Marks print as requested and pushes formatted output
        printPresent = True
        if isinstance(argument, str):
            argument = argument.replace("\\n", "\n").replace("\\t", "\t")
        stack.push(argument)

    elif functionName == "Conc":
        # Concatenate two strings from stack
        stackSymbol = stack.pop()
        control.pop()
        concatenated = argument + stackSymbol
        stack.push(concatenated)

    elif functionName == "Stern":
        # Returns string without first character
        stack.push(argument[1:])

    elif functionName == "Stem":
        # Returns first character of the string
        stack.push(argument[0])

    elif functionName == "Isinteger":
        # Check if argument is an integer
        stack.push(isinstance(argument, int))

    elif functionName == "Istruthvalue":
        # Check if argument is a boolean
        stack.push(isinstance(argument, bool))

    elif functionName == "Isstring":
        # Check if argument is a string
        stack.push(isinstance(argument, str))

    elif functionName == "Istuple":
        # Check if argument is a tuple
        stack.push(isinstance(argument, tuple))

    elif functionName == "Isfunction":
        # Check if argument is a built-in function
        stack.push(argument in builtInFunctions)

    elif functionName == "ItoS":
        # Convert integer to string
        if isinstance(argument, int):
            stack.push(str(argument))
        else:
            print("Error: ItoS function can only accept integers.")
            exit(1)


def applyRules():
    """
    Main evaluator loop that applies reduction rules on the control list and stack.
    Executes the control structure using rules inspired by the CSE machine.
    """
    binaryOperators = ["+", "-", "*", "/", "**", "gr", "ge", "ls", "le", "eq", "ne", "or", "&", "aug"]
    unaryOperators = ["neg", "not"]

    global control
    global currentEnvironment

    while len(control) > 0:
        symbol = control.pop()

        # Rule 1: Lookup tokens beginning with '<' and ending with '>'
        if isinstance(symbol, str) and symbol.startswith("<") and symbol.endswith(">"):
            stack.push(lookup(symbol))

        # Rule 2: Push Lambda with environment info onto stack
        elif isinstance(symbol, Lambda):
            newLambda = Lambda(symbol.number)
            newLambda.bounded_variable = symbol.bounded_variable
            newLambda.environment = currentEnvironment
            stack.push(newLambda)

        # Rule 4: Function application
        elif symbol == "gamma":
            operand1 = stack.pop()
            operand2 = stack.pop()

            # If operand1 is a Lambda expression
            if isinstance(operand1, Lambda):
                currentEnvironment = len(environments)

                lambdaNum = operand1.number
                boundedVar = operand1.bounded_variable
                parentEnvNum = operand1.environment

                parentEnv = environments[parentEnvNum]
                childEnv = Environment(currentEnvironment, parentEnv)
                parentEnv.addChild(childEnv)
                environments.append(childEnv)

                # Add variables to new environment
                varList = boundedVar.split(",")
                if len(varList) > 1:
                    for i, var in enumerate(varList):
                        childEnv.addVariable(var, operand2[i])
                else:
                    childEnv.addVariable(boundedVar, operand2)

                stack.push(childEnv.name)
                control.append(childEnv.name)
                control += controlStructures[lambdaNum]

            # Tuple indexing
            elif isinstance(operand1, tuple):
                stack.push(operand1[operand2 - 1])

            # Eta expansion rule
            elif operand1 == "Y*":
                tempEta = Eta(operand2.number)
                tempEta.bounded_variable = operand2.bounded_variable
                tempEta.environment = operand2.environment
                stack.push(tempEta)

            # Eta application rule
            elif isinstance(operand1, Eta):
                tempLambda = Lambda(operand1.number)
                tempLambda.bounded_variable = operand1.bounded_variable
                tempLambda.environment = operand1.environment

                control.append("gamma")
                control.append("gamma")
                stack.push(operand2)
                stack.push(operand1)
                stack.push(tempLambda)

            # Built-in functions
            elif operand1 in builtInFunctions:
                builtIn(operand1, operand2)

        # Rule 5: Environment switch
        elif isinstance(symbol, str) and symbol.startswith("e_"):
            stackSymbol = stack.pop()
            stack.pop()

            if currentEnvironment != 0:
                for element in reversed(stack):
                    if isinstance(element, str) and element.startswith("e_"):
                        currentEnvironment = int(element[2:])
                        break
            stack.push(stackSymbol)

        # Rule 6: Binary operators
        elif symbol in binaryOperators:
            rightOperand = stack.pop()
            leftOperand = stack.pop()

            if symbol == "+":
                stack.push(leftOperand + rightOperand)
            elif symbol == "-":
                stack.push(leftOperand - rightOperand)
            elif symbol == "*":
                stack.push(leftOperand * rightOperand)
            elif symbol == "/":
                stack.push(leftOperand // rightOperand)
            elif symbol == "**":
                stack.push(leftOperand ** rightOperand)
            elif symbol == "gr":
                stack.push(leftOperand > rightOperand)
            elif symbol == "ge":
                stack.push(leftOperand >= rightOperand)
            elif symbol == "ls":
                stack.push(leftOperand < rightOperand)
            elif symbol == "le":
                stack.push(leftOperand <= rightOperand)
            elif symbol == "eq":
                stack.push(leftOperand == rightOperand)
            elif symbol == "ne":
                stack.push(leftOperand != rightOperand)
            elif symbol == "or":
                stack.push(leftOperand or rightOperand)
            elif symbol == "&":
                stack.push(leftOperand and rightOperand)
            elif symbol == "aug":
                if isinstance(rightOperand, tuple):
                    stack.push(leftOperand + rightOperand)
                else:
                    stack.push((leftOperand, rightOperand))

        # Rule 7: Unary operators
        elif symbol in unaryOperators:
            operand = stack.pop()
            if symbol == "neg":
                stack.push(-operand)
            elif symbol == "not":
                stack.push(not operand)

        # Rule 8: Delta reduction for conditionals
        elif isinstance(symbol, Delta):
            condition = stack.pop()
            if condition is True:
                control += controlStructures[symbol.number - 1]
            else:
                control += controlStructures[symbol.number]

        # Rule 9: Tau (tuple) constructor
        elif isinstance(symbol, Tau):
            elements = []
            for _ in range(symbol.number):
                elements.insert(0, stack.pop())
            stack.push(tuple(elements))

        # Rule 10: Eta reduction
        elif isinstance(symbol, Eta):
            tempLambda = Lambda(symbol.number)
            tempLambda.bounded_variable = symbol.bounded_variable
            tempLambda.environment = symbol.environment

            control.append("gamma")
            control.append("gamma")
            stack.push(symbol)
            stack.push(symbol)
            stack.push(tempLambda)

        # Rule 11: Beta reduction
        elif symbol == "beta":
            stack.pop()

        else:
            print("Error: Invalid symbol encountered.")
            exit(1)

    return printPresent, stack.pop()
