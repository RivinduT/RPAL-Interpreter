from src.screener import filterTokens
from src.stack import Stack
from src.node import *

# A stack containing nodes
stack = Stack("AST")

# This function is used to build the abstract syntax tree.
def buildAST(value, num_children):
    node = Node(value)
    node.children = [None] * num_children
    
    for i in range (0, num_children):
        if stack.is_empty():
            print("Stack is empty")
            exit(1)
        node.children[num_children - i - 1] = stack.pop()
        
    stack.push(node)
 
# This function is used to print the abstract syntax tree in preorder traversal.    
def printAST(root):
    preOrderTraversal(root)
 
# This function is used to read the expected token. 
def read(expected_token):
    if tokens[0].content != expected_token:
        print("Syntax error in line " + str(tokens[0].lineNumber) + ": Expected " + str(expected_token) + " but got " + str(tokens[0].content))
        exit(1)
     
    if not tokens[0].isLastToken:
        del tokens[0]   
        
    else:
        if tokens[0].tokenType != ")":
            tokens[0].tokenType = ")"    
            

def parse(file_name):
    global tokens
    tokens, invalid_flag, invalid_token = filterTokens(file_name)
    
    # If there are invalid tokens, we cannot proceed with the parsing.
    if invalid_flag:
        print("Invalid token present in line " + str(invalid_token.lineNumber) + ": " + str(invalid_token.content))
        exit(1)
    
    procedureE()
    
    if not stack.is_empty():
        root = stack.pop()
    else:
        print("Stack is empty")
        exit(1)
        
    return root
 
############################################################## 
def procedureE():      
    # E -> 'let' D 'in' E 
    if tokens[0].content == "let":
        read("let")
        procedureD()
        
        if tokens[0].content == "in":
            read("in")
            procedureE()
            buildAST("let", 2)
        else:
            print("Syntax error in line " + str(tokens[0].lineNumber) + ": 'in' expected")
            exit(1)
    
    # E -> 'fn'  Vb+ '.' E    
    elif tokens[0].content == "fn":
        read("fn")
        n = 0

        while tokens[0].tokenType == "<IDENTIFIER>" or tokens[0].tokenType == "(":  
            procedureVb()
            n += 1
            
        if n == 0:
            print("Syntax error in line " + str(tokens[0].lineNumber) + ": Identifier or '(' expected")
            exit(1)
            
        if tokens[0].content == ".":
            read(".")
            procedureE()
            buildAST("lambda", n + 1)
        else:
            print("Syntax error in line " + str(tokens[0].lineNumber) + ": '.' expected")
            exit(1)
             
    # E  ->  Ew    
    else:
        procedureEw()

##############################################################
def procedureEw():
    # Ew -> T
    procedureT()

    # Ew -> T 'where' Dr
    if tokens[0].content == "where":
        read("where")
        procedureDr()
        buildAST("where", 2)  
        
##############################################################
def procedureT():     
    # T -> Ta
    procedureTa()
    
    # T -> Ta (','  Ta)+
    n = 0
    while tokens[0].content == ",":
        read(",")
        procedureTa()
        n += 1
        
    if n > 0:
        buildAST("tau", n+1)
        
##############################################################      
def procedureTa():  
    # Ta -> Tc
    procedureTc()
    
    # Ta -> Ta 'aug' Tc 
    while tokens[0].content == "aug":
        read("aug")
        procedureTc()
        buildAST("aug", 2)  
        
##############################################################
def procedureTc():   
    # Tc -> B
    procedureB()
    
    # Tc -> B '->' Tc '|' Tc
    if tokens[0].content == "->":  
        read("->")
        procedureTc()
        
        if tokens[0].content == "|":
            read("|")
            procedureTc()
            buildAST("->", 3)
        else:
            print("Syntax error in line " + str(tokens[0].lineNumber) + ": '|' expected")
            exit(1)
            
##############################################################
def procedureB():
    # B -> Bt
    procedureBt()
    
    # B -> B 'or' Bt
    while tokens[0].content == "or":
        read("or")
        procedureBt()
        buildAST("or", 2) 

##############################################################
def procedureBt():    
    # Bt -> Bs
    procedureBs()
    
    # Bt -> Bt '&' Bs
    while tokens[0].content == "&":
        read("&")
        procedureBs()
        buildAST("&", 2)
        
