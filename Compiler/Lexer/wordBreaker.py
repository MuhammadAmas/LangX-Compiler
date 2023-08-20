from lexer import generateToken


def breakWords(sourceCode):
    word = "am"
    line = 1
    tokenList = []
    singleBreak = [",",  ";", "(", ")", "{", "}", "[", "]",
                   "-", "+", "*", "/", "%", "=", ">", "<", "@", "!", "."]
    comboBreak = ["||", "&&", ">=", "<=", "!=",
                  "++", "--", "+=", "-=", "*=", "/=", "=="]

    i = 0
    while (i < len(sourceCode)):
        checker = sourceCode[i]

        # ! checking the next line, carriage return, tab, and space character
        if (checker == "\n" or checker == "\r" or checker == "\t" or checker == " "):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenList.append(current_token)
            else:
                i = i + 1
            line += 1
            continue

        # ! checking for dot and generating token based on the type of value
        if (sourceCode[i] == "."):
            if (word != ""):
                # If word contains only numbers then dot is a decimal
                if (word.isnumeric()):
                    word = word + sourceCode[i]
                    i = i + 1
                # If not then word and dot are separate
                else:
                    word, i, current_token = generateToken(word, line, i)
                    tokenList.append(current_token)
                    i = i - 1

            if (i < len(sourceCode)):
                # If next character of dot is a number then dot is part of next and word continues
                checking = sourceCode[i+1]
                if (sourceCode[i+1].isnumeric()):
                    word = word + sourceCode[i]
                    i = i + 1
                # If next character of dot is not a number then dot is a separate word
                else:
                    word = word + sourceCode[i]
                    word, i, current_token = generateToken(word, line, i)
                    tokenList.append(current_token)

            continue        
        

        # ! checking for string with ""
        # Checking for Starting of a String (with double quote)
        if (sourceCode[i] == "\""):
            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenList.append(current_token)
                i -= 1

            word = sourceCode[i]
            i = i + 1

            # String continues till File Ends, Next Double Quote or New Line Character
            while (i < len(sourceCode)):
                checking = sourceCode[i]
                if (i+1 < len(sourceCode)):
                    if (sourceCode[i] == "\\"):
                        checking = f"{sourceCode[i]}{sourceCode[i+1]}"
                        word = word + checking
                        i += 1
                        if (i+1 < len(sourceCode)):
                            i += 1
                            continue
                        else:
                            break

                if (sourceCode[i] != "\"" and sourceCode[i] != "\n"):
                    word = word + sourceCode[i]
                    i = i + 1
                else:
                    break

            if (sourceCode[i] == "\n"):
                line += 1

            # Breaking String if Double Quote Appear
            if (i < len(sourceCode) and sourceCode[i] == "\""):
                word = word + sourceCode[i]

            word, i, current_token = generateToken(word, line, i)
            tokenList.append(current_token)
            continue


            if (word != ""):
                word, i, current_token = generateToken(word, line, i)
                tokenist.append(current_token)
                i -= 1

            word = checker[i]
            i = i + 1

            # String continues till File Ends, Next Double Quote or New Line Character
            while (i < len(checker)):
                checking = checker[i]
                if (i+1 < len(checker)):
                    if (checker[i] == "\\"):
                        checking = f"{checker[i]}{checker[i+1]}"
                        word = word + checking
                        i += 1
                        if (i+1 < len(checker)):
                            i += 1
                            continue
                        else:
                            break

                if (checker[i] != "\"" and checker[i] != "\n"):
                    word = word + checker[i]
                    i = i + 1
                else:
                    break

            if (checker[i] == "\n"):
                line += 1

            # Breaking String if Double Quote Appear
            if (i < len(checker) and checker[i] == "\""):
                word = word + checker[i]

            word, i, current_token = generateToken(word, line, i)
            tokenList.append(current_token)
            continue

        i+=1
    return tokenList
        # TODO: check of if-else for dot, comment, string

        # int name = "amsas"
