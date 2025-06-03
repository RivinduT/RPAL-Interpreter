'''
Converts a raw string of characters into a list of Token objects that represent 
identifiers, integers, keywords, operators, strings, punctuation etc.
'''
from src.tokenDefinitions import Token

def extractTokens(inputChars): 
    numbers = '0123456789'
    alphabetLetters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    underscore = '_'
    operatorSymbols = '+-*<>&.@/:=~|$!#%^_[]{}\"?'
    punctuationMarks = '();,'
    newlineChar = '\n'

    tokenTypes = []
    tokenValues = []
    lineInfo = []

    idx = 0
    currentToken = ''
    currentLine = 1
    
    try:
        while idx < len(inputChars):
            # Process identifiers
            if inputChars[idx] in alphabetLetters:
                currentToken += inputChars[idx]
                idx += 1

                while idx < len(inputChars) and (inputChars[idx] in alphabetLetters or inputChars[idx] in numbers or inputChars[idx] == underscore):
                    currentToken += inputChars[idx]
                    idx += 1

                tokenValues.append(currentToken)
                tokenTypes.append('<IDENTIFIER>')
                lineInfo.append(currentLine)
                currentToken = ''

            # Process numeric constants
            elif inputChars[idx] in numbers:
                currentToken += inputChars[idx]
                idx += 1

                while idx < len(inputChars): 
                    if inputChars[idx] in numbers:
                        currentToken += inputChars[idx]
                        idx += 1
                    elif inputChars[idx] in alphabetLetters:
                        currentToken += inputChars[idx]
                        idx += 1
                    else:
                        break

                tokenValues.append(currentToken)
                lineInfo.append(currentLine)

                try:
                    int(currentToken)
                    tokenTypes.append('<INTEGER>')
                except:
                    tokenTypes.append('<INVALID>')

                currentToken = ''

            # Process comments (starting with // and ending at newline)
            elif inputChars[idx] == '/' and inputChars[idx + 1] == '/':
                currentToken += inputChars[idx] + inputChars[idx + 1]
                idx += 2

                while idx < len(inputChars) and inputChars[idx] != '\n':
                    currentToken += inputChars[idx]
                    idx += 1

                tokenValues.append(currentToken)
                tokenTypes.append('<DELETE>')
                lineInfo.append(currentLine)
                currentToken = ''

            # Process string literals
            elif inputChars[idx] == "'":
                currentToken += inputChars[idx]
                idx += 1

                while idx < len(inputChars):
                    if inputChars[idx] == "\n":
                        currentLine += 1

                    if inputChars[idx] == "'":
                        currentToken += inputChars[idx]
                        idx += 1
                        break
                    else:
                        currentToken += inputChars[idx]
                        idx += 1

                if len(currentToken) == 1 or currentToken[-1] != "'":
                    print("Unterminated string detected.")
                    exit(1)

                tokenValues.append(currentToken)
                tokenTypes.append('<STRING>')
                lineInfo.append(currentLine)
                currentToken = ''

            # Handle punctuation symbols
            elif inputChars[idx] in punctuationMarks:
                currentToken += inputChars[idx]
                tokenValues.append(currentToken)
                tokenTypes.append(currentToken)
                lineInfo.append(currentLine)
                currentToken = ''
                idx += 1

            # Handle spaces and tabs
            elif inputChars[idx] in [' ', '\t']:
                currentToken += inputChars[idx]
                idx += 1

                while idx < len(inputChars) and inputChars[idx] in [' ', '\t']:
                    currentToken += inputChars[idx]
                    idx += 1

                tokenValues.append(currentToken)
                tokenTypes.append('<DELETE>')
                lineInfo.append(currentLine)
                currentToken = ''

            # Handle newline characters
            elif inputChars[idx] == '\n':
                tokenValues.append(newlineChar)
                tokenTypes.append('<DELETE>')
                lineInfo.append(currentLine)
                currentLine += 1
                idx += 1

            # Handle operator tokens
            elif inputChars[idx] in operatorSymbols:
                while idx < len(inputChars) and inputChars[idx] in operatorSymbols:
                    if inputChars[idx] == '/' and inputChars[idx + 1] == '/':
                        tokenValues.append(currentToken)
                        tokenTypes.append('<OPERATOR>')
                        currentToken = ''
                        lineInfo.append(currentLine)
                        break

                    currentToken += inputChars[idx]
                    idx += 1

                tokenValues.append(currentToken)
                tokenTypes.append('<OPERATOR>')
                lineInfo.append(currentLine)
                currentToken = ''

            # Catch unrecognized characters
            else:
                print(f"Unexpected character: {inputChars[idx]} at index {idx}")
                exit(1)

    except IndexError:
        pass

    totalTokens = len(tokenValues)

    for i in range(totalTokens):
        if i == 0:
            tokenValues[i] = Token(tokenValues[i], tokenTypes[i], lineInfo[i])
            tokenValues[i].markAsFirst()
        elif i == totalTokens - 1:
            if tokenValues[i] == '\n':
                tokenValues[i - 1].markAsLast()
                del tokenValues[i]
                del tokenTypes[i]
                del lineInfo[i]
            else:
                tokenValues[i] = Token(tokenValues[i], tokenTypes[i], lineInfo[i])
                tokenValues[i].markAsLast()
        else:
            tokenValues[i] = Token(tokenValues[i], tokenTypes[i], lineInfo[i])

    return tokenValues
