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
count = 0
control = []
stack = Stack("CSE")                        # Stack for the CSE machine
environments = [Environment(0, None)]
currentEnvironment = 0
builtInFunctions = ["Order", "Print", "print", "Conc", "Stern", "Stem", "Isinteger", "Istruthvalue", "Isstring", "Istuple", "Isfunction", "ItoS"]
printPresent = False


def generateControlStructure(root, i):
    global count
    
    while(len(controlStructures) <= i):
        controlStructures.append([])

    # When lambda is encountered, we have to generate a new control structure.
    if (root.value == "lambda"):
        count += 1
        leftChild = root.children[0]
        if (leftChild.value == ","):
            temp = Lambda(count)
            
            x = ""
            for child in leftChild.children:
                x += child.value[4:-1] + ","
            x = x[:-1]
            
            temp.boundedVariable = x
            controlStructures[i].append(temp)
        else:
            temp = Lambda(count)
            temp.boundedVariable = leftChild.value[4:-1]
            controlStructures[i].append(temp)

        for child in root.children[1:]:
            generateControlStructure(child, count)

    elif (root.value == "->"):
        count += 1
        temp = Delta(count)
        controlStructures[i].append(temp)
        generateControlStructure(root.children[1], count)
        count += 1
        temp = Delta(count)
        controlStructures[i].append(temp)
        generateControlStructure(root.children[2], count)
        controlStructures[i].append("beta")
        generateControlStructure(root.children[0], i)

    elif (root.value == "tau"):
        n = len(root.children)
        temp = Tau(n)
        controlStructures[i].append(temp)
        for child in root.children:
            generateControlStructure(child, i)

    else:
        controlStructures[i].append(root.value)
        for child in root.children:
            generateControlStructure(child, i)

def lookup(name):
    name = name[1:-1]
    info = name.split(":")
    
    if (len(info) == 1):
        value = info[0]
    else:
        dataType = info[0]
        value = info[1]
    
        if dataType == "INT":
            return int(value)
        elif dataType == "STR":
            return value.strip("'")
        elif dataType == "ID":
            if (value in builtInFunctions):
                return value
            else:
                try:
                    value = environments[currentEnvironment].variables[value]
                except KeyError:
                    print("Undeclared Identifier: " + value)
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
    
def builtIn(function, argument):
    global printPresent
    
    if (function == "Order"):
        order = len(argument)
        stack.push(order)

    elif (function == "Print" or function == "print"):
        printPresent = True
        
        if type(argument) == str:
            if "\\n" in argument:
                argument = argument.replace("\\n", "\n")
            if "\\t" in argument:
                argument = argument.replace("\\t", "\t")

        stack.push(argument)

    elif (function == "Conc"):
        stackSymbol = stack.pop()
        control.pop()
        temp = argument + stackSymbol
        stack.push(temp)

    elif (function == "Stern"):
        stack.push(argument[1:])

    elif (function == "Stem"):
        stack.push(argument[0])

    elif (function == "Isinteger"):
        if (type(argument) == int):
            stack.push(True)
        else:
            stack.push(False)

    elif (function == "Istruthvalue"):
        if (type(argument) == bool):
            stack.push(True)
        else:
            stack.push(False)

    elif (function == "Isstring"):
        if (type(argument) == str):
            stack.push(True)
        else:
            stack.push(False)

    elif (function == "Istuple"):
        if (type(argument) == tuple):
            stack.push(True)
        else:
            stack.push(False)

    elif (function == "Isfunction"):
        if (argument in builtInFunctions):
            return True
        else:
            False
    
    elif (function == "ItoS"):
        if (type(argument) == int):
            stack.push(str(argument))
        else:
            print("Error: ItoS function can only accept integers.")
            exit()

