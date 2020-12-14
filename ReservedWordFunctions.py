import tokens
import sys

functions = []
functionsend = []

def check_reserved_words_type(tokenword):
    rw = tokens.Tokens().RESERVED_WORDS
    if tokenword == rw.INTEIRO or tokenword == rw.REAL:
        return True
    else:
        return False


def typedef(tokenlist, idx):
    print("anatilsando typedef")
    steps = 5
    typedef = False
    identificator = False
    rwas = False
    rwtype = False
    semicolon = False
    for i in range(0, steps):
        indice = idx + i
        if i == 0 and tokenlist[indice][2] == "TYPEDEF":
            typedef = True
        if i == 1 and tokenlist[indice][0] == "IDENTIFICADOR":
            identificator = True
        if i == 2 and tokenlist[indice][2] == "AS":
            rwas = True
        if i == 3 and check_reserved_words_type(tokenlist[indice][1]):
            rwtype = True
        if i == 4 and tokenlist[indice][2] == ";":
            semicolon = True

    if typedef and identificator and rwas and rwtype and semicolon:
        return True, idx + steps
    else:
        return False, 0


def inputf(tokenlist, idx):
    print("analisando input")
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


def check_delimiter(word):
    delimiters = tokens.Tokens.DELIMITATORS
    comp_delimiters = tokens.Tokens.COMPOUND
    if word == delimiters.SUM or word == delimiters.SUB or word == delimiters.ASTRSC or word == delimiters.SLASH:
        return True
    else:
        return False


def identificator(tokenlist, idx):
    print("analisando identificador")
    steps = 0
    semicolon = False
    final = True
    id1 = False
    att_delimiter = False
    change = True
    while(final):
        print("passo", steps)
        indice = idx + steps
        if tokenlist[indice][2] == ";":
            semicolon = True
            final = False
            break
        if tokenlist[indice][0] == "reserved words":
            print("erro")
            final = False
            break
        if steps == 0 and tokenlist[indice][0] == "IDENTIFICADOR":
            id1 = True
        if steps == 1 and tokenlist[indice][2] == "<-":
            att_delimiter = True
        if steps > 1:
            if change and tokenlist[indice][0] == "IDENTIFICADOR":  # identificador
                change = False
            elif not change and check_delimiter(tokenlist[indice][1]):
                change = True
            else:
                print("erro")
                final = False
                break
        steps += 1
    print("aqui", semicolon, id1, att_delimiter, change)
    if semicolon and id1 and att_delimiter and not change:
        return True, idx + steps
    else:
        return False, 0


def parameters_type(word):
    rw = tokens.Tokens.RESERVED_WORDS
    if word == rw.ARRAY or word == rw.INTEIRO or word == rw.REAL or word == rw.VARIABLE:
        return True
    else:
        return False


def parametersf(tokenlist, idx):
    print("analisando parametros")
    end = True
    local = 0
    steps = 0
    while end:
        indice = idx + steps
        print("indice", indice, tokenlist[indice], local)
        if local == 0 and tokenlist[indice][0] == "IDENTIFICADOR":
            # pegar o nome do identificador
            local = 1
        elif local == 1 and tokenlist[indice][2] == ":":
            local = 2
        elif local == 2 and parameters_type(tokenlist[indice][1]) and tokenlist[indice][0] == "reserved words":
            # pegar o tipo
            print("aqui o tipo")
            local = 3
        elif local == 3 and tokenlist[indice][2] == ",":
            local = 0
        elif tokenlist[indice][2] == ")":
            end = False
            break
        else:
            end = False
            print("erro aqui")
            sys.exit(0)
        steps += 1
    print("terminou parametros, local", local)
    if local == 3 or local == 0:
        return True, steps - 1
    else:
        print("erro em parametros")
        return False, 0


def functionsf(tokenlist, idx):
    print("analisando função")
    global functionsend
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
        if i == 2 and tokenlist[indice][2] == "(":
            parleft = True
        if i == 3:
            works, jump = parametersf(tokenlist, indice)
            if works:
                parameters = True
                print("jump", jump)
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
    print(func, identificador, parleft, parameters,
          parright, colon, ftype, semicolon)
    if func and identificador and parleft and parameters and parright and colon and ftype and semicolon:
        return True, idx + steps
    else:
        return False, 0


def proceduref(tokenlist, idx):
    print("analisando procedimento")
    proc = False
    identificador = False
    parameters = False
    parleft = False
    parright = False
    steps = 5
    i = 0
    while i < steps:
        indice = idx + i
        if i == 0 and tokenlist[indice][2] == "PROCEDURE":
            proc = True
        if i == 1 and tokenlist[indice][0] == "IDENTIFICADOR":
            identificador = True
        if i == 2 and tokenlist[indice][2] == "(":
            parleft = True
        if i == 3:
            works, jump = parametersf(tokenlist, indice)
            if works:
                parameters = True
                print("jump", jump)
                idx = jump  # idx + step
            else:
                print("erro ")
                sys.exit()
        if i == 4 and tokenlist[indice][2] == ")":
            parright = True
        i = i + 1

    print(proc, identificador, parleft, parameters, parright)
    if proc and identificador and parameters and parleft and parright:
        return True, idx + steps
    else:
        print("erro procedure")
        return False, 0


def run():
    global functions
    functions = [0] * 30
    functions[tokens.ReservedWords.TYPEDEF] = typedef
    functions[tokens.ReservedWords.INPUT] = inputf
    functions[tokens.ReservedWords.IDENTIFICADOR] = identificator
    functions[tokens.ReservedWords.FUNCTION] = functionsf
    functions[tokens.ReservedWords.PROCEDURE] = proceduref
    return functions