##############################################################
def procedureBs():
    # Bs -> 'not' Bp
    if tokens[0].content == "not":
        read("not")
        procedureBp()
        buildAST("not", 1)
        
    # Bs -> Bp
    else:
        procedureBp()
        
##############################################################
def procedureBp():           
    # Bp -> A
    procedureA()
    
    # Bp -> A ('gr' | '>' ) A
    if tokens[0].content == "gr" or tokens[0].content == ">":
        read(tokens[0].content)
        procedureA()
        buildAST("gr", 2)
        
    # Bp -> A ('ge' | '>=' ) A
    elif tokens[0].content == "ge" or tokens[0].content == ">=":
        read(tokens[0].content)
        procedureA()
        buildAST("ge", 2)
        
    # Bp -> A ('ls' | '<' ) A
    elif tokens[0].content == "ls" or tokens[0].content == "<":
        read(tokens[0].content)
        procedureA()
        buildAST("ls", 2)
        
    # Bp -> A ('le' | '<=' ) A
    elif tokens[0].content == "le" or tokens[0].content == "<=":
        read(tokens[0].content)
        procedureA()
        buildAST("le", 2)
        
    # Bp -> A 'eq' A
    elif tokens[0].content == "eq":
        read("eq")
        procedureA()
        buildAST("eq", 2)
        
    # Bp -> A 'ne' A
    elif tokens[0].content == "ne":
        read("ne")
        procedureA()
        buildAST("ne", 2)

##############################################################
def procedureA():
    # A -> '+' At
    if tokens[0].content=="+":
        read("+")
        procedureAt()
        
    # A -> '-' At
    elif tokens[0].content=="-":
        read("-")
        procedureAt()
        buildAST("neg", 1)
        
    # A -> At
    else:
        procedureAt()
        
    while tokens[0].content in ["+", "-"]:
        # A -> A '+' At
        if tokens[0].content=="+":
            read("+")
            procedureAt()
            buildAST("+", 2)
            
        # A -> A '-' At
        else:
            read("-")
            procedureAt()
            buildAST("-", 2)
    
##############################################################
def procedureAt():
    # At -> Af
    procedureAf()
    
    while tokens[0].content in ["*", "/"]:
        # At -> At '*' Af
        if tokens[0].content=="*":
            read("*")
            procedureAf()
            buildAST("*", 2)
            
        # At -> At '/' Af
        else:
            read("/")
            procedureAf()
            buildAST("/", 2)

##############################################################
def procedureAf():    
    # Af -> Ap 
    procedureAp()
    
    # Af -> Ap '**' Af
    if tokens[0].content == "**":     
        read("**")
        procedureAf()
        buildAST("**", 2)
 
##############################################################    
def procedureAp():
    # Ap -> R
    procedureR()
    
    # Ap -> Ap '@' <IDENTIFIER> R
    while tokens[0].content == "@":
        read("@")
        
        if tokens[0].tokenType == "<IDENTIFIER>":
            buildAST("<ID:" + tokens[0].content + ">", 0)
            read(tokens[0].content)
            procedureR()
            buildAST("@", 3)            
        else:
            print("Syntax error in line " + str(tokens[0].lineNumber) + ": Identifier expected")
            exit(1)
    
##############################################################
def procedureR():
    # R -> Rn
    procedureRn()
    
    # R -> R Rn
    while  tokens[0].tokenType in ["<IDENTIFIER>", "<INTEGER>", "<STRING>"] or tokens[0].content in ["true", "false","nil", "(", "dummy"]: 
        procedureRn()
        buildAST("gamma", 2)

##############################################################
def procedureRn():   
    value = tokens[0].content
    
    # Rn -> <IDENTIFIER>
    if tokens[0].tokenType == "<IDENTIFIER>":
        read(value)
        buildAST("<ID:" + value + ">", 0)
    
    # Rn -> <INTEGER>    
    elif tokens[0].tokenType == "<INTEGER>":
        read(value)
        buildAST("<INT:" + value + ">", 0)
        
    # Rn -> <STRING>    
    elif tokens[0].tokenType == "<STRING>":
        read(value)
        buildAST("<STR:" + value + ">", 0)
        
    # Rn -> 'true'
    #    -> 'false'
    #    -> 'nil'
    #    -> 'dummy'    
    elif value in ["true", "false", "nil", "dummy"]:
        read(value)
        buildAST("<" + value + ">", 0)
      
    # Rn -> '(' E ')'    
    elif value == "(":
        read("(")
        procedureE()
        
        if tokens[0].content == ")":     
            read(")")
        else:
            print("Syntax error in line " + str(tokens[0].lineNumber) + ": ')' expected")
            exit(1)
            
    else:
        print("Syntax error in line " + str(tokens[0].lineNumber) + ": Identifier, Integer, String, 'true', 'false', 'nil', 'dummy' or '(' expected")
        exit(1)

