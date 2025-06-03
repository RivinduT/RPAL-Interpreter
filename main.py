import sys
from src.parser import parse
from src.node import preOrderTraversal
from src.ASTtoST import *
from src.cseMachine import *

if __name__ == "__main__":
    arguments = sys.argv
    
    if len(arguments) < 2:
        print("Incorrect usage. Please run the command as follows:\n python ./myrpal.py [-l] [-ast] [-st] filename")
        sys.exit(1)
        
    else:
        if len(arguments) == 2:
            file_name = arguments[1]
            getResult(file_name)
            
        else:
            switches = arguments[1 : -1]
            file_name = arguments[-1]
            
            if "-l" in switches or "-ast" in switches or "-st" in switches:

                # When '-l' is specified, output the raw contents of the file.
                if "-l" in switches:
                    with open(file_name, "r") as file:
                        print(file.read())
                        
                    print()
                    
                # When '-ast' is present, generate and display the abstract syntax tree (AST).
                if "-ast" in switches:
                    ast = parse(file_name)
                    preorder_traversal(ast)
                    
                    print()
                    
                    # If '-st' is also included, produce and show the standardized tree.
                    if "-st" in switches:
                        st = make_standardized_tree(ast)
                        preorder_traversal(st)
                        
                        print() 
                        exit()
                
                # If only '-st' is specified, create and print the standardized tree.
                elif "-st" in switches:
                    st = standardize(file_name)  
                    preorder_traversal(st)
                    
                    print()
                    exit()
            
            else:
                print("Incorrect usage. Please run the command as follows:\n python ./myrpal.py [-l] [-ast] [-st] filename")
                sys.exit(1)