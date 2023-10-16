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
              "\n\tFile:\t\'.\\input.txt\' [@ " + str(tokenList[errorAt].line) + "]\n\tToken:\t" + str(errorAt) + "\n\n\n"
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

# <start> → mst <start> | class def <start> | func def <start> 
try: 
    # ? **************************** structure ********************************
    def structure():
        global i, tokenList
        if tokenList[i].type == "EOF":
            return True
        elif mst():
            return structure()
        # elif class_def():
        #     return structure()
        elif func_def():
            return structure()
        return syntaxError()
    
    def body():
        return mst()
    
    def mst():
        if SST():
            return mst()
        return True
    
    # ? **************************** SST ********************************
    def SST():
        global i, tokenList
        if dec():
            print('decleration')
            return True
        elif when_otherwise():
            return True
        elif assign_st():
            return True
        elif inc_dec_st():
            return True
        elif yield_st():
            return True
        elif func_call():
            return True
        elif try_catch():
            return True
        elif dict_():
            return True
        elif array():
            return True
        return syntaxError()
            

    # ? **************************** function definition******************************** 
    def func_def():
        if DT_func():
            if tokenList[i].type == "DEFINE":
                i += 1
                if tokenList[i].type == "ID":
                    i += 1
                    if tokenList[i].type == "O_PARAN":
                        i += 1
                        if args():
                            if tokenList[i].type == "C_PARAN":
                                i += 1
                                if tokenList[i].type == "O_BRACE":
                                    i += 1
                                    if body():
                                        return True
        return syntaxError()

    def DT_func():
        global i, tokenList
        if tokenList[i].type in ["VOID", "INT"]:
            i += 1
            return True
        return syntaxError()

    def args():
        if tokenList[i].type == "DT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                return n_args()
        return syntaxError()

    def n_args():
        global i, tokenList
        if tokenList[i].type == "COMMA":
            i += 1
            if tokenList[i].type == "DT":
                i += 1
                if tokenList[i].type == "ID":
                    i += 1
                    return n_args()
        return True


    # ? **************************** return st ********************************
    def yield_st():
        global i, tokenList
        if tokenList[i].type == "YIELD":
            i += 1
            if exp():
                return True
        return syntaxError()

    # ? **************************** function call ********************************
    def func_call():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            if tokenList[i].type == "O_PARAN":
                i += 1
                if param():
                    if tokenList[i].type == "C_PARAN":
                        i += 1
                        return True
        return syntaxError()

    def param():
        if exp():
            return param2()
        return syntaxError()

    def param2():
        global i, tokenList
        if tokenList[i].type == "COMMA":
            i += 1
            if exp():
                return param2()
        return True

    # ? **************************** if else ********************************
    def when_otherwise():
        global i, tokenList
        if tokenList[i].type == "WHEN":
            i += 1
            if tokenList[i].type == "O_PARAN":
                i += 1
                if exp() and tokenList[i].type == "C_PARAN":
                    i += 1
                    if tokenList[i].type == "O_BRACE":
                        i += 1
                        if body():
                            if if_else_tail():
                                return True
        return syntaxError()

    def when_otherwise_tail():
        global i, tokenList
        if tokenList[i].type == "CHECK":
            i += 1
            if tokenList[i].type == "O_PARAN":
                i += 1
                if exp() and tokenList[i].type == "C_PARAN":
                    i += 1
                    if tokenList[i].type == "O_BRACE":
                        i += 1
                        if body():
                            if when_otherwise_tail():
                                return True
        elif tokenList[i].type == "OTHERWISE":
            i += 1
            if tokenList[i].type == "O_BRACE":
                i += 1
                if body():
                    if when_otherwise_tail():
                        return True
        return True

    # ? **************************** array ********************************
    def array():
        global i, tokenList
        if tokenList[i].type == "DT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                if dim():
                    if tokenList[i].type == "ASSIGN":
                        i += 1
                        if array_init():
                            return True
        return syntaxError()

    def dim():
        if tokenList[i].type == "O_BRACK":
            i += 1
            if size():
                if tokenList[i].type == "C_BRACK":
                    i += 1
                    if dim():
                        return True
        return True

    def array_init():
        if tokenList[i].type == "O_BRACK":
            i += 1
            if exp():
                if tokenList[i].type == "C_BRACK":
                    i += 1
                    return True
        return syntaxError()

    def size():
        global i, tokenList
        if tokenList[i].type == "INT_CONST":
            i += 1
            return True
        return syntaxError()

    # ? **************************** dict ********************************
    def dict_():
        global i, tokenList
        if tokenList[i].type == "DICT":
            i += 1
            if tokenList[i].type == "O_BRACE":
                i += 1
                if key_value_list():
                    if tokenList[i].type == "C_BRACE":
                        i += 1
                        return True
        return syntaxError()

    def key_value_list():
        if key_value():
            if key_value_tail():
                return True
        return True

    def key_value_tail():
        global i, tokenList
        if tokenList[i].type == "COMMA":
            i += 1
            if key_value_list():
                return True
        return True

    def key_value():
        if key():
            if tokenList[i].type == "COLON":
                i += 1
                if value():
                    return True
        return syntaxError()

    def key():
        if exp():
            return True
        return syntaxError()

    def value():
        if exp():
            return True
        return syntaxError()

    # ? **************************** decleration ********************************
    def dec():
        global i, tokenList
        if tokenList[i].type == "DT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                if init():
                    if list_():
                        return True
        return syntaxError()

    def init():
        global i, tokenList
        if tokenList[i].type == "ASSIGN":
            i += 1
            if init_1():
                return True
        return True

    def init_1():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            if init_2():
                return True
        elif const():
            return True
        elif exp():
            return True
        return syntaxError()

    def init_2():
        if init_2_tail():
            return True
        return syntaxError()

    def init_2_tail():
        global i, tokenList
        if tokenList[i].type == "COMMA":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                return init_2_tail()
        return True

    def list_():
        global i, tokenList
        if tokenList[i].type == "SEMICOLON":
            i += 1
            if list_1():
                if tokenList[i].type == "COMMA":
                    i += 1
                    if tokenList[i].type == "ID":
                        i += 1
                        if init():
                            if list_():
                                return True
        return True

    def list_1():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            if init():
                if list_():
                    return True
        return True

    def const():
        global i, tokenList
        if tokenList[i].type in ["STRING", "CHAR", "FLOAT", "INT"]:
            i += 1
            return True
        return syntaxError()

    # ? **************************** assign st ********************************
    def assign_st():
        global i, tokenList
        if tokenList[i].type == "ID":
            i += 1
            if A2():
                 if tokenList[i].type == "ASSIGN":
                    i += 1
                    if exp():
                        return True
        return syntaxError()

    def A2():
        if A2_tail():
            return True
        return True

    def A2_tail():
        global i, tokenList
        if tokenList[i].type == "DOT":
            i += 1
            if tokenList[i].type == "ID":
                i += 1
                if A2():
                    return True
        elif tokenList[i].type == "O_BRACK":
            i += 1
            if exp():
                if tokenList[i].type == "C_BRACK":
                    i += 1
                    if A2():
                        return True
        elif tokenList[i].type == "O_PARAN":
            i += 1
            if PL():
                if tokenList[i].type == "C_PARAN":
                    i += 1
                    if F2():
                        return True
        return True

    def F():
        global i, tokenList
        if tokenList[i].type == "DOT":
            i += 1
            if A2():
                return True
        elif tokenList[i].type == "O_BRACK":
            i += 1
            if exp():
                if tokenList[i].type == "C_BRACK":
                    i += 1
                    if A2():
                        return True
        return True
    
    # ? **************************** increment decrement ********************************
    def inc_dec_st():
        global i, tokenList
        if tokenList[i].type == "INC_OP":
            i += 1
            if exp():
                return True
        elif tokenList[i].type == "DEC_OP":
            i += 1
            if exp():
                return True
        elif exp():
            if tokenList[i].type == "INC_OP":
                i += 1
                return True
            elif tokenList[i].type == "DEC_OP":
                i += 1
                return True
        return syntaxError()

    # ? **************************** try catch ********************************
    def try_catch():
        global i, tokenList
        if tokenList[i].type == "ATTEMPT":
            i += 1
            if tokenList[i].type == "O_BRACE":
                i += 1
                if body():
                    if tokenList[i].type == "C_BRACE":
                        i += 1
                        if catch_block():
                            if tokenList[i].type == "FINALLY":
                                i += 1
                                if tokenList[i].type == "O_BRACE":
                                    i += 1
                                    if body():
                                        if tokenList[i].type == "C_BRACE":
                                            i += 1
                                            return True
        return syntaxError()

    def catch_block():
        global i, tokenList
        if tokenList[i].type == "CATCH":
            i += 1
            if tokenList[i].type == "O_PARAN":
                i += 1
                if tokenList[i].type == "ID" and tokenList[i + 1].type == "C_PARAN":
                    i += 2
                    if tokenList[i].type == "O_BRACE":
                        i += 1
                        if body():
                            if tokenList[i].type == "C_BRACE":
                                i += 1
                                return True
        return True

    # ? **************************** expression ********************************
    def exp():
       print("exp")
       return True

except:
    print("ERROR: Syntax Analyzer: structure()")