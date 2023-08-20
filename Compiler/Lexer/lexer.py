token = []


class token ():
    def __init__(self, value, line):
        self.type = "undefined"
        self.value = value
        self.line = line

    def displayToken(self):
        showToken = "\t(" + self.type + ", " + self.value + \
            ", " + str(self.line) + ")"
        return showToken


def intConst(word):
    pattern = "(^[+|-]?[0-9]+$)"
    matchPattern = pattern.match(pattern, word)

    if matchPattern:
        return True
    else:
        return False


def floatConst(word):
    pattern = "(^[+|-]?[0-9]*[.][0-9]+$)"
    matchPattern = pattern.match(pattern, word)

    if matchPattern:
        return True
    else:
        return False


def stringConst(word):
    pattern = "(\"(.*)\")"
    matchPattern = pattern.match(pattern, word)

    if matchPattern:
        return True
    else:
        return False


def isIdentifier(word):
    pattern = "([a-zA-Z_][a-zA-Z0-9_]*)"
    matchPattern = pattern.match(pattern, word)

    if matchPattern:
        return True
    else:
        return False


def generateToken(word, line, i):
    currentToken = token(word, line)
    # showToken = str(line) +"\t" + word
    # print(showToken)
    i = i+1
    return "", i, currentToken


def classifyToken(tokenlist):
    keywords = {"num": "DT", "dec": "DT", "bool": "DT", "string": "DT", "when": "WHEN", "otherwise": "OTHERWISE", "check": "CHECK",
                "iterate": "LOOP", "stop": "CONTROL FLOW", "continue": "CONTROL FLOW", "define": "FUNCTION", "yield": "RETURN",
                "show": "PRINT", "take": "INPUT", "use": "IMPORT", "rename": "RENAME", "attempt": "TRY", "catch": "CATCH", "group": "GROUP",
                "obj": "SELF", "create": "INIT", "base": "SUPER", "true": "BOOL", "false": "BOOL"}

    operators = {"=": "ASSIGN", "+=": "COMBO_ASSIGN", "-=": "COMBO_ASSIGN", "++": "INC_DEC", "--": "INC_DEC", "<": "RELATION", ">": "RELATION",
                 "==": "RELATION", "<=": "RELATION", ">=": "RELATION", "!=": "RELATION", "and": "LOGICAL", "or": "LOGICAL", "not": "LOGICAL",
                 "+": "ARITHMETIC", "-": "ARITHMETIC", "*": "ARITHMETIC", "/": "ARITHMETIC", "%": "ARITHMETIC", "**": "POWER", "in": "SOMETHING"}

    punctuators = {"(": "O_PARAM", ")": "C_PARAM", "[": "O_BRACK", "]": "C_BRACK", "{": "O_BRACE", "}": "C_BRACE", ":": "COLON",
                   "//": "SINGLE_COMMENT", ",": "SEPARATOR"}

# def generateOutput(tokens):
