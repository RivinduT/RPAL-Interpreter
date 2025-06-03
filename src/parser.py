'''
Parser for the abstract syntax tree (AST) of RPAL.
This parser reads tokens from a file, builds the AST according to the grammar rules,
and provides functions to print the AST and read expected tokens.
'''

from src.screener import filterTokens
from src.stack import Stack
from src.node import *

#Stack containing nodes
stack = Stack("AST")

#Builds the abstract syntax tree.
def buildAST(value, num_children):
    node = Node(value)
    node.children = [None] * num_children
    
    for i in range(num_children):
        if stack.is_empty():
            print("Stack is empty")
            exit(1)
        node.children[num_children - i - 1] = stack.pop()
        
    stack.push(node)
 
#Prints the abstract syntax tree in preorder traversal.    
def printAST(root):
    preOrderTraversal(root)
 
#Reads the expected token. 
def read(expected_token):
    if tokens[0].content != expected_token:
        print("Syntax error in line " + str(tokens[0].lineNumber) + ": Expected " + str(expected_token) + " but got " + str(tokens[0].content))
        exit(1)
     
    if not tokens[0].isLastToken:
        del tokens[0]   
        
    else:
        if tokens[0].tokenType != ")":
            tokens[0].tokenType = ")"


# Parses the input file and builds the abstract syntax tree.
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
        buildAST("apply", 2)
        
##############################################################
def procedureRn():     
    # Rn -> <IDENTIFIER> | <INTEGER> | <STRING> | true | false | nil | dummy
    if tokens[0].tokenType == "<IDENTIFIER>":
        buildAST("<ID:" + tokens[0].content + ">", 0)
        read(tokens[0].content)
    
    elif tokens[0].tokenType == "<INTEGER>":
        buildAST("<INT:" + tokens[0].content + ">", 0)
        read(tokens[0].content)
    
    elif tokens[0].tokenType == "<STRING>":
        buildAST("<STR:" + tokens[0].content + ">", 0)
        read(tokens[0].content)
    
    elif tokens[0].content == "true":
        buildAST("true", 0)
        read("true")
    
    elif tokens[0].content == "false":
        buildAST("false", 0)
        read("false")
        
    elif tokens[0].content == "nil":
        buildAST("nil", 0)
        read("nil")
        
    elif tokens[0].content == "dummy":
        buildAST("dummy", 0)
        read("dummy")
        
    # Rn -> '(' E ')'
    elif tokens[0].content == "(":
        read("(")
        procedureE()
        
        if tokens[0].content == ")":
            read(")")
        else:
            print("Syntax error in line " + str(tokens[0].lineNumber) + ": ')' expected")
            exit(1)
            
    else:
        print("Syntax error in line " + str(tokens[0].lineNumber) + ": Identifier, Integer, String, true, false, nil, dummy or '(' expected")
        exit(1)
        
##############################################################
def procedureD():
    # D -> Db
    procedureDb()
    
    # D -> Db ';' D
    if tokens[0].content == ";":
        read(";")
        procedureD()
        buildAST("Dseq", 2)

##############################################################
def procedureDb():
    # Db -> <IDENTIFIER> '=' E
    if tokens[0].tokenType == "<IDENTIFIER>":
        buildAST("<ID:" + tokens[0].content + ">", 0)
        read(tokens[0].content)
        
        if tokens[0].content == "=":
            read("=")
            procedureE()
            buildAST("=", 2)
        else:
            print("Syntax error in line " + str(tokens[0].lineNumber) + ": '=' expected")
            exit(1)
            
    else:
        print("Syntax error in line " + str(tokens[0].lineNumber) + ": Identifier expected")
        exit(1)

##############################################################
def procedureDr():
    # Dr -> Db
    procedureDb()
    
    # Dr -> Db ',' Dr
    if tokens[0].content == ",":
        read(",")
        procedureDr()
        buildAST("Dseq", 2)
        
##############################################################
def procedureVb():
    # Vb -> <IDENTIFIER>
    if tokens[0].tokenType == "<IDENTIFIER>":
        buildAST("<ID:" + tokens[0].content + ">", 0)
        read(tokens[0].content)
        
    # Vb -> '(' Vb ')'
    elif tokens[0].content == "(":
        read("(")
        procedureVb()
        if tokens[0].content == ")":
            read(")")
        else:
            print("Syntax error in line " + str(tokens[0].lineNumber) + ": ')' expected")
            exit(1)
    else:
        print("Syntax error in line " + str(tokens[0].lineNumber) + ": Identifier or '(' expected")
        exit(1)
