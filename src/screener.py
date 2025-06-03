'''
This module filters and processes the raw tokens generated from the source file.
It tags RPAL keywords, removes unnecessary tokens, and identifies invalid ones.
'''

from src.lexicalAnalyzer import extractTokens

def filterTokens(fileName):
    # Reserved keywords in RPAL
    rpalKeywords = {
        "let", "in", "where", "rec", "fn",
        "aug", "or", "not", "gr", "ge", "ls", "le", "eq", "ne",
        "true", "false", "nil", "dummy", "within", "and"
    }

    characterStream = []
    tokenStream = []
    hasInvalidToken = False
    firstInvalidToken = None

    try:
        with open(fileName, 'r') as sourceFile:
            for line in sourceFile:
                characterStream.extend(line)
            tokenStream = extractTokens(characterStream)

    except FileNotFoundError:
        print("Error: File not found.")
        exit(1)
    except Exception as error:
        print("An unexpected error occurred:", error)
        exit(1)

    # Reverse traversal for safe removal and tagging
    for i in range(len(tokenStream) - 1, -1, -1):
        token = tokenStream[i]

        # Tag keywords
        if token.type == "<IDENTIFIER>" and token.content in rpalKeywords:
            token.make_keyword()

        # Remove whitespace, comments, and line breaks
        if token.type == "<DELETE>" or token.content == "\n":
            tokenStream.pop(i)

        # Flag first encountered invalid token
        if token.type == "<INVALID>" and not hasInvalidToken:
            hasInvalidToken = True
            firstInvalidToken = token

    # Ensure last token is marked properly
    if tokenStream:
        tokenStream[-1].is_last_token = True

    return tokenStream, hasInvalidToken, firstInvalidToken
