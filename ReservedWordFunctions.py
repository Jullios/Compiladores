import tokens
import sys

import re
functions = []
functionsend = []
scoped_list = []

lexic_table = []

variables = {}


def check_reserved_words_type(tokenword):
    rw = tokens.Tokens().RESERVED_WORDS
    if tokenword == rw.INTEIRO or tokenword == rw.REAL:
        return True
    else:
        return False


def findscope():
    global scoped_list
    if len(scoped_list) > 1:
        return "local"
    else:
        return "global"


def typedef(tokenlist, idx):
    steps = 5
    typedef = False
    identificator = False
    rwas = False
    rwtype = False
    semicolon = False
    global lexic_table
    variable = ["", "", "", "", "", ""]
    for i in range(0, steps):
        indice = idx + i
        if i == 0 and tokenlist[indice][2] == "TYPEDEF":
            typedef = True
        if i == 1 and tokenlist[indice][0] == "IDENTIFICADOR":
            identificator = True
            variable[0] = tokenlist[indice][2]
            variable[1] = "IDENTIFICADOR"
            variable[2] = "VARIAVEL"
        if i == 2 and tokenlist[indice][2] == "AS":
            rwas = True
        if i == 3 and check_reserved_words_type(tokenlist[indice][1]):
            variable[3] = "INTEIRO"
            rwtype = True
        if i == 4 and tokenlist[indice][2] == ";":
            semicolon = True

    if typedef and identificator and rwas and rwtype and semicolon:
        variable[5] = findscope()
        lexic_table.append(variable)
        return True, idx + steps
    else:
        return False, 0


def inputf(tokenlist, idx):
    steps = 3
    inputf = False
    identificator = False
    semicolon = False
    for i in range(0, steps):
        indice = idx + i
        if i == 0 and tokenlist[indice][2] == "INPUT":
            inputf = True
        if i == 1 and tokenlist[indice][0] == "IDENTIFICADOR":
            identificator = True
        if i == 2 and tokenlist[indice][2] == ";":
            semicolon = True

    if inputf and identificator and semicolon:
        return True, idx + steps
    else:
        return False, 0


def outputf(tokenlist, idx):
    steps = 3
    outputf = False
    identificator = False
    semicolon = False
    delimiterCompound = False

    for i in range(0, steps):
        indice = idx + i
        if i == 0 and tokenlist[indice][2] == "OUTPUT":
            outputf = True
        elif i == 1 and tokenlist[indice][2] == "<-":
            delimiterCompound = True
        else:
            end = True
            cnt = 0
            ex = 0
            exp = []
            while(end):
                index = indice + cnt
                if tokenlist[index][2] == ";":
                    end = False
                    semicolon = True
                    steps = steps + cnt
                elif ex == 0 and tokenlist[index][0] == "IDENTIFICADOR":
                    exp.append(tokenlist[index][2])
                    ex = 1
                    identificator = True
                elif ex == 1 and check_delimiter(tokenlist[index][1]):
                    exp.append(tokenlist[index][2])
                    ex = 0
                else:
                    print("erro em output", index)
                    sys.exit(0)
                cnt += 1
    if outputf and delimiterCompound and identificator and semicolon:
        return True, idx + steps
    else:
        return False, 0


def variable(tokenlist, idx):
    steps = 5
    variablef = False
    nameVariable = False
    identificator = False
    semicolon = False
    reservedWords = False

    for i in range(0, steps):
        indice = idx + i
        if i == 0 and tokenlist[indice][2] == "VARIABLE":
            variablef = True
        if i == 1 and tokenlist[indice][0] == "IDENTIFICADOR":
            verify = any(char.isdigit() for char in tokenlist[indice][2])
            if verify == True:
                a = 0
                for i in tokenlist[indice][2]:
                    if i.isdigit():
                        if a == 0:
                            nameVariable = False
                            break
                        else:
                            nameVariable = True
                    else:
                        pass
                    a += 1
            else:
                nameVariable = True
        if i == 2 and tokenlist[indice][2] == ":":
            identificator = True
        if i == 3 and (tokenlist[indice][2] == "INTEIRO" or tokenlist[indice][2] == "REAL"):
            reservedWords = True
        if i == 4 and tokenlist[indice][2] == ";":
            semicolon = True
    if variablef and nameVariable and identificator and reservedWords and semicolon:
        return True, idx + steps
    else:
        return False, 0


