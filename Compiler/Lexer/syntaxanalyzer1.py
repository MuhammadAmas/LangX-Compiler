i = 0
tokenList = []
# syntaxErr = True
errorAt = 0
synError = ""


def syntaxAnalyzer(tokens):
    global i, tokenList, errorAt, synError
    i = 0
    errorAt = 0
    tokenList = tokens
    result = structure()
    if (not result):
        # print('Syntax error')
        synError += "\nTOKEN UNEXPECTED:\n\tValue:\t" + tokenList[errorAt].value + "\n\tType:\t" + tokenList[errorAt].type + \
            "\n\tFile:\t\'.\\input.txt\' [@ " + str(
                tokenList[errorAt].line) + "]\n\tToken:\t" + str(errorAt) + "\n\n\n"
        print("\nTOKEN UNEXPECTED:\n\tValue:\t" + tokenList[errorAt].value + "\n\tType:\t" + tokenList[errorAt].type +
              "\n\tFile:\t\'.\\input.txt\' [@ " + str(tokenList[errorAt].line) + "]\n\tToken:\t" + str(errorAt))
    if result:
        print("Source code is syntactically correct :)")
    return synError, result


def syntaxError(message):
    global i, tokenList, errorAt
    if (i > errorAt):
        errorAt = i
    return False