##############################################################
def procedureD():
    # D -> Da
    procedureDa()
    
    # D -> Da 'within' D
    if tokens[0].content == "within":
        read("within")
        procedureD()
        buildAST("within", 2)
    
##############################################################
def procedureDa():
    # Da -> Dr
    procedureDr()
    
    # Da -> Dr ('and' Dr)+
    n = 0
    while tokens[0].content == "and":
        read("and")
        procedureDr()
        n += 1
        
    if n > 0:  
        buildAST("and", n + 1)
    
##############################################################
def procedureDr():
    # Dr -> 'rec' Db
    if tokens[0].content == "rec":
        read("rec")
        procedureDb()
        buildAST("rec", 1)
        
    # Dr -> Db
    else:
        procedureDb()
    
##############################################################
def procedureDb():    
    value = tokens[0].content
    
    # Db -> '(' D ')'
    if value == "(":
        read("(")
        procedureD()
        
        if tokens[0].content == ")":
            read(")")
        else:
            print("Syntax error in line " + str(tokens[0].lineNumber) + ": ')' expected")
            exit(1)

    elif tokens[0].tokenType == "<IDENTIFIER>":
        read(value)
        buildAST("<ID:" + value + ">", 0)  

        # Db -> <IDENTIFIER> Vb+ '=' E
        if tokens[0].content in [",", "="]:  
            procedureVl()
            read("=")
            procedureE()
            buildAST("=", 2)
        
        # Db -> Vl '=' E
        else: 
            n = 0
        
            while tokens[0].tokenType == "<IDENTIFIER>" or tokens[0].tokenType == "(":
                procedureVb()
                n += 1
                
            if n == 0:
                print("Syntax error in line " + str(tokens[0].lineNumber) + ": Identifier or '(' expected")
                exit(1)    
                
            if tokens[0].content == "=":
                read("=")
                procedureE()
                buildAST("function_form", n + 2)
            else:
                print("Syntax error in line " + str(tokens[0].lineNumber) + ": '=' expected")
                exit(1)

##############################################################
def procedureVb(): 
    # Vb -> <IDENTIFIER>
    #    -> '(' Vl ')'
    #    -> '(' ')' 
    
    value_1 = tokens[0].content 

    # Vb -> <IDENTIFIER>
    if tokens[0].tokenType == "<IDENTIFIER>":
        read(value_1)
        buildAST("<ID:" + value_1 + ">", 0)     
        
    elif value_1 == "(":
        read("(")
        
        value_2 = tokens[0].content 
        
        # Vb -> '(' ')'
        if value_2 == ")":
            read(")")
            buildAST("()", 0)
        
        # Vb -> '(' Vl ')'
        elif tokens[0].tokenType == "<IDENTIFIER>": 
            read(value_2)
            buildAST("<ID:" + value_2 + ">", 0)    
            procedureVl()
            
            if tokens[0].content == ")":
                read(")")
            else:
                print("Syntax error in line " + str(tokens[0].lineNumber) + ": ')' expected")
                exit(1)
        else:
            print("Syntax error in line " + str(tokens[0].lineNumber) + ": Identifier or ')' expected")
            exit(1)
    else:
        print("Syntax error in line " + str(tokens[0].lineNumber) + ": Identifier or '(' expected")
        exit(1)
    
##############################################################
def procedureVl():
    # Vl -> <IDENTIFIER> (',' <IDENTIFIER>)*   
    n = 0
    
    while tokens[0].content == ",":
        read(",")
        
        if tokens[0].tokenType == "<IDENTIFIER>":
            value = tokens[0].content
            read(value)
            buildAST("<ID:" + value + ">", 0)    
            n += 1
        else:
            print("Syntax error in line " + str(tokens[0].lineNumber) + ": Identifier expected")
            
    if n > 0:
        buildAST(",", n + 1) 