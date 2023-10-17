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
        synError += "\nTOKEN UNEXPECTED:\n\tValue:\t" + tokenList[errorAt].value + "\n\tType:\t" + tokenList[errorAt].type + \
            "\n\tFile:\t\'.\\input.txt\' [@ " + str(
                tokenList[errorAt].line) + "]\n\tToken:\t" + str(errorAt) + "\n\n\n"
        print("\nTOKEN UNEXPECTED:\n\tValue:\t" + tokenList[errorAt].value + "\n\tType:\t" + tokenList[errorAt].type +
              "\n\tFile:\t\'.\\input.txt\' [@ " + str(tokenList[errorAt].line) + "]\n\tToken:\t" + str(errorAt))
    if result:
        print("Source code is syntactically correct :)")
    return synError, result


def syntaxError():
    global i, tokenList, errorAt
    if (i > errorAt):
        errorAt = i
    return False


try:
    def structure():
        global i, tokenList
        if tokenList[i].type == "mst":
            i += 1
            structure()
        elif class_def():
            structure()
        elif func_def():
            structure()
        else:
            raise Exception("Syntax Error: Invalid start rule")

    def class_def():
        global i, tokenList
        if tokenList[i].type == "sealed":
            i += 1
            if tokenList[i].type == "class":
                i += 1
                if tokenList[i].type.type == "ID":
                    i += 1
                    if tokenList[i].type == "O_BRACE":
                        i += 1
                        class_body()
                        if tokenList[i].type == "C_BRACE":
                            i += 1
                            return True
        elif tokenList[i].type == "class":
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
            pass  # Epsilon case

    def inheritance_2():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            if tokenList[i].type.type == "ID":
                i += 1
                inheritance_2()
        else:
            pass  # Epsilon case

    def class_body():
        global i, tokenList
        XMST()

    def XMST():
        global i, tokenList
        if tokenList[i].type in ["ID", "#", "constructor", "method"]:
            XSST()
            XMST()
        else:
            pass  # Epsilon case

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
        else:
            pass  # Epsilon case

    def params():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            params2()
        else:
            pass  # Epsilon case

    def params2():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                params2()
        else:
            pass  # Epsilon case

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
            pass  # Epsilon case

    def interface_body_2():
        global i, tokenList
        if tokenList[i].type in ["ID", "constructor", "method"]:
            method_sign()
            if tokenList[i].type == "TERMINATOR":
                i += 1
                interface_body_2()
        else:
            pass  # Epsilon case

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
        else:
            pass  # Epsilon case

    def dec():
        global i, tokenList
        if tokenList[i].type == "DT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                init()
                list()
        else:
            raise Exception("Syntax Error")

        def init():
            global i, tokenList
            if tokenList[i].type == "ASSIGN":
                i += 1
                init_1()
            elif tokenList[i].type == "TERMINATOR":
                return
            else:
                raise Exception("Syntax Error")

        def init_1():
            global i, tokenList
            if tokenList[i].type == "ID":
                i += 1
                init_2()
            elif tokenList[i].type in ["STR", "CHAR", "FLT", "INT"]:
                i += 1
            else:
                exp()

        def init_2():
            global i, tokenList
            if tokenList[i].type == "SEPARATOR":
                i += 1
                if tokenList[i].type == "ID":
                    i += 1
                    init_2()

        def list():
            global i, tokenList
            if tokenList[i].type == "TERMINATOR":
                i += 1
                list_1()
            elif tokenList[i].type == "SEPARATOR":
                i += 1
                if tokenList[i].type == "ID":
                    i += 1
                    init()
                    list()
            else:
                raise Exception("Syntax Error")

        def list_1():
            global i, tokenList
            if tokenList[i].type == "ID":
                i += 1
                init()
                list()
            else:
                return

    # <for_loop> → iterate (<init> ; <cond> ; <update>) { <body> }

    def for_loop():
        global i, tokenList
        if tokenList[i].type == "LOOP":
            i += 1
            if tokenList[i].type == "O_PARAM":
                i += 1
                init()
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
                                else:
                                    raise Exception(
                                        "Syntax Error: Missing '}'")
                            else:
                                raise Exception("Syntax Error: Missing '{'")
                        else:
                            raise Exception("Syntax Error: Missing ')'")
                    else:
                        raise Exception("Syntax Error: Missing ';'")
                else:
                    raise Exception(
                        "Syntax Error: Missing ';' after condition")
            else:
                raise Exception("Syntax Error: Missing '('")
        else:
            raise Exception("Syntax Error: Missing 'ITERATE'")

    # <init> → <dec> | <assign_st> | E

    def init():
        global i, tokenList
        if tokenList[i].type in ["DT", "ID"]:
            dec()
        elif tokenList[i].type == "ID":
            assign_st()
        else:
            pass  # Epsilon case

    def cond():
        global i, tokenList
        if tokenList[i].type in ["ID", "INT", "FLT", "STR"]:
            comparison()
            cond_1()
        else:
            pass  # Epsilon case

    def cond_1():
        global i, tokenList
        if tokenList[i].type == "RELATION":
            i += 1
            comparison()
        else:
            pass  # Epsilon case

    def comparison():
        global i, tokenList
        if tokenList[i].type in ["ID", "INT", "FLT", "STR"]:
            i += 1
        else:
            raise Exception(
                "Syntax Error: Expected ID or constant in comparison")

    def update():
        global i, tokenList
        if tokenList[i].type == "INC_DEC":
            i += 1
            exp()
        elif tokenList[i].type == "ID":
            assign_st()
        else:
            pass  # Epsilon case

    # <assign_st> -> ID <A2> <assignop> <exp>
    def assign_st():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            A2()
            assignop()
            exp()
        else:
            raise Exception("Syntax Error: Missing ID in assignment statement")

    def assignop():
        global i, tokenList
        if tokenList[i].type in ["ASSIGN","COMBO_ASSIGN"]:
            i += 1
        else:
            raise Exception("Syntax Error: Invalid assignment operator")
    
    # <A2> -> <A2_tail>

    def A2():
        A2_tail()

    # <A2_tail> -> .ID <A2> | [<exp>] <A2> | (<PL>) <F2> | E

    def A2_tail():
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
            pass  # Epsilon case

    # <F2> -> .ID <A2> | [<exp>] <A2> | E

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

    # <PL> -> <exp> <param2>

    def PL():
        exp()
        param2()

    # <param2> -> , <exp> <param2> | E

    def param2():
        global i, tokenList
        if tokenList[i].type == "SEPARATOR":
            i += 1
            exp()
            param2()
        else:
            pass  # Epsilon case

    # <yield_exp> → <exp> | E

    def yield_exp():
        global i, tokenList
        if tokenList[i].type in ["ID", "INT", "FLT", "STR", "CHAR"]:
            i += 1
        else:
            pass  # Epsilon case

    # <body> → <MST>

    def body():
        MST()

    # <MST> → <SST><MST>

    def MST():
        SST()
        MST()

    # <SST> → <dec> | <when_otherwise> | <iterate_st> | <assign_st> | <inc_dec_st> | <return_st> | <fn_call> | <try_catch> | <dict> | <array>

    def SST():
        if tokenList[i].type == "DT":
            dec()
        elif tokenList[i].type == "WHEN":
            when_otherwise()
        elif tokenList[i].type == "ITERATE":
            for_loop()
        elif tokenList[i].type == "ID":
            assign_st()

    # Array
    def array():
        if tokenList[i].type == "DT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                dim()
                if tokenList[i].type == "ASSIGN":
                    i += 1
                    array_init()
                else:
                    raise Exception(
                        "Syntax Error: Missing '=' in array declaration")
            else:
                raise Exception(
                    "Syntax Error: Missing ID in array declaration")
        else:
            raise Exception(
                "Syntax Error: Missing data type in array declaration")

    def dim():
        global i, tokenList
        if tokenList[i].type == "O_BRACK":
            i += 1
            size()
            if tokenList[i].type == "C_BRACK":
                i += 1
                dim()
        else:
            pass  # Epsilon case

    def array_init():
        global i, tokenList
        if tokenList[i].type == "O_BRACK":
            i += 1
            exp()
            if tokenList[i].type == "C_BRACK":
                i += 1
            else:
                raise Exception(
                    "Syntax Error: Missing ']' in array initialization")
        else:
            raise Exception(
                "Syntax Error: Missing '[' in array initialization")

    def size():
        global i, tokenList
        if tokenList[i].type == "INT":
            i += 1
        else:
            raise Exception(
                "Syntax Error: Missing integer constant for array size")

    # Dict

    def dict_():
        if tokenList[i].type == "DICT":
            i += 1
            if tokenList[i].type == "O_BRACE":
                i += 1
                key_value_list()
                if tokenList[i].type == "C_BRACE":
                    i += 1
                else:
                    raise Exception(
                        "Syntax Error: Missing '}' in dictionary declaration")
            else:
                raise Exception(
                    "Syntax Error: Missing '{' in dictionary declaration")
        else:
            raise Exception(
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
            pass  # Epsilon case

    def key_value():
        key()
        if tokenList[i].type == "COLON":
            i += 1
            value()
        else:
            raise Exception("Syntax Error: Missing ':' in key-value pair")

    def key():
        exp()

    def value():
        exp()

    # When Otherwise Check

    def when_otherwise():
        if tokenList[i].type == "WHEN":
            i += 1
            if tokenList[i].type == "O_PARAM":
                i += 1
                exp()
                if tokenList[i].type == "C_PARAM":
                    i += 1
                    if tokenList[i].type == "COLON":
                        i += 1
                        body()
                        if_else_tail()
                    else:
                        raise Exception(
                            "Syntax Error: Missing ':' after condition in 'when' statement")
                else:
                    raise Exception(
                        "Syntax Error: Missing ')' after condition in 'when' statement")
            else:
                raise Exception(
                    "Syntax Error: Missing '(' in 'when' statement")
        else:
            raise Exception("Syntax Error: Missing 'WHEN' in 'when' statement")

    def if_else_tail():
        global i, tokenList
        if tokenList[i].type == "CHECK":
            i += 1
            if tokenList[i].type == "O_PARAM":
                i += 1
                exp()
                if tokenList[i].type == "C_PARAM":
                    i += 1
                    if tokenList[i].type == "COLON":
                        i += 1
                        body()
                        if_else_tail()
                    else:
                        raise Exception(
                            "Syntax Error: Missing ':' after condition in 'check' statement")
                else:
                    raise Exception(
                        "Syntax Error: Missing ')' after condition in 'check' statement")
        elif tokenList[i].type == "OTHERWISE":
            i += 1
            if tokenList[i].type == "COLON":
                i += 1
                body()
                if_else_tail()
            else:
                raise Exception("Syntax Error: Missing ':' after 'otherwise'")
        else:
            pass  # Epsilon case

    # Function Calling
    def func_call():
        if tokenList[i].type == "ID":
            i += 1
            if tokenList[i].type == "O_PARAM":
                i += 1
                param()
                if tokenList[i].type == "C_PARAM":
                    i += 1
                else:
                    raise Exception(
                        "Syntax Error: Missing ')' in function call")
            else:
                raise Exception("Syntax Error: Missing '(' in function call")
        else:
            raise Exception(
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
            pass  # Epsilon case

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
                            else:
                                raise Exception("Syntax Error: Missing '}' in function body")
                        else:
                            raise Exception("Syntax Error: Missing '{' in function body")
                    else:
                        raise Exception("Syntax Error: Missing ')' in function definition")
                else:
                    raise Exception("Syntax Error: Missing '(' in function definition")
            else:
                raise Exception("Syntax Error: Missing function name in function definition")
        else:
            raise Exception("Syntax Error: Missing 'DEFINE' keyword in function definition")


    def DT_func():
        global i, tokenList
        if tokenList[i].type in ["VOID", "INT"]:
            i += 1
        else:
            raise Exception(
                "Syntax Error: Missing return type in function definition")

    def args():
        if tokenList[i].type == "DT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                n_args()
        else:
            raise Exception(
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
            else:
                raise Exception(
                    "Syntax Error: Missing data type in function arguments")
        else:
            pass  # Epsilon case

    # Assignment Statement

    def assign_st():
        if tokenList[i].type == "ID":
            i += 1
            A2()
            if tokenList[i].type == "ASSIGN":
                i += 1
                exp()
            else:
                raise Exception(
                    "Syntax Error: Missing '=' in assignment statement")
        else:
            raise Exception(
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
            pass  # Epsilon case

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
            pass  # Epsilon case

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
            pass  # Epsilon case

    # Increment-Decrement Statement

    def inc_dec_st():
        global i, tokenList
        if tokenList[i].type == "INC_DEC":
            i += 1
            exp()
        else:
            exp()
            if tokenList[i].type == "INC_DEC":
                i += 1
            else:
                raise Exception(
                    "Syntax Error: Missing increment/decrement operator")

    # Attempt Catch

    def try_catch():
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
                            else:
                                raise Exception(
                                    "Syntax Error: Missing '}' in 'finally' block")
                        else:
                            raise Exception(
                                "Syntax Error: Missing '{' in 'finally' block")
                    else:
                        raise Exception(
                            "Syntax Error: Missing 'FINALLY' block in 'try-catch' statement")
                else:
                    raise Exception(
                        "Syntax Error: Missing '}' in 'attempt' block")
            else:
                raise Exception("Syntax Error: Missing '{' in 'attempt' block")
        else:
            raise Exception(
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
                        else:
                            raise Exception(
                                "Syntax Error: Missing '}' in 'catch' block")
                    else:
                        raise Exception(
                            "Syntax Error: Missing '{' in 'catch' block")
                else:
                    raise Exception(
                        "Syntax Error: Missing error variable in 'catch' block")
            else:
                raise Exception("Syntax Error: Missing '(' in 'catch' block")
        else:
            pass  # Epsilon case

    # <exp>-> <a> <exp'>
    def exp():
        a()
        exp_prime()

    # <exp'>-> OR <a> <exp'> | ϵ
    def exp_prime():
        global i, tokenList
        if tokenList[i].type == "OR":
            i += 1
            a()
            exp_prime()
        else:
            pass  # Epsilon case

    # <a> -> <r> <a'>
    def a():
        r()
        a_prime()

    # <a'>  -> AND <r> <a'> | ϵ
    def a_prime():
        global i, tokenList
        if tokenList[i].type == "AND":
            i += 1
            r()
            a_prime()
        else:
            pass  # Epsilon case

    # <r> -> <e> <r'>
    def r():
        e()
        r_prime()

    # <r'> -> ROP<e> <r'> | ϵ
    def r_prime():
        global i, tokenList
        if tokenList[i].type == "RELATION":
            i += 1
            e()
            r_prime()
        else:
            pass  # Epsilon case

    # <e>  -> <t> <e'>
    def e():
        t()
        e_prime()

    # <e'> -> PM<t> <e'> | ϵ
    def e_prime():
        global i, tokenList
        if tokenList[i].type == "PM":
            i += 1
            t()
            e_prime()
        else:
            pass  # Epsilon case

    # <t> -> <q> <t'>
    def t():
        q()
        t_prime()

    # <t'> -> MDM <q> <t'> | ϵ
    def t_prime():
        global i, tokenList
        if tokenList[i].type == "M_D_M":
            i += 1
            q()
            t_prime()
        else:
            pass  # Epsilon case

    # <q> -> <F> <q'>
    def q():
        F()
        q_prime()

    # <q'> -> NOT <F> <q'> | ϵ
    def q_prime():
        global i, tokenList
        if tokenList[i].type == "NOT":
            i += 1
            F()
            q_prime()
        else:
            pass  # Epsilon case

    # <F>-> ID <F'>
    def F():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            F_prime()
        else:
            raise Exception("Syntax Error: Expected ID")

    # <F'>  -> <func_call> | <inc_dec_st> | <exp> | !<F> | <const> | ϵ
    def F_prime():
        global i, tokenList
        if tokenList[i].type == "O_PARAM":
            func_call()
        elif tokenList[i].type == "INC_DEC":
            inc_dec_st()
        elif tokenList[i].type in ["ID", "INT", "FLT", "STR", "CHAR"]:
            exp()
        elif tokenList[i].type == "NOT":
            i += 1
            F()
        else:
            pass  # Epsilon case

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
                else:
                    raise Exception(
                        "Syntax Error: Missing ')' in function call")
            else:
                raise Exception("Syntax Error: Missing '(' in function call")
        else:
            raise Exception(
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
            pass  # Epsilon case

    # Increment-Decrement Statement
    def inc_dec_st():
        global i, tokenList
        if tokenList[i].type == "INC_DEC":
            i += 1
            exp()
        else:
            exp()
            if tokenList[i].type == "INC_DEC":
                i += 1
            else:
                raise Exception(
                    "Syntax Error: Missing increment/decrement operator")

except LookupError:
    print("Tree Incomplete... Input Completely Parsed")