def check_delimiter(word):
    delimiters = tokens.Tokens.DELIMITATORS
    comp_delimiters = tokens.Tokens.COMPOUND
    if word == delimiters.SUM or word == delimiters.SUB or word == delimiters.ASTRSC or word == delimiters.SLASH:
        return True
    else:
        return False


def checkvalue(val):
    global variables
    r = variables.get(val)
    if r != None:
        return r
    else:
        return int(val)


# def setvariablevalue(val, list):
#     global variables
#     h = variables.get(val)
#     if h != None:
#         print("ERRO: variavel ", val, "duplicada")
#         sys.exit()
#     else:
#         if len(list) == 1:
#             variables[val] = checkvalue(list[0])
#         else:
#             val = 0
#             for i in range(0, len(list)):
#                 for i in range(0, len(list)):
#                     if list[i] == "*":
#                         a = checkvalue(list[i - 1])
#                         b = checkvalue(list[i + 1])
#                         variables[val] = multiplication(a, b)
#                         list.pop(i + 1)
#                         list.pop(i - 1)
#                     elif list[i] == "/":
#                         pass
#                     elif list[i] == "+":
#                         pass
#                     elif list[i] == "-":
#                         pass


def identificator(tokenlist, idx):
    # print("identificador")
    steps = 0
    semicolon = False
    final = True
    id1 = False
    att_delimiter = False
    change = True
    result = ""
    # result = []
    idt = ""
    findword = False
    while(final):
        indice = idx + steps
        if tokenlist[indice][2] == ";":
            semicolon = True
            final = False
            break
        if tokenlist[indice][0] == "reserved words":
            final = False
            break
        if steps == 0 and tokenlist[indice][0] == "IDENTIFICADOR":
            id1 = True
            idt = tokenlist[indice][2]
        if steps == 1 and tokenlist[indice][2] == "<-":
            att_delimiter = True
        if steps > 1:
            if change and tokenlist[indice][0] == "IDENTIFICADOR":  # identificador
                change = False
                result += tokenlist[indice][2]
            elif not change and check_delimiter(tokenlist[indice][1]):
                change = True
                result += tokenlist[indice][2]
            else:
                print("erro")
                final = False
                break
        steps += 1
    global lexic_table
    rowslen = len(lexic_table)
    i = 0
    for i in range(0, rowslen):
        if lexic_table[i][0] == idt:
            if lexic_table[i][1] == "identificador" and lexic_table[i][3] == "inteiro":
                lexic_table[i][4] = result
                findword = True
    findword = True
    # setvariablevalue(idt, result)
    if semicolon and id1 and att_delimiter and not change and findword == True:
        return True, idx + steps
    else:
        return False, 0

# def identificatorf()


def parameters_type(word):
    rw = tokens.Tokens.RESERVED_WORDS
    if word == rw.ARRAY or word == rw.INTEIRO or word == rw.REAL or word == rw.VARIABLE:
        return True
    else:
        return False


def parametersf(tokenlist, idx):
    end = True
    local = 0
    steps = 0
    while end:
        indice = idx + steps
        if local == 0 and tokenlist[indice][0] == "IDENTIFICADOR":
            # pegar o nome do identificador
            local = 1
        elif local == 1 and tokenlist[indice][2] == ":":
            local = 2
        elif local == 2 and parameters_type(tokenlist[indice][1]) and tokenlist[indice][0] == "reserved words":
            # pegar o tipo
            local = 3
        elif local == 3 and tokenlist[indice][2] == ",":
            local = 0
        elif tokenlist[indice][2] == ")":
            end = False
            break
        else:
            end = False
            print("erro em parametros 1")
            sys.exit(0)
        steps += 1
    if local == 3 or local == 0:
        return True, steps - 1
    else:
        print("erro em parametros")
        return False, 0


def functionsf(tokenlist, idx):
    global functionsend
    global scoped_list
    steps = 8
    func = False
    identificador = False
    parleft = False
    parright = False
    parameters = False
    colon = False
    ftype = False
    semicolon = False
    i = 0
    while i < steps:
        indice = idx + i
        # print("indice", indice)
        if i == 0 and tokenlist[indice][2] == "FUNCTION":
            func = True
            functionsend.append("open")
        if i == 1 and tokenlist[indice][0] == "IDENTIFICADOR":
            identificador = True
            functionname = "function=" + tokenlist[indice][2]
            scoped_list.append(functionname)
        if i == 2 and tokenlist[indice][2] == "(":
            parleft = True
        if i == 3:
            works, jump = parametersf(tokenlist, indice)
            if works:
                parameters = True
                idx = jump  # idx + step
            else:
                print("erro ")
                sys.exit()
        if i == 4 and tokenlist[indice][2] == ")":
            parright = True
        if i == 5 and tokenlist[indice][2] == ":":
            colon = True
        if i == 6 and check_reserved_words_type(tokenlist[indice][1]):
            # get function type
            ftype = True
        if i == 7 and tokenlist[indice][2] == ";":
            semicolon = True
        i = i + 1
    # print(func, identificador, parleft, parameters,
    #       parright, colon, ftype, semicolon)
    if func and identificador and parleft and parameters and parright and colon and ftype and semicolon:
        return True, idx + steps
    else:
        return False, 0