def applyRules():
    op = ["+", "-", "*", "/", "**", "gr", "ge", "ls", "le", "eq", "ne", "or", "&", "aug"]
    uop = ["neg", "not"]

    global control
    global currentEnvironment

    while(len(control) > 0):
        symbol = control.pop()

        if type(symbol) == str and (symbol[0] == "<" and symbol[-1] == ">"):
            stack.push(lookup(symbol))

        elif type(symbol) == Lambda:
            temp = Lambda(symbol.number)
            temp.boundedVariable = symbol.boundedVariable
            temp.environment = currentEnvironment
            stack.push(temp)

        elif (symbol == "gamma"):
            stackSymbol1 = stack.pop()
            stackSymbol2 = stack.pop()

            if (type(stackSymbol1) == Lambda):
                currentEnvironment = len(environments)
                
                lambdaNumber = stackSymbol1.number
                boundedVariable = stackSymbol1.boundedVariable
                parentEnvironmentNumber = stackSymbol1.environment

                parent = environments[parentEnvironmentNumber]
                child = Environment(currentEnvironment, parent)
                parent.addChild(child)
                environments.append(child)

                variableList = boundedVariable.split(",")
                
                if (len(variableList) > 1):
                    for i in range(len(variableList)):
                        child.addVariable(variableList[i], stackSymbol2[i])
                else:
                    child.addVariable(boundedVariable, stackSymbol2)

                stack.push(child.name)
                control.append(child.name)
                control += controlStructures[lambdaNumber]

            elif (type(stackSymbol1) == tuple):
                stack.push(stackSymbol1[stackSymbol2 - 1])

            elif (stackSymbol1 == "Y*"):
                temp = Eta(stackSymbol2.number)
                temp.boundedVariable = stackSymbol2.boundedVariable
                temp.environment = stackSymbol2.environment
                stack.push(temp)

            elif (type(stackSymbol1) == Eta):
                temp = Lambda(stackSymbol1.number)
                temp.boundedVariable = stackSymbol1.boundedVariable
                temp.environment = stackSymbol1.environment
                
                control.append("gamma")
                control.append("gamma")
                stack.push(stackSymbol2)
                stack.push(stackSymbol1)
                stack.push(temp)

            elif stackSymbol1 in builtInFunctions:
                builtIn(stackSymbol1, stackSymbol2)
              
        elif type(symbol) == str and (symbol[0:2] == "e_"):
            stackSymbol = stack.pop()
            stack.pop()
            
            if (currentEnvironment != 0):
                for element in reversed(stack):
                    if (type(element) == str and element[0:2] == "e_"):
                        currentEnvironment = int(element[2:])
                        break
            stack.push(stackSymbol)

        elif (symbol in op):
            rand1 = stack.pop()
            rand2 = stack.pop()
            if (symbol == "+"): 
                stack.push(rand1 + rand2)
            elif (symbol == "-"):
                stack.push(rand1 - rand2)
            elif (symbol == "*"):
                stack.push(rand1 * rand2)
            elif (symbol == "/"):
                stack.push(rand1 // rand2)
            elif (symbol == "**"):
                stack.push(rand1 ** rand2)
            elif (symbol == "gr"):
                stack.push(rand1 > rand2)
            elif (symbol == "ge"):
                stack.push(rand1 >= rand2)
            elif (symbol == "ls"):
                stack.push(rand1 < rand2)
            elif (symbol == "le"):
                stack.push(rand1 <= rand2)
            elif (symbol == "eq"):
                stack.push(rand1 == rand2)
            elif (symbol == "ne"):
                stack.push(rand1 != rand2)
            elif (symbol == "or"):
                stack.push(rand1 or rand2)
            elif (symbol == "&"):
                stack.push(rand1 and rand2)
            elif (symbol == "aug"):
                if (type(rand2) == tuple):
                    stack.push(rand1 + rand2)
                else:
                    stack.push(rand1 + (rand2,))

        elif (symbol in uop):
            rand = stack.pop()
            if (symbol == "not"):
                stack.push(not rand)
            elif (symbol == "neg"):
                stack.push(-rand)

        elif (symbol == "beta"):
            B = stack.pop()
            elsePart = control.pop()
            thenPart = control.pop()
            if (B):
                control += controlStructures[thenPart.number]
            else:
                control += controlStructures[elsePart.number]

        elif type(symbol) == Tau:
            n = symbol.number
            tauList = []
            for i in range(n):
                tauList.append(stack.pop())
            tauTuple = tuple(tauList)
            stack.push(tauTuple)

        elif (symbol == "Y*"):
            stack.push(symbol)

    if type(stack[0]) == Lambda:
        stack[0] = "[lambda closure: " + str(stack[0].boundedVariable) + ": " + str(stack[0].number) + "]"
         
    if type(stack[0]) == tuple:          
        for i in range(len(stack[0])):
            if type(stack[0][i]) == bool:
                stack[0] = list(stack[0])
                stack[0][i] = str(stack[0][i]).lower()
                stack[0] = tuple(stack[0])
                
        if len(stack[0]) == 1:
            stack[0] = "(" + str(stack[0][0]) + ")"
        else: 
            if any(type(element) == str for element in stack[0]):
                temp = "("
                for element in stack[0]:
                    temp += str(element) + ", "
                temp = temp[:-2] + ")"
                stack[0] = temp
                
    if stack[0] == True or stack[0] == False:
        stack[0] = str(stack[0]).lower()

def getResult(fileName):
    global control

    st = standardize(fileName)
    
    generateControlStructure(st,0) 
    
    control.append(environments[0].name)
    control += controlStructures[0]

    stack.push(environments[0].name)

    applyRules()

    if printPresent:
        print(stack[0])