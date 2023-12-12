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
    analysis_report = report()
    print(analysis_report)
    return analysis_report


def report():
    global currentClass, currentFunction, currentScope, scopeStack_, errorAt, mainTable_, functionTable_, error
    # return
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


def syntaxError(message):
    global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_, errorAt
    return False


def reDeclarationError(name, detail):
    print(name, detail)
    global i, error
    error += "\n\t***  Re-Declaration Error  ***\n\tID:\t\t" + name + \
        "\n\tAs:\t\t" + detail + "\n\tLine #:\t       " + \
        str(tokenList[i].line) + "\n"

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


try:
    def structure():
        global i, tokenList
        if tokenList[i].type == 'EOF':
            return True
        if MST():
            structure()
        elif class_def():
            structure()
        syntaxError("Syntax Error: Invalid start rule")

    # ? ************************* CLASS DEFINITION *************************

    def class_def():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_

        if tokenList[i].type == "SEALED":
            typeMod = tokenList[i].type
            i += 1
            if tokenList[i].type == "GROUP":
                entryOf = tokenList[i].type
                i += 1
                if tokenList[i].type == "ID":
                    name = tokenList[i].value
                    i += 1
                    check = insertMainTable(
                        name, entryOf, typeMod, 'ownParent')
                    if (check == False):
                        reDeclarationError(name, "Class")
                        return False
                        currentClass = name
                    if tokenList[i].type == "O_BRACE":
                        currentScope = createScope()
                        i += 1
                        class_body()
                        if tokenList[i].type == "C_BRACE":
                            currentScope = destroyScope()
                            i += 1
                            return True

    # ? ************************* Inheritance *************************
        elif tokenList[i].type == "GROUP":
            entryOf = tokenList[i].type
            i += 1
            if tokenList[i].type == "ID":
                name = tokenList[i].value
                i += 1
                parent, check = inheritance()
                if (check):
                    check = insertMainTable(name, entryOf, 'public', parent)
                    if (check == False):
                        reDeclarationError(name, "Class")
                        return False
                        currentClass = name
                if tokenList[i].type == "O_BRACE":
                    currentScope = createScope()
                    i += 1
                    class_body()
                    if tokenList[i].type == "C_BRACE":
                        currentScope = destroyScope()
                        i += 1
                        return True
        return False

    def inheritance():
        global i, tokenList
        parClass = " "
        if tokenList[i].type == "EXTENDS":
            i += 1
            if tokenList[i].type == "ID":
                id = tokenList[i].value
                check = lookupMainTable(id)
                if (check == False):
                    unDeclaredError(id, "Parent Class")
                    return parClass, False
                if (check.type != "GROUP"):
                    randomError(
                        "Class should be inherited from a class.")
                    return parClass, False
                if (check.typeMod == "SEALED"):
                    randomError("class can't be inherited from " +
                                check.typeMod.lower() + " class.")
                    return parClass, False
                parClass = parClass + id
                i += 1
                return parClass, True
        elif tokenList[i].type == "IMPLEMENTS":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                if inheritance_2():
                    return True
        else:
            return parClass, True  # Epsilon case

    def inheritance_2():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                inheritance_2()
        else:
            return True  # Epsilon case

    def class_body():
        global i, tokenList
        if tokenList[i].type == 'DT':
            dec()
        if tokenList[i].type in ["ID", "#", "CONSTRUCTOR", "METHOD"]:
            if C_ST():
                if C_MT():
                    return True

    # ? ************************* CLASS SINGLE STATEMENT *************************

    def C_ST():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            init()
            if tokenList[i].type == "TERMINATOR":
                i += 1
        elif tokenList[i].type == "METHOD":
            if method():
                return True
        elif tokenList[i].type == "CONSTRUCTOR":
            if constructor():
                return True
        else:
            return False

    # ? ************************* CLASS METHOD *************************

    def method():
        global i, tokenList
        if method_header():
            i += 1
            if tokenList[i].type == "O_BRACE":
                i += 1
                MST()
                if tokenList[i].type == "C_BRACE":
                    i += 1
                    return True

    def method_header():
        global tokenList, i
        if (tokenList[i].type == "METHOD"):
            i += 1
            if (tokenList[i].type == "DT" or tokenList[i].type == "VOID"):
                i += 1
                if tokenList[i].type == "ID":
                    i += 1
                    if tokenList[i].type == "O_PARAM":
                        i += 1
                        params()
                        if tokenList[i].type == "C_PARAM":
                            return True
        return False

    def params():
        global i, tokenList
        if tokenList[i].type == "DT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                params2()
        else:
            return True  # Epsilon case

    def params2():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            if tokenList[i].type == "DT":
                i += 1
                if tokenList[i].type == "ID":
                    i += 1
                    params2()
        else:
            return True  # Epsilon case

    # ? ************************* CLASS CONSTRUCTOR *************************

    def constructor():
        global i, tokenList
        if tokenList[i].type == "CONSTRUCTOR":
            i += 1
            if tokenList[i].type == "O_PARAM":
                i += 1
                params()
                if tokenList[i].type == "C_PARAM":
                    i += 1
                    if tokenList[i].type == "O_BRACE":
                        i += 1
                        MST()
                        if tokenList[i].type == "C_BRACE":
                            i += 1
                            return True

    # ? ************************* CLASS MULTI STATEMENT *************************

    def C_MT():
        global i, tokenList
        if tokenList[i].type in ["ID", "#", "CONSTRUCTOR", "METHOD"]:
            if C_ST():
                if C_MT():
                    return True
        else:
            return False

    # ? ************************* Interfaces *************************

    def interface():
        global i, tokenList
        if tokenList[i].type == "INTERFACE":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                if tokenList[i].type == "O_BRACE":
                    i += 1
                    interface_body()
                    if tokenList[i].type == "C_BRACE":
                        i += 1
                        return True
        return False

    def interface_body():
        global i, tokenList
        if tokenList[i].type == "METHOD":
            method_header()
            if tokenList[i].type == "TERMINATOR":
                i += 1
                interface_body_2()
        else:
            return True  # Epsilon case

    def interface_body_2():
        global i, tokenList
        if tokenList[i].type in "METHOD":
            method_header()
            i += 1
            if tokenList[i].type == "TERMINATOR":
                i += 1
                interface_body_2()
        else:
            return True  # Epsilon case
    # ? ************************* Decleration *************************

    def dec():
        global i, tokenList
        if tokenList[i].type == "DT":
            ofType = tokenList[i].value
            i += 1
            if tokenList[i].type == "ID":
                name = tokenList[i].value
                i += 1
                check = insertFunctionTable(name, ofType, currentScope)
                if (check == False):
                    reDeclarationError(name, f"Inside Scope No # {currentScope}")
                    return False
                init()
                list_()
        else:
            syntaxError("Syntax Error")

    def init():
        global i, tokenList
        if tokenList[i].type == "ASSIGN":
            i += 1
            if exp():
                if list_():
                    return True
        else:
            syntaxError("Syntax Error")
        return True

    def list_():
        global i, tokenList
        if tokenList[i].type == "TERMINATOR":
            i += 1

            dec()
        elif tokenList[i].type == "SEPARATOR":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                init()
                list_()
        elif tokenList[i].type in ['M_D_M', 'PM', 'RELATION']:
            exp()
        else:
            syntaxError("Syntax Error")

    # def list_1():
    #     global i, tokenList
    #     if tokenList[i].type == "ID":
    #         i += 1
    #         init()
    #         list_()
    #     else:
    #         return True

    # ? ************************* iterate *************************
    # <for_loop> → iterate (<init> ; <cond> ; <update>) { <body> }

    def for_loop():
        global i, tokenList
        if tokenList[i].type == "LOOP":
            i += 1
            if tokenList[i].type == "O_PARAM":
                i += 1
                for_loop_init()
                if tokenList[i].type == "TERMINATOR":
                    i += 1
                    cond()
                    if tokenList[i].type == "TERMINATOR":
                        i += 1
                        update()
                    if tokenList[i].type == "C_PARAM":
                        i += 1
                        if tokenList[i].type == "O_BRACE":
                            i += 1
                            body()
                            if tokenList[i].type == "C_BRACE":
                                i += 1
                                return True
                            else:
                                syntaxError(
                                    "Syntax Error: Missing '}'")
                        else:
                            syntaxError("Syntax Error: Missing '{'")
                    else:
                        syntaxError("Syntax Error: Missing ')'")
                else:
                    syntaxError("Syntax Error: Missing ';'")
            else:
                syntaxError("Syntax Error: Missing ';' after condition")
        else:
            syntaxError("Syntax Error: Missing '('")
    # else:
    #     syntaxError("Syntax Error: Missing 'ITERATE'")

    # <init> → <dec> | <assign_st> | E

    def for_loop_init():
        global i, tokenList
        if tokenList[i].type == "DT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                if tokenList[i].type == "ASSIGN":
                    i += 1
                    if tokenList[i].type in ['ID', 'INT', 'FLT', 'STR', 'CHAR']:
                        i += 1
                        return True
        else:
            syntaxError("Syntax Error")

    def cond():
        global i, tokenList

        if tokenList[i].type in ["ID", "INT", "FLT", "STR", "CHAR", "NOT"]:
            exp()
        else:
            return True  # Epsilon case

    def update():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            if tokenList[i].type == "INC_DEC":
                i += 1
                return True
        else:
            return True  # Epsilon case

    # ? ************************* Assignment *************************
    # <assign_st> -> ID <A2> <assignop> <exp>
    def assign_st():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            A2()
            assignop()
            exp()
        else:
            syntaxError("Syntax Error: Missing ID in assignment statement")

    def assignop():
        global i, tokenList
        if tokenList[i].type in ["ASSIGN", "COMBO_ASSIGN"]:
            i += 1
        else:
            syntaxError("Syntax Error: Invalid assignment operator")

    def A2():
        global i, tokenList
        if tokenList[i].type == "DOT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                A2()
        elif tokenList[i].type == "O_BRACK":
            i += 1
            exp()
            if tokenList[i].type == "C_BRACK":
                i += 1
                A2()
        elif tokenList[i].type == "O_PARAM":
            i += 1
            PL()
            if tokenList[i].type == "C_PARAM":
                i += 1
                F2()

    def F2():
        global i, tokenList
        if tokenList[i].type == "DOT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                A2()
        elif tokenList[i].type == "O_BRACK":
            i += 1
            exp()
            if tokenList[i].type == "C_BRACK":
                i += 1
                A2()

    def PL():
        exp()
        param2()

    def param2():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            exp()
            param2()

    # <yield_exp> → <exp> | E

    def yield_exp():
        global i, tokenList
        if tokenList[i].type in ["ID", "INT", "FLT", "STR", "CHAR"]:
            i += 1
            return True
        else:
            return True  # Epsilon case

    # <body> → <MST>

    def body():
        MST()

    # <MST> → <SST><MST>

    def MST():
        if tokenList[i].type == 'EOF':
            return False
        if SST():
            MST()
        # return True

    # <SST> → <dec> | <when_otherwise> | <iterate_st> | <assign_st> | <inc_dec_st> | <return_st> | <fn_call> | <try_catch> | <dict> | <array>

    def SST():
        if tokenList[i].type == 'EOF':
            return False
        elif (tokenList[i].type == "DT" and tokenList[i+1].type != "DEFINE"):
            dec()
            SST()
        elif tokenList[i].type == "ARRAY":
            array()
            SST()
        elif tokenList[i].type == "ID":
            assign_st()
        elif tokenList[i].type == "CALL_FUNC":
            func_call()
            SST()
        elif tokenList[i].type == "INC_DEC":
            inc_dec_st()
        elif tokenList[i].type == "WHEN":
            when_otherwise()
            SST()
        elif tokenList[i].type == "LOOP":
            for_loop()
            SST()
        elif tokenList[i].type == "YIELD":
            yield_exp()
            SST()
        elif tokenList[i].type == "ATTEMPT":
            try_catch()
            SST()
        elif tokenList[i].type == "DICT":
            dict_()
            SST()
        elif (tokenList[i].type in ['DT', 'VOID'] and tokenList[i+1].type == "DEFINE"):
            func_def()
            SST()
        # elif tokenList[i].type in ['METHOD', "CONSTRUCTOR"]:
        #     class_body()
        #     SST()

    # ? ************************* Array *************************
    def array():
        global i, tokenList
        if tokenList[i].type == "ARRAY":
            i += 1
            if tokenList[i].type == "DT":
                i += 1
                if tokenList[i].type == "ID":
                    i += 1
                    dims()
                    array_body()
        syntaxError("Syntax Error: Missing data type in array declaration")

    def dims():
        global i, tokenList
        if tokenList[i].type == "O_BRACK":
            i += 1
            if tokenList[i].type == "INT":
                i += 1
                if tokenList[i].type == "C_BRACK":
                    i += 1
                    dims()
            else:
                syntaxError(
                    "Syntax Error: Missing integer constant for array size")
        else:
            return True  # Epsilon case

    def array_body():
        global i, tokenList
        if tokenList[i].type == "ASSIGN":
            i += 1
            if tokenList[i].type == "O_BRACK":
                i += 1
                array_values()
                if tokenList[i].type == "C_BRACK":
                    i += 1
                    return True
        syntaxError("Syntax Error: Missing '=' in array declaration")

    def array_values():
        global i, tokenList
        if tokenList[i].type == "O_BRACK":
            nested_array()
        else:
            value_list()

    def nested_array():
        global i, tokenList
        if tokenList[i].type == "O_BRACK":
            i += 1
            value_list()
            if tokenList[i].type == "C_BRACK":
                i += 1
        else:
            value_list()

    def nested_array():
        global i, tokenList
        if tokenList[i].type == "O_BRACK":
            i += 1
            value_list()
            if tokenList[i].type == "C_BRACK":
                i += 1

        elif tokenList[i].type == "O_BRACK":
            i += 1
            value_list()
            if tokenList[i].type == "C_BRACK":
                i += 1
                if tokenList[i].type == "SEPARATOR":
                    nested_array()
        else:
            syntaxError("Syntax Error: Missing '[' in nested array")

    def value_list():
        global i, tokenList
        if tokenList[i].type in ["ID", "INT", "FLT", "STR", "CHAR"]:
            i += 1
            value()
        elif tokenList[i].type in ["ID", "INT", "FLT", "STR", "CHAR"]:
            value()
            if tokenList[i].type == "SEPARATOR":
                i += 1
                value_list()
        else:
            syntaxError("Syntax Error: Missing value in the value list")

    def value():
        exp()

    # ? ************************* Dict *************************

    def dict_():
        global i, tokenList, currentScope
        if tokenList[i].type == "DICT":
            ofType= tokenList[i].value
            i += 1
            if tokenList[i].type == "ID":
                name= tokenList[i].value
                check = insertFunctionTable(name, ofType, currentScope)
                if (check == False):
                    reDeclarationError(name, f"Inside Scope No # {currentScope}")
                    return False
                i += 1
                if tokenList[i].type == "ASSIGN":
                    i += 1
                    if tokenList[i].type == "O_BRACE":
                        currentScope =createScope()
                        i += 1
                        key_value_list()
                        if tokenList[i].type == "C_BRACE":
                            currentScope = destroyScope()
                            i += 1
                            return True
        syntaxError(
            "Syntax Error: Missing 'DICT' in dictionary declaration")

    def key_value_list():
        key_value()
        key_value_tail()

    def key_value_tail():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            key_value_list()
        else:
            return True  # Epsilon case

    def key_value():
        global i, tokenList
        key()
        if tokenList[i].type == "COLON":
            i += 1
            value()
        syntaxError("Syntax Error: Missing ':' in key-value pair")

    def key():
        global i, tokenList
        if tokenList[i].type == "STR" or tokenList[i].type == "CHAR":
            i += 1
            return True
        else:
            exp()

    def value():
        global i, tokenList
        if tokenList[i].type == "STR" or tokenList[i].type == "CHAR":
            i += 1
            return True
        exp()

    # ? ************************* When Otherwise Check *************************

    def when_otherwise():
        global i, tokenList
        if tokenList[i].type == "WHEN":
            i += 1
            if tokenList[i].type == "O_PARAM":
                i += 1
                exp()
                if tokenList[i].type == "C_PARAM":
                    i += 1
                    if tokenList[i].type == "O_BRACE":
                        i += 1
                        body()
                        if tokenList[i].type == "C_BRACE":
                            i += 1

                        if_else_tail()
        syntaxError("Syntax Error: Missing 'WHEN' in 'when' statement")

    def if_else_tail():
        global i, tokenList
        if tokenList[i].type == "CHECK":
            i += 1
            if tokenList[i].type == "O_PARAM":
                i += 1
                exp()
                if tokenList[i].type == "C_PARAM":
                    i += 1
                    if tokenList[i].type == "O_BRACE":
                        i += 1
                        body()
                        if tokenList[i].type == "C_BRACE":
                            i += 1
                            if_else_tail()
                    else:
                        syntaxError(
                            "Syntax Error: Missing ':' after condition in 'check' statement")
                else:
                    syntaxError(
                        "Syntax Error: Missing ')' after condition in 'check' statement")
        elif tokenList[i].type == "OTHERWISE":
            i += 1
            if tokenList[i].type == "O_BRACE":
                i += 1
                body()
                if tokenList[i].type == "C_BRACE":
                    i += 1
                if_else_tail()
            else:
                syntaxError("Syntax Error: Missing ':' after 'otherwise'")
        else:
            return True  # Epsilon case

    # ? ************************* Function Call *************************
    def func_call():
        if tokenList[i].type == 'CALL_FUNC':
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                if tokenList[i].type == "O_PARAM":
                    i += 1
                    param()
                    if tokenList[i].type == "C_PARAM":
                        i += 1
                        return True
        syntaxError(
            "Syntax Error: Missing function name in function call")

    def param():
        exp()
        param2()

    def param2():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            exp()
            param2()
        else:
            return True  # Epsilon case

    # Function Definition

    def func_def():
        global i, tokenList, currentClass, currentFunction, currentScope, scopeStack_, errorAt
        if (tokenList[i].type == "DT" or tokenList[i].type == "VOID"):
            ofType = tokenList[i].value
            i += 1
            if tokenList[i].type == "DEFINE":
                i += 1
                if tokenList[i].type == "ID":
                    name = tokenList[i].value
                    i += 1
                    check = insertFunctionTable(name, ofType, currentScope)
                    if (check == False):
                        reDeclarationError(name, 'function')
                        return False
                    if tokenList[i].type == "O_PARAM":
                        currentScope = createScope()
                        i += 1
                        args(ofType, name, currentScope)
                        if tokenList[i].type == "C_PARAM":
                            i += 1

                            if tokenList[i].type == "O_BRACE":
                                i += 1
                                body()
                                if tokenList[i].type == "C_BRACE":
                                    currentScope = destroyScope()
                                    i += 1
                                    return True

        syntaxError(
            "Syntax Error: Missing 'DEFINE' keyword in function definition")

    def args(ofType, name, currentScope):
        global i, tokenList
        if tokenList[i].type == "DT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                n_args()
        syntaxError(
            "Syntax Error: Missing data type in function arguments")

    def n_args():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            if tokenList[i].type == "DT":
                i += 1
                if tokenList[i].type == "ID":
                    i += 1
                    n_args()
            syntaxError(
                "Syntax Error: Missing data type in function arguments")
        else:
            return True  # Epsilon case

    # Assignment Statement

    def assign_st():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            A2()
            if tokenList[i].type == "ASSIGN":
                i += 1
                exp()
        syntaxError(
            "Syntax Error: Missing variable name in assignment statement")

    def A2():
        global i, tokenList
        if tokenList[i].type == "DOT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                A2()
        elif tokenList[i].type == "O_BRACK":
            i += 1
            exp()
            if tokenList[i].type == "C_BRACK":
                i += 1
                A2()
        elif tokenList[i].type == "O_PARAM":
            i += 1
            PL()
            if tokenList[i].type == "C_PARAM":
                i += 1
                F2()
        else:
            return True  # Epsilon case

    def F2():
        global i, tokenList
        if tokenList[i].type == "DOT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                A2()
        elif tokenList[i].type == "O_BRACK":
            i += 1
            exp()
            if tokenList[i].type == "C_BRACK":
                i += 1
                A2()
        else:
            return True  # Epsilon case

    def PL():
        exp()
        param2()

    def param2():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            exp()
            param2()
        else:
            return True  # Epsilon case

    # Increment-Decrement Statement

    def inc_dec_st():
        global i, tokenList
        if tokenList[i].type in ["ID", "STR", "CHAR", "FLT", "INT"]:
            i += 1
            exp()
            inc_dec_op()
        else:
            syntaxError(
                "Syntax Error: Missing identifier or value for increment/decrement statement")

    def inc_dec_op():
        global i, tokenList
        if tokenList[i].type == "INC_DEC":
            i += 1
        elif tokenList[i].value in ["++", "--"]:
            i += 1
        else:
            syntaxError("Syntax Error: Invalid increment/decrement operator")

    # ? ************************* Try Catch *************************
    def try_catch():
        global i, tokenList
        if tokenList[i].type == "ATTEMPT":
            i += 1
            if tokenList[i].type == "O_BRACE":
                i += 1
                body()
                if tokenList[i].type == "C_BRACE":
                    i += 1
                    catch_block()
                    if tokenList[i].type == "FINALLY":
                        i += 1
                        if tokenList[i].type == "O_BRACE":
                            i += 1
                            body()
                            if tokenList[i].type == "C_BRACE":
                                i += 1
                                return True
        syntaxError(
            "Syntax Error: Missing 'ATTEMPT' keyword in 'try-catch' statement")

    def catch_block():
        global i, tokenList
        if tokenList[i].type == "CATCH":
            i += 1
            if tokenList[i].type == "O_PARAM":
                i += 1
                if tokenList[i].type == "ERROR":
                    i += 1
                    if tokenList[i].type == "C_PARAM":
                        i += 1
                        if tokenList[i].type == "O_BRACE":
                            i += 1
                            body()
                            if tokenList[i].type == "C_BRACE":
                                i += 1
                                return True
            syntaxError("Syntax Error: Missing '(' in 'catch' block")
        else:
            return True  # Epsilon case

    # ? ************************* Expression *************************
    # <exp>-> <a> <exp'>
    def exp():
        if a():
            return True
        if exp_prime():
            return True
        return False

    def exp_prime():
        global i, tokenList
        if tokenList[i].type == "OR":
            i += 1
            if a():
                return True
            if exp_prime():
                return True
        return False

    def a():
        if r():
            return True
        if a_prime():
            return True
        return False

    def a_prime():
        global i, tokenList
        if tokenList[i].type == "AND":
            i += 1
            if r():
                return True
            if a_prime():
                return True
        return False

    def r():
        if e():
            return True
        if r_prime():
            return True
        return False

    def r_prime():
        global i, tokenList
        if tokenList[i].type == "RELATION":
            i += 1
            if e():
                return True
            if r_prime():
                return True
        return False

    def e():
        if t():
            return True
        if e_prime():
            return True
        return False

    def e_prime():
        global i, tokenList
        if tokenList[i].type == "PM" or tokenList[i+1].type == "ASSIGN":
            i += 1
            if t():
                return True
            if e_prime():
                return True
        return False

    def t():
        if f():
            return True
        if t_prime():
            return True
        return False

    def t_prime():
        global i, tokenList
        if tokenList[i].type == "M_D_M":
            i += 1
            if f():
                return True
            if t_prime():
                return True
        return False

    def f():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            f_init()
        elif tokenList[i].type in ["INT", "FLT", "STR", "CHAR"]:
            i += 1
            return True
        elif tokenList[i].type == "NOT":
            i += 1
            if f():
                return True
        elif tokenList[i].type == "CALLING":
            i += 1
            func_call()
        syntaxError("Syntax Error: Expected ID or literal")

    def f_init():
        global i, tokenList
        if tokenList[i].type == "O_BRACK":
            i += 1
            exp()
            if tokenList[i].type == "C_BRACK":
                i += 1
                f_init()
        elif tokenList[i].type == "ID":
            i += 1
            f_init()
        elif tokenList[i].type == "INC_DEC":
            i += 1
        else:
            return True

    def f_init_tail():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            f_init()
        elif tokenList[i].type == "O_BRACK":
            i += 1
            exp()
            if tokenList[i].type == "C_BRACK":
                i += 1
                f_init()
        else:
            return True

    # Function calling
    def func_call():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            if tokenList[i].type == "O_PARAM":
                i += 1
                param()
                if tokenList[i].type == "C_PARAM":
                    i += 1
                    return True
        syntaxError(
            "Syntax Error: Missing function name in function call")

    def param():
        exp()
        param2()

    def param2():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            exp()
            param2()
        else:
            return True

except LookupError:
    print("Tree Incomplete... Input Completely Parsed")
