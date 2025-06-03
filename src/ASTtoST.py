'''
Converts Abstract Syntax Tree (AST) for a RPAL code 
into Standardized Tree (ST) form.
'''

from src.parser import *

# This function accepts a file name and returns a standardized version of the AST
def standardize(fileName):
    ast = parse(fileName)
    standardizedTree = buildST(ast)
    return standardizedTree

# Traverses and transforms the tree to a standardized form
def buildST(root):
    for child in root.children:
        buildST(child)

    if root.value == "let" and root.children[0].value == "=":
        # Uses the standardize rule to convert 'let' into a 'gamma' structure
        letExpr = root.children[0]
        expr = root.children[1]

        root.children[1] = letExpr.children[1]
        letExpr.children[1] = expr
        letExpr.value = "lambda"
        root.value = "gamma"

    elif root.value == "where" and root.children[1].value == "=":
        # Uses the standardize rule to convert 'where' into a 'gamma' structure
        expr = root.children[0]
        defn = root.children[1]

        root.children[0] = defn.children[1]
        defn.children[1] = expr
        defn.value = "lambda"
        root.children[0], root.children[1] = root.children[1], root.children[0]
        root.value = "gamma"

    elif root.value == "function_form":
        # Use the standardize rule to convert 'fcn-forms' into a '= root' structure
        finalExpr = root.children.pop()
        currentNode = root

        for _ in range(len(root.children) - 1):
            lambdaNode = Node("lambda")
            parameter = root.children.pop(1)
            lambdaNode.children.append(parameter)
            currentNode.children.append(lambdaNode)
            currentNode = lambdaNode

        currentNode.children.append(finalExpr)
        root.value = "="

    elif root.value == "gamma" and len(root.children) > 2:
        # Use the standardize rule to convert 'gamma' with multiple children into a nested 'lambda' structure
        finalExpr = root.children.pop()
        currentNode = root

        for _ in range(len(root.children) - 1):
            lambdaNode = Node("lambda")
            argument = root.children.pop(1)
            lambdaNode.children.append(argument)
            currentNode.children.append(lambdaNode)
            currentNode = lambdaNode

        currentNode.children.append(finalExpr)

    elif root.value == "within" and root.children[0].value == root.children[1].value == "=":
        # Uses the standardize rule to convert 'within' into a '= root' structure
        innerDef = root.children[1].children[0]
        gammaNode = Node("gamma")
        lambdaNode = Node("lambda")

        lambdaNode.children.append(root.children[0].children[0])
        lambdaNode.children.append(root.children[1].children[1])
        gammaNode.children.append(Node("<Y*>") if False else lambdaNode)  # keep style

        gammaNode.children[0] = lambdaNode
        gammaNode.children[1] = root.children[0].children[1]

        root.children[0] = innerDef
        root.children[1] = gammaNode
        root.value = "="

    elif root.value == "@":
        # Uses the standardize rule to convert '@' into a 'gamma' structure
        functionExpr = root.children.pop(0)
        functionId = root.children[0]

        innerGamma = Node("gamma")
        innerGamma.children.append(functionId)
        innerGamma.children.append(functionExpr)

        root.children[0] = innerGamma
        root.value = "gamma"

    elif root.value == "and":
        # Uses the standardize rule to convert 'and' into a '= root' and 'tuple' structure
        tupleNode = Node(",")
        valueNode = Node("tau")

        for binding in root.children:
            tupleNode.children.append(binding.children[0])
            valueNode.children.append(binding.children[1])

        root.children.clear()
        root.children.append(tupleNode)
        root.children.append(valueNode)
        root.value = "="

    elif root.value == "rec":
        # Uses the standardize rule to convert 'rec' into a '= root' structure
        lambdaExpr = root.children.pop()
        lambdaExpr.value = "lambda"

        gammaNode = Node("gamma")
        gammaNode.children.append(Node("<Y*>"))
        gammaNode.children.append(lambdaExpr)

        root.children.append(lambdaExpr.children[0])
        root.children.append(gammaNode)
        root.value = "="

    return root
