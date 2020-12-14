
# from sintatico.teste import Teste
import fileinput
import tokens
import re
import sys

# sys.path.append('..\sintatico')


alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
            'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

valid_characters = [0] * 256

reservedwords = tokens.Tokens().RESERVED_WORDS
compouddelimiters = tokens.Tokens().COMPOUND
delimitators = tokens.Tokens().DELIMITATORS


tokenlist = []

variables = {}


def is_valid_character(character):
    return True if valid_characters[ord(character)] == 1 else False


def get_reserved_token(word):
    w = reservedwords.dictionary_reservedWords.get(word)
    if w == None:
        return -1
    else:
        return w


def get_variable_type(word):
    variables = reservedwords.variables
    w = variables["typedef"].get(word)
    if w != None:
        return reservedwords.dictionary_reservedWords["typedef"]
    w = variables["inteiro"].get(word)
    if w != None:
        return reservedwords.dictionary_reservedWords["inteiro"]


def readline(line, list):
    f = False
    w = []
    word = ""
    for i in range(0, len(line)):
        if line[i] == " " and f == False:
            continue
        if is_valid_character(line[i]):
            w.append(line[i])
            f = True
        else:
            word = "".join(w)
            print("palavra", word)
            token = get_reserved_token(word)
            print("token", token)
            if token != -1:
                rline = line.replace(word, "")
                if token == 1:
                    # main
                    continue
                if token == 2:
                    # end
                    continue
                if token == 3:
                    reservedwords.typedef_declarations(rline)
                    break
                elif token == 9:
                    reservedwords.inteiro_declarations(rline)
                    break
                elif token == 11:
                    reservedwords.return_declarations(rline)
                    break
                elif token == 12:
                    reservedwords.function_declarations(rline)
                    break
                else:
                    print("erro de declaração, token n encontrado")
                    sys.exit()
                    return
            else:
                token = get_variable_type(word)
                if token == 9:
                    print("variavel do tipo inteiro")
                    checking_operation(list)
                    break
                elif token == 3:
                    print("variavel do tipo typedef")
                    break


def is_valid_identificator():
    pass


def findTokens(list):

    rw = reservedwords.dictionary_reservedWords
    cdelimiters = compouddelimiters.dictionary_delimiters_compound
    dl = delimitators.dictionary_delimitators

    for item in list:
        w = rw.get(item)
        if w != None:
            tokenlist.append([reservedwords.TYPE, w, item])
            continue
        w = cdelimiters.get(item)
        if w != None:
            tokenlist.append([compouddelimiters.TYPE, w, item])
            continue
        w = dl.get(item)
        if w != None:
            tokenlist.append([delimitators.TYPE, w, item])
            continue
        # is valid identificator
        tokenlist.append(["IDENTIFICADOR", reservedwords.IDENTIFICADOR, item])
        variables[item] = True


def checking_operation(list):
    print("list", list)
    # a :== c +-*/ b -*/+ d ...
    # rw = reservedwords.dictionary_reservedWords
    # cdelimiters = compouddelimiters.dictionary_delimiters_compound
    dl = delimitators.dictionary_delimitators

    point = 0
    for i in range(0, len(list)):
        if i == 0:
            if variables.get(list[i]):
                continue
            else:
                print("Erro - 1")
                sys.exit()
        if i == 1:
            if list[i] == "::=":
                continue
            else:
                print("Erro 0")
                sys.exit()

        if point == 0:
            w = variables.get(list[i])
            if w != None:
                point = 1
                continue
            else:
                try:
                    number = int(list[i])
                    point = 1
                    continue
                except:
                    print("sequencia invalida 1")
                    break

        elif point == 1:
            print("list i", list[i])
            w = dl.get(list[i])
            print("w", w)
            if w == 6 or w == 11 or w == 13 or w == 12:
                point = 0
                continue
            elif w == 8:
                break
            else:
                print("Sequencia invalida 2")
                sys.exit()
                break
        if i == len(list) - 1:
            if list[len(list) - 1] != ";":
                print("Erro expected ;")
    if point == 0:
        print("Sequencia invalida 3")
        sys.exit()
    else:
        print("Sequencia válida")


def end():
    main = tokenlist[0]
    if main[1] != reservedwords.MAIN:
        print("Erro de sequencia")
        sys.exit()
    l = len(tokenlist)
    end = tokenlist[l - 1]
    if end[1] != reservedwords.END:
        print("Erro de sequencia")
        sys.exit()


def get_tokens():
    for i in alphabet:
        valid_characters[ord(i)] = 1
    for i in numbers:
        valid_characters[ord(i)] = 1

    file = open("./input.txt", "r")
    for line in file:
        if line == "\n":
            continue
        l = re.findall(
            r'[A-Z0-9]+|[0-9]{1,}|::=|<-|\+|-|\*|\/|;|\*|<=|<|>=|>|<|\(|\)|==|[|]|:|,', line)
        # print("l", l)
        findTokens(l)
        # readline(line, l)
    # print("tokenlist", tokenlist)
    # end()
    for item in tokenlist:
        print(item)

    return tokenlist
