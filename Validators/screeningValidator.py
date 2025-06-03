from src.screener import filterTokens
file = input()
token_list, invalid_flag, invalid_token = filterTokens(file)

# Write the filtered tokens to an output file
with open("output.txt", "w") as file:
    for token in token_list:
        file.write(f"{token.content} {token.type}\n")

# Print the results      
print(f"Invalid token present: {invalid_flag}")
if invalid_flag:
    print(f"Invalid token: {invalid_token}")       