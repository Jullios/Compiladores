import tokens
import re


def is_dec_valid_int(word):
    word = word.replace(" ", "")
    result = re.findall(r'[a-z]{1,}=[0-9]{1,}', word)
    if len(result) > 0:
        print("Declaração de inteiro", result[0])
        return True
    else:
        return False


def is_declaration(word):
    res = re.findall(r'^([ +]{0,}variable|array|inteiro|real)', word)
    if (len(res) > 0):
        print("Palavra reservada", res[0])
        return True, res[0]
    else:
        print("Palavra não pertence as declarações da linguagem")
        return False, None


def is_statement(word):
    res = re.findall(r'^([ ]{0,}if|else|for|while)', word)
    if (len(res) > 0):
        print("Palavra reservada", res[0])
        return True, res[0]
    else:
        print("Palavra não pertence a linguagem")
        return False, None


def is_valid_statement(word):
    word = word.replace(" ", "")
    res = re.findall(
        r'([a-zA-Z0-9]{1,}<[a-zA-Z0-9]{1,}|[a-zA-Z0-9]{1,}>[a-zA-Z0-9]{1,}|[a-zA-Z0-9]{1,}=[a-zA-Z0-9]{1,})', word)
    if len(res) > 0:
        print("Condição", res[0])
        return True
    else:
        return False


def main():
    file = open("./input.txt", "r")
    linha = 0
    for line in file:
        linha += 1
        res, word = is_declaration(line)
        if (res):
            is_dec_valid_int(line.replace(word, ""))

        else:
            res, word = is_statement(line)
            if (res):
                is_valid_statement(line.replace(word, ""))


main()
