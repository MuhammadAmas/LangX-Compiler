from Token import Token
from semanticFunctions import createScope, destroyScope, insertAttribute, insertFunctionTable, insertMainTable, lookupAttributeTable, lookupFunctionTable, lookupMainTable, scopeStack_, binTypeCompatible, uniTypeCompatible, mainTable_, functionTable_


i = 0
tokenList = []
# syntaxErr = True
error = ""

currentClass = ""
currentFunction = 0
currentScope = 0


def semanticAnalyzer(tokens):
    global i, tokenList
    i = 0
    tokenList = tokens
    result = structure()
    print(report())
    return result


def report():
    global currentClass, currentFunction, currentScope, scopeStack_, errorAt, mainTable_, functionTable_, error
    report = error + "\n"
    report += "\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\n"
    report += "\t\t\t\t\t\t  R\t  E\t  P\t  O\t  R\t  T\n"
    report += "\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\t~~~~~\n\n"
    report += "\nLast Updated Class:\t" + currentClass + "\n"
    report += "Last Function Scope:\t" + str(currentFunction) + "\n"
    report += "Scope @ End:\t\t" + str(currentScope) + "\n\n"
    report += "###########################################################################\n"
    report += "Main Table:\n\n"
    for i in mainTable_:
        report += "Name:\t\t'" + i.name + "'\nType:\t\t'" + i.type + \
            "'\nTypeMod:\t'" + i.typeMod + "'\nParent:\t\t'" + i.parent + "'\n"
        report += "Attributes:\n"
        for j in i.attrTable:
            report += str(vars(j))
            report += "\n"
        report += "-------------------------\n"
    report += "\n"
    report += "###########################################################################\n"
    report += "Function Table:\n\n"
    for i in functionTable_:
        report += str(vars(i))
        report += "\n"
    return report


def syntaxError():
    global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_, errorAt
    return False


def reDeclarationError(name, detail):
    global i, error
    error += "\n\t***  Re-Declaration Error  ***\n\tID:\t\t" + name + "\n\tAs:\t\t" + \
        detail, "\n\tLine #:\t       ", str(tokenList[i].line) + "\n"
    return


def unDeclaredError(name, detail):
    global i, error
    error += "\n\t***  Un-Declared Error  ***\n\tID:\t\t" + name + "\n\tAs:\t\t" + \
        detail + "\n\tLine #:\t       " + str(tokenList[i].line) + "\n"
    return


def binTypeMismatchedError(left, right, op):
    global i, error
    error += "\n\t***  Type Mismatched Error  ***\n\t"+"Cant Apply:\t" + op + " on " + \
        left + " and " + right + \
        "\n\tLine #:\t       " + str(tokenList[i].line) + "\n"
    return


def uniTypeMismatchedError(operand, op):
    global i, error
    error += "\n\t***  Type Mismatched Error  ***\n\t"+"Cant Apply:\t" + op, " on " + \
        operand + "\n\tLine #:\t       " + str(tokenList[i].line) + "\n"
    return


def randomError(note):
    global i, error
    error += "\n\t***  Exception Unhandled  ***\n\t" + note + \
        "\n\tLine #:\t       " + str(tokenList[i].line) + "\n"
    return


def checkConstructor(check):
    length = len(check.attrTable)
    if (length == 0):
        return True
    count = 0
    for i in check.attrTable:
        if (i.name == check.name):
            if (i.params == ""):
                return True
            count += 1
    if (count > 0):
        randomError(
            check.name + " class doesn't contain no parameterized constructor.")
        return False
    return True
