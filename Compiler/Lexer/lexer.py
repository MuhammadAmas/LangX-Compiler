import re
from Token import Token

def intConst(word):
    pattern = "(^[+|-]?[0-9]+$)"
    matchPattern = re.match(pattern, word)

    if matchPattern:
        return True
    else:
        return False


def floatConst(word):
    pattern = "(^[+|-]?[0-9]*[.][0-9]+$)"
    matchPattern = re.match(pattern, word)

    if matchPattern:
        return True
    else:
        return False

def charConst(word):
    pattern = "(\'[\\sA-Za-z0-9-!@$#%^&*()+=;:<>,.?/{}[\]|]\')"
    matchPattern = re.match(pattern, word)

    if matchPattern:
        return True
    else:
        return False
    
def stringConst(word):
    pattern = "(\"(.*)\")"
    matchPattern = re.match(pattern, word)

    if matchPattern:
        return True
    else:
        return False


def isIdentifier(word):
    pattern = "([a-zA-Z_][a-zA-Z0-9_]*)"
    matchPattern = re.match(pattern, word)

    if matchPattern:
        return True
    else:
        return False


def generateToken(word, line, i):
    currentToken = Token(word, line)
    # showToken = str(line) +"\t" + word
    # print(showToken)
    i = i+1
    return "", i, currentToken