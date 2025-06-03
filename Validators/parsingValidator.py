from src.parser import *

progFile = input()

tree = parse(progFile)
printAST(tree)