try:
    def structure():
        global i, tokenList
        if tokenList[i].type == 'EOF':
            return True
        if MST():
            structure()
        elif class_def():
            structure()
        elif func_def():
            structure()
        syntaxError("Syntax Error: Invalid start rule")

    def class_def():
        global i, tokenList
        if tokenList[i].type == "SEALED":
            i += 1
            if tokenList[i].type == "GROUP":
                i += 1
                if tokenList[i].type == "ID":
                    i += 1
                    if tokenList[i].type == "O_BRACE":
                        i += 1
                        class_body()
                        if tokenList[i].type == "C_BRACE":
                            i += 1
                            return True
        elif tokenList[i].type == "GROUP":
            i += 1
            if tokenList[i].type.type == "ID":
                i += 1
                inheritance()
                if tokenList[i].type == "O_BRACE":
                    i += 1
                    class_body()
                    if tokenList[i].type == "C_BRACE":
                        i += 1
                        return True
        return False

    # ? ************************* Inheritance *************************
    def inheritance():
        global i, tokenList
        if tokenList[i].type == "extends":
            i += 1
            if tokenList[i].type.type == "ID":
                i += 1
        elif tokenList[i].type == "implements":
            i += 1
            if tokenList[i].type.type == "ID":
                i += 1
                inheritance_2()
        else:
            return True # Epsilon case

    def inheritance_2():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            if tokenList[i].type.type == "ID":
                i += 1
                inheritance_2()
        else:
            return True # Epsilon case

    def class_body():
        global i, tokenList
        XMST()

    def XMST():
        global i, tokenList
        if tokenList[i].type in ["ID", "#", "constructor", "method"]:
            XSST()
            XMST()
        else:
            return True # Epsilon case

    def XSST():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            init()
            if tokenList[i].type == "TERMINATOR":
                i += 1
        elif tokenList[i].type == "#":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                init()
                if tokenList[i].type == "TERMINATOR":
                    i += 1
        elif tokenList[i].type == "constructor":
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
        else:
            return True # Epsilon case

    def params():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            params2()
        else:
            return True # Epsilon case

    def params2():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                params2()
        else:
            return True # Epsilon case

    # ? ************************* Interfaces *************************

    def interface():
        global i, tokenList
        if tokenList[i].type == "interface":
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
        if tokenList[i].type in ["ID", "constructor", "method"]:
            method_sign()
            if tokenList[i].type == "TERMINATOR":
                i += 1
                interface_body_2()
        else:
            return True # Epsilon case

    def interface_body_2():
        global i, tokenList
        if tokenList[i].type in ["ID", "constructor", "method"]:
            method_sign()
            if tokenList[i].type == "TERMINATOR":
                i += 1
                interface_body_2()
        else:
            return True # Epsilon case

    def method_sign():
        global i, tokenList
        if tokenList[i].type in ["constructor", "method"]:
            i += 1
            if tokenList[i].type.type == "ID":
                i += 1
                if tokenList[i].type == "O_PARAM":
                    i += 1
                    params()
                    if tokenList[i].type == "C_PARAM":
                        i += 1
                        return True
        else:
            return True # Epsilon case

    # ? ************************* Decleration *************************
    def dec():
        global i, tokenList
        if tokenList[i].type == "DT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                init()
                list_()
        else:
            syntaxError("Syntax Error")

    def init():
        global i, tokenList
        if tokenList[i].type == "ASSIGN":
            i += 1
            init_1()
        elif tokenList[i].type == "TERMINATOR":
            return True
        else:
            syntaxError("Syntax Error")

    def init_1():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            init_2()
        elif tokenList[i].type in ["STR", "CHAR", "FLT", "INT"]:
            i += 1
            return True
        else:
            
            exp()

    def init_2():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                init_2()

    def list_():
        global i, tokenList
        if tokenList[i].type == "TERMINATOR":
            i += 1
            list_1()
        elif tokenList[i].type == "SEPARATOR":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                init()
                list_()
        else:
            syntaxError("Syntax Error")

    def list_1():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            init()
            list_()
        else:
            return True

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
                    syntaxError(
                        "Syntax Error: Missing ';' after condition")
            else:
                syntaxError("Syntax Error: Missing '('")
        else:
            syntaxError("Syntax Error: Missing 'ITERATE'")

    # <init> → <dec> | <assign_st> | E

    def for_loop_init():
        global i, tokenList
        if tokenList[i].type in ["DT", "ID"]:
            dec()
        elif tokenList[i].type == "ID":
            assign_st()
        else:
            return True # Epsilon case

    def cond():
        global i, tokenList
        if tokenList[i].type in ["ID", "INT", "FLT", "STR","CHAR","NOT"]:
            exp()
        else:
            return True # Epsilon case

    def update():
        global i, tokenList
        if tokenList[i].type == "INC_DEC":
            i += 1
            inc_dec_st()
        elif tokenList[i].type == "ID":
            assign_st()
        else:
            return True # Epsilon case

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
            return True # Epsilon case

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
        elif tokenList[i].type == "DT":
            dec()
        elif tokenList[i].type == "ARRAY":
            array()
        elif tokenList[i].type == "ID":
            assign_st()
        elif tokenList[i].type == "CALL_FUNC":
            func_call()
        elif tokenList[i].type == "INC_DEC":
            inc_dec_st()
        elif tokenList[i].type == "WHEN":
            when_otherwise()
        elif tokenList[i].type == "LOOP":
            for_loop()
        elif tokenList[i].type == "YIELD":
            yield_exp()
        elif tokenList[i].type == "ATTEMPT":
            try_catch()
        elif tokenList[i].type == "DICT":
            dict_()

    # ? ************************* Array *************************
    # Array
    def array():
        global i, tokenList
        if tokenList[i].type == "ARRAY":
            i+=1
            if tokenList[i].type == "DT":
                i += 1
                if tokenList[i].type == "ID":
                    i += 1
                    dims()
                    array_body()
                else:
                    syntaxError("Syntax Error: Missing ID in array declaration")
            else:
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
                syntaxError("Syntax Error: Missing integer constant for array size")
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
                else:
                    syntaxError("Syntax Error: Missing ']' in array body")
            else:
                syntaxError("Syntax Error: Missing '[' in array body")
        else:
            syntaxError("Syntax Error: Missing '=' in array declaration")

    def array_values():
        global i, tokenList
        if tokenList[i].type in ["O_BRACK"]: 
            nested_array()
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
            i+=1
            value_list()
            if tokenList[i].type == "C_BRACK":
                i+=1
                if tokenList[i].type == "SEPARATOR":
                    value_list()
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
        global i , tokenList
        if tokenList[i].type == "DICT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                if tokenList[i].type == "ASSIGN":
                    i += 1
                    if tokenList[i].type == "O_BRACE":
                        i += 1
                        key_value_list()
                        if tokenList[i].type == "C_BRACE":
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
            return True # Epsilon case

    def key_value():
        key()
        if tokenList[i].type == "COLON":
            i += 1
            value()
        syntaxError("Syntax Error: Missing ':' in key-value pair")

    def key():
        exp()

    def value():
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
                    else:
                        syntaxError(
                            "Syntax Error: Missing ':' after condition in 'when' statement")
                else:
                    syntaxError(
                        "Syntax Error: Missing ')' after condition in 'when' statement")
            else:
                syntaxError(
                    "Syntax Error: Missing '(' in 'when' statement")
        else:
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
            return True # Epsilon case

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
            return True # Epsilon case

    # Function Definition

    def func_def():
        global i, tokenList
        DT_func()
        if tokenList[i].type == "DEFINE":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                if tokenList[i].type == "O_PARAM":
                    i += 1
                    args()
                    if tokenList[i].type == "C_PARAM":
                        i += 1
                        if tokenList[i].type == "O_BRACE":
                            i += 1
                            body()
                            if tokenList[i].type == "C_BRACE":
                                i += 1
                                return True
        syntaxError(
            "Syntax Error: Missing 'DEFINE' keyword in function definition")

    def DT_func():
        global i, tokenList
        if tokenList[i].type in ["VOID", "INT"]:
            i += 1
            return True
        syntaxError(
            "Syntax Error: Missing return type in function definition")

    def args():
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
            return True # Epsilon case

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
            return True # Epsilon case

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
            return True # Epsilon case

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
            return True # Epsilon case

    # Increment-Decrement Statement

    def inc_dec_st():
        global i, tokenList
        if tokenList[i].type in ["ID", "STR", "CHAR", "FLT", "INT"]:
            i += 1
            exp()
            inc_dec_op()
        else:
            syntaxError("Syntax Error: Missing identifier or value for increment/decrement statement")

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
        global i , tokenList
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
                if tokenList[i].type == "ID" and tokenList[i + 1] == "C_PARAM":
                    i += 2
                    if tokenList[i].type == "O_BRACE":
                        i += 1
                        body()
                        if tokenList[i].type == "C_BRACE":
                            i += 1
                            return True
            syntaxError("Syntax Error: Missing '(' in 'catch' block")
        else:
            return True # Epsilon case

    # ? ************************* Expression *************************
    # <exp>-> <a> <exp'>
    def exp():
        a()
        exp_prime()

    def exp_prime():
        global i, tokenList
        if tokenList[i].type == "OR":
            i += 1
            a()
            exp_prime()

    def a():
        r()
        a_prime()

    def a_prime():
        global i, tokenList
        if tokenList[i].type == "AND":
            i += 1
            r()
            a_prime()

    def r():
        e()
        r_prime()

    def r_prime():
        global i, tokenList
        if tokenList[i].type == "RELATION":
            i += 1
            e()
            r_prime()

    def e():
        t()
        e_prime()

    def e_prime():
        global i, tokenList
        if tokenList[i].type == "PM":
            i += 1
            t()
            e_prime()

    def t():
        f()
        t_prime()

    def t_prime():
        global i, tokenList
        if tokenList[i].type == "M_D_M":
            i += 1
            f()
            t_prime()

    def f():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            f_init()
        elif tokenList[i].type in ["INT", "FLT", "STR", "CHAR"]:
            i += 1
        elif tokenList[i].type == "NOT":
            i += 1
            f()
        elif tokenList[i].type == "CALLING":
            i += 1
            func_call()
        else:
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
