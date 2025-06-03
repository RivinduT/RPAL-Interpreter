from src.screener import filterTokens
file = input()
tokenList, invalidFlag, invalidToken = filterTokens(file)

# Write the filtered tokens to an output file
with open("output.txt", "w") as file:
    for token in tokenList:
        file.write(f"{token.content} {token.type}\n")

# Print the results      
print(f"Invalid token present: {invalidFlag}")
if invalidFlag:
    print(f"Invalid token: {invalidToken}")       