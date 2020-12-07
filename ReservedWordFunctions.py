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
    steps = 4
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
    print("analisando output...")
    steps = 4
    outputf = False
    identificator = False
    semicolon = False
    delimiterCompound = False
   
    for i in range(0, steps):
        indice = idx + i
        # print("indice", indice)
        if i == 0 and tokenlist[indice][2] == "OUTPUT":
            # print("entrou no output")
            # print('i:; ', i, 'steps: ',steps)
            outputf = True
        if i == 1:
            # print('entrou no i=1')
            if tokenlist[indice][2] == "<-":
                # print('entrou no <-')
                delimiterCompound = True
                # i+=1
                # print('i: ', i, 'steps: ',steps)
                pass
            else:
                # print('entrou no else')
                # steps = steps - 1
                # i+=1
                # print('i: ', i, 'steps: ',steps)
                pass
        if i == 2 and tokenlist[indice][0] == "IDENTIFICADOR":
            # print('entrou no identificador')
            # print('i: ', i, 'steps: ',steps)
            identificator = True
        if i == 3 and tokenlist[indice][2] == ";":
            # print('entrou no ;')
            # print('i: ', i, 'steps: ',steps)
            semicolon = True
    # print('steps:  ',steps)
    print(outputf, delimiterCompound, identificator, semicolon)
    if outputf and delimiterCompound and identificator and semicolon:
        return True, idx + steps
    elif outputf and identificator and semicolon:
        return True, idx + steps-1
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
    functions[tokens.ReservedWords.OUTPUT] = outputf
    return functions