def proceduref(tokenlist, idx):
    global scoped_list
    global lexic_table
    proc = False
    identificador = False
    parameters = False
    parleft = False
    parright = False
    steps = 5
    i = 0
    vlist = ["", "", "", "", "", ""]
    while i < steps:
        indice = idx
        # indice = idx + i
        if i == 0 and tokenlist[indice][2] == "PROCEDURE":
            proc = True
        if i == 1 and tokenlist[indice][0] == "IDENTIFICADOR":
            identificador = True
            functionname = "function=" + tokenlist[indice][2]
            scoped_list.append(functionname)
            vlist[0] = tokenlist[indice][2]
            vlist[1] = "IDENTIFICADOR"
            vlist[2] = "PROCEDURE"
            vlist[3] = "NULL"
        if i == 2 and tokenlist[indice][2] == "(":
            parleft = True
        if i == 3:
            works, jump = parametersf(tokenlist, indice)
            if works:
                parameters = True
                # idx = jump  # idx + step
                idx += jump  # idx + step
            else:
                print("erro em procedimento")
                sys.exit()
        if i == 4 and tokenlist[indice][2] == ")":
            parright = True
        idx += 1
        i = i + 1

    if proc and identificador and parameters and parleft and parright:
        lexic_table.append(vlist)
        return True, idx
        # return True, idx + steps
    else:
        print("erro procedure")
        return False, 0


def conditionals(con):
    conditionalss = {
        "<=": 1,
        ">=": 2,
        "==": 3,
        "<": 4,
        ">": 5
    }
    if conditionalss.get(con):
        return True
    else:
        return False


def returnf(tokenlist, idx):
    returname = False
    end = True
    steps = 0
    ex0 = 0
    exp1 = []
    while end:
        indice = idx + steps
        if steps == 0 and tokenlist[indice][2] == "RETURN":
            returname = True
        elif tokenlist[indice][2] == ";":
            end = False
        elif tokenlist[indice][0] == "IDENTIFICADOR" or tokenlist[indice][0] == "Delimiter":
            if ex0 == 0 and tokenlist[indice][0] == "IDENTIFICADOR":
                exp1.append(tokenlist[indice][2])
                ex0 = 1
            elif ex0 == 1 and check_delimiter(tokenlist[indice][1]):
                exp1.append(tokenlist[indice][2])
                ex0 = 0
            else:
                print("erro sintatico em return de função")
                sys.exit(0)
        steps += 1
    if returname == True and ex0 == 1:
        return True, idx + steps
    else:
        print("erro sintatico no comando return")
        return False, 0


def whilef(tokenlist, idx):
    whileval = False
    do = False
    end = False
    steps = 2
    indice = idx
    global scoped_list
    for i in range(0, 3):
        # indice = idx + i
        if i == 0 and tokenlist[indice][2] == "WHILE":
            whileval = True
            indice = + 1
            functionname = "while=" + tokenlist[indice][2]
            scoped_list.append(functionname)
        elif i == 1:
            res, pos = conditionf(tokenlist, idx + i)
            if res:
                indice = pos
                idx = pos - i
            else:
                print("erro em condicional")
                sys.exit()
        # print("indice", indice)
        elif i == 2 and tokenlist[indice][2] == "DO":
            do = True
            for j in range(indice, len(tokenlist)):
                if tokenlist[j][2] == "END":
                    end = True
                    break

    if whileval == True and do == True and end == True:
        return True, idx + steps
    else:
        return False


