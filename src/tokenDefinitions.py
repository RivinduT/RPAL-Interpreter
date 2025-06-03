"""
Defines the Token class used to represent lexical tokens in the RPAL interpreter.
Each token stores its content, type, line number, and flags for parsing purposes.
"""

class Token:
    def __init__(self, content, tokenType, lineNumber):
        self.content = content
        self.tokenType = tokenType
        self.lineNumber = lineNumber
        self.isFirstToken = False
        self.isLastToken = False
        
     
    # Returns a readable string representation of the token for debugging purposes if required.
    def __str__(self):
        return f"{self.content} : {self.tokenType}"
    
    # Marks this token's type as a keyword.
    # Very important for the lexical screener.    
    def markAsKeyword(self):
        self.tokenType = "<KEYWORD>"

    # Marks this token as the first token in a sequence.
    def markAsFirst(self):
        self.isFirstToken = True

    # Marks this token as the last token in a sequence.
    # Useful for parsing boundary detection.    
    def markAsLast(self):
        self.isLastToken = True


