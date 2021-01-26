import ReservedWordFunctions as rwfunctions
import sys

tokenlist = []


def reserved_words(item, idx):
    token = item[1]
    functionslist = rwfunctions.run()

    if functionslist[token] == 0:
        return idx + 1

    works, nextidx = functionslist[token](tokenlist, idx)
    # print("works nextid", works, nextidx)
    if works:
        # print("tudo certo", nextidx)
        return nextidx
    else:
        print("erro em ", tokenlist[idx], "indice pilha ", idx)
        sys.exit(0)


def token_resolver(item, idx):
    # print("token r", item[0])
    if item[0] == "reserved words":
        return reserved_words(item, idx)
    if item[0] == "IDENTIFICADOR":
        return reserved_words(item, idx)
    else:
        return idx + 1


def run(tokens):
    global tokenlist
    tokenlist = tokens
    tokenslen = len(tokens)
    i = 0
    while i < tokenslen:
        item = tokens[i]
        if len(item) == 3:
            i = token_resolver(item, i)
    print("análise sintatica finalizada com sucesso")
