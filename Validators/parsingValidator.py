from src.parser import *

prog_file = input()

tree = parse(prog_file)
printAST(tree)
