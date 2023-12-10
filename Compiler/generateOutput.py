from Token import Token

def generateOutput(tokens):
    output = "TOKENLIST:\n"
    for i in range(len(tokens)):
        output = output + str(i) + "\t"
        output = output + Token.displayToken(tokens[i]) + "\n"
    return output