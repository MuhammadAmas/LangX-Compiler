from lexer import *

def classifyToken(tokenList):
    keywords = {"void": "VOID","num": "DT", "dec": "DT", "bool": "DT", "string": "DT", "array":"ARRAY", "dict":"DICT", 
                "when": "WHEN", "otherwise": "OTHERWISE", "check": "CHECK","iterate": "LOOP", "stop": "CONTROL FLOW", 
                "continue": "CONTROL FLOW", "define": "DEFINE", "yield": "YIELD","show": "PRINT", "take": "INPUT", 
                "attempt": "ATTEMPT", "catch": "CATCH", "finally":"FINALLY", "group": "GROUP", "error": "ERROR",
                "obj": "SELF", "create": "INIT", "base": "SUPER", "true": "BOOL", "false": "BOOL", "~": "EOF", 
                "calling": "CALL_FUNC", "sealed": "SEALED", "construct":"CONSTRUCTOR", "method":"METHOD",
                "extends" : "EXTENDS", "implements:" : "IMPLEMENTS"}

    operators = {"=": "ASSIGN", "+=": "COMBO_ASSIGN", "-=": "COMBO_ASSIGN", "++": "INC_DEC", "--": "INC_DEC", "<": "RELATION", ">": "RELATION",
                 "==": "RELATION", "<=": "RELATION", ">=": "RELATION", "!=": "RELATION", "and": "AND", "or": "OR", "not": "NOT",
                 "+": "PM", "-": "PM", "*": "M_D_M", "/": "M_D_M", "%": "M_D_M", "**": "POWER", "in": "SOMETHING"}

    punctuators = {"(": "O_PARAM", ")": "C_PARAM", "[": "O_BRACK", "]": "C_BRACK", "{": "O_BRACE", "}": "C_BRACE", ":": "COLON",
                   ",": "SEPARATOR", ";": "TERMINATOR", ".": "DOT"}

    for i in range(len(tokenList)):

        if (tokenList[i].value in keywords.keys()):
            tokenList[i].type = keywords[tokenList[i].value]
            continue

        if (tokenList[i].value in operators.keys()):
            tokenList[i].type = operators[tokenList[i].value]
            continue

        if (tokenList[i].value in punctuators.keys()):
            tokenList[i].type = punctuators[tokenList[i].value]
            continue

        if (intConst(tokenList[i].value)):
            tokenList[i].type = "INT"
            continue

        if (floatConst(tokenList[i].value)):
            tokenList[i].type = "FLT"
            continue

        if (charConst(tokenList[i].value)):
            tokenList[i].type = "CHAR"
            tokenList[i].value = tokenList[i].value[1:-1]
            continue

        if (stringConst(tokenList[i].value)):
            tokenList[i].type = "STR"
            tokenList[i].value = tokenList[i].value[1:-1]
            continue

        if (isIdentifier(tokenList[i].value)):
            tokenList[i].type = "ID"
            continue

        tokenList[i].type = "INVALID"

    return tokenList
