import tokens

functions = []


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


def run():
    global functions
    functions = [0] * 30
    functions[tokens.ReservedWords.TYPEDEF] = typedef
    functions[tokens.ReservedWords.INPUT] = inputf
    functions[tokens.ReservedWords.IDENTIFICADOR] = identificator
    return functions
