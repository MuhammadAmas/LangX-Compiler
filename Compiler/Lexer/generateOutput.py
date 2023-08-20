from Token import Token

def generateOutput(tokens):
    output = "TOKENLIST:\n"
    for i in range(len(tokens)):
        if (i == len(tokens)-1):
            output = output + str(i) + "\t"
            output = output + Token.displayToken(tokens[i])
            continue
        output = output + str(i) + "\t"
        output = output + Token.displayToken(tokens[i]) + "\n"
    return output