def conditionf(tokenlist, idx):
    parleft = False
    parright = False
    end = True
    do = False
    condition = False
    steps = 0
    exp1 = []
    exp2 = []
    ex0 = 0
    ex1 = 0
    while end:
        indice = idx + steps
        if tokenlist[indice][2] == ")":
            parleft = True
            end = False
        # elif tokenlist[indice][2] == "DO":
        #     do = True
        #     end = False
        elif tokenlist[indice][2] == "(":
            parright = True
        elif conditionals(tokenlist[indice][2]):
            condition = True
        elif tokenlist[indice][2] == ";" or tokenlist[indice][2] == "END":
            print("erro em condição")
            sys.exit(0)
        # elif tokenlist[indice][2] == "WHILE":
        #     steps += 1
        #     continue
        else:
            if tokenlist[indice][0] == "IDENTIFICADOR" or tokenlist[indice][0] == "Delimiter" or tokenlist[indice][0] == "compound delimiter":
                if condition == False:
                    if ex0 == 0 and tokenlist[indice][0] == "IDENTIFICADOR":
                        exp1.append(tokenlist[indice][2])
                        ex0 = 1
                    elif ex0 == 1 and check_delimiter(tokenlist[indice][1]):
                        exp1.append(tokenlist[indice][2])
                        ex0 = 0
                    else:
                        print("erro aqui em condição 2")
                        sys.exit(0)
                else:
                    if ex1 == 0 and tokenlist[indice][0] == "IDENTIFICADOR":
                        exp2.append(tokenlist[indice][2])
                        ex1 = 1
                    elif ex1 == 1 and check_delimiter(tokenlist[indice][1]):
                        exp2.append(tokenlist[indice][2])
                        ex1 = 0
                    else:
                        print("erro em condição 3")
                        sys.exit(0)
            else:
                print("erro em condição")
                sys.exit(0)
        steps += 1

    if parleft == True and parright == True and condition == True:
        return True, idx + steps
    else:
        print("erro em condicional")
        return False, 0


def iff(tokenlist, idx):
    ifval = False
    thenval = False
    end = False
    elseval = False
    steps = 2
    indice = idx
    for i in range(0, 3):
        # indice = idx + i
        if i == 0 and tokenlist[indice][2] == "IF":
            ifval = True
            indice += 1
            global scoped_list
            scoped_list.append("IF")
        elif i == 1:
            con, pos = conditionf(tokenlist, idx + i)
            if not con:
                print("if erro em condicional")
                sys.exit()
            else:
                idx = pos - i
                indice = pos
        elif i == 2 and tokenlist[indice][2] == "THEN":
            thenval = True
            indice += 1
            for j in range(indice, len(tokenlist)):
                if tokenlist[j][2] == "END":
                    end = True
                    # steps = 3
                    break
                if tokenlist[j][2] == "ELSE":
                    indice += 1
                    # steps = 3
                    for l in range(0, len(tokenlist)):
                        if tokenlist[l][2] == "END":
                            end = True
                            break
    if ifval == True and thenval == True and end == True:
        return True, idx + steps
    else:
        return False, 0


def endf(tokenlist, idx):
    global scoped_list
    # print("tokenlist, idx, scoped list", tokenlist[idx], idx, scoped_list)
    if len(scoped_list) == 0:
        print("erro palavra 'END' faltando")
        sys.exit()
    else:
        print("saindo do escopo", scoped_list.pop(-1))
        return True, idx + 1


def mainf(tokenlist, idx):
    global scoped_list
    for i in scoped_list:
        if i == "MAIN":
            print("Erro: função main já declarada")
            sys.exit()
    # print("adicionando escopo main")
    scoped_list.append("MAIN")
    return True, idx + 1


def run():
    global lexic_table
    lexic_table.append(
        ["LEXEMA", "TOKEN", "CATEGORIA", "TIPO", "VALOR", "ESCOPO"]
    )
    global functions
    functions = [0] * 30
    functions[tokens.ReservedWords.TYPEDEF] = typedef
    functions[tokens.ReservedWords.INPUT] = inputf
    functions[tokens.ReservedWords.IDENTIFICADOR] = identificator
    functions[tokens.ReservedWords.FUNCTION] = functionsf
    functions[tokens.ReservedWords.PROCEDURE] = proceduref
    functions[tokens.ReservedWords.OUTPUT] = outputf
    functions[tokens.ReservedWords.VARIABLE] = variable
    functions[tokens.ReservedWords.WHILE] = whilef
    functions[tokens.ReservedWords.IF] = iff
    functions[tokens.ReservedWords.MAIN] = mainf
    functions[tokens.ReservedWords.END] = endf
    functions[tokens.ReservedWords.RETURN] = returnf
    return functions
