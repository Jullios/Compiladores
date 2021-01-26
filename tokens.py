import re
import sys

# modificado .. por ,


class ReservedWords:
    TYPE = "reserved words"

    MAIN = 1
    END = 2
    TYPEDEF = 3
    AS = 4
    VARIABLE = 5
    ARRAY = 6
    OF = 7
    STRUCTURE = 8
    INTEIRO = 9
    REAL = 10
    RETURN = 11
    FUNCTION = 12
    PROCEDURE = 13
    IF = 14
    THEN = 15
    ELSE = 16
    FOR = 17
    TO = 18
    DO = 19
    BY = 20
    UNTIL = 21
    AT = 22
    WITH = 23
    WHILE = 24
    STRUCTID = 25
    REPEAT = 26
    INPUT = 27
    OUTPUT = 28
    IDENTIFICADOR = 29

    dictionary_reservedWords = {
        "MAIN": MAIN,
        "END": END,
        "TYPEDEF": TYPEDEF,
        "AS": AS,
        "VARIABLE": VARIABLE,
        "ARRAY": ARRAY,
        "OF": OF,
        "STRUCTURE": STRUCTURE,
        "INTEIRO": INTEIRO,
        "REAL": REAL,
        "RETURN": RETURN,
        "FUNCTION": FUNCTION,
        "PROCEDURE": PROCEDURE,
        "IF": IF,
        "THEN": THEN,
        "ELSE": ELSE,
        "FOR": FOR,
        "TO": TO,
        "DO": DO,
        "BY": BY,
        "UNTIL": UNTIL,
        "AT": AT,
        "WITH": WITH,
        "WHILE": WHILE,
        "STRUCTID": STRUCTID,
        "REPEAT": REPEAT,
        "INPUT": INPUT,
        "OUTPUT": OUTPUT,
        "IDENTIFICADOR": IDENTIFICADOR
    }

    variables = {
        "typedef": {},
        "inteiro": {},
        "variable": {},
        "array": {},
    }

    def check_only_one_word(self, list):
        print("checando se list é valida", list)
        return False if len(list) > 1 else True

    def return_declarations(self, list):
        pass

    def typedef_declarations(self, line):
        # print("chamando line", line)
        arr = re.findall(r'[a-z]{1,} ::= [a-zA-Z]{0,};', line)
        print("TYPEDEF ARR", arr)
        # print("arr", arr)
        if len(arr) > 0:
            arr[0] = arr[0].replace(";", "")
            sentenca = arr[0].split("::=")  # ex: a ::= node
            variavel_declarada = sentenca[0].replace(" ", "")
            variavel_recebida = sentenca[1].replace(" ", "")
            # print("declarada", variavel_declarada, "rcebida", variavel_recebida)
            typedefdeclarations = self.variables["typedef"]
            if len(variavel_recebida) == 0:
                typedefdeclarations[variavel_declarada] = ""
            else:
                w = typedefdeclarations.get(variavel_recebida)
                print("w", w)
                if w == None:
                    print("Erro ", variavel_recebida, "nao existe")
                    sys.exit()
                else:
                    typedefdeclarations[variavel_declarada] = w
        else:
            print("Erro declaração de palavra", line)
            sys.exit()
        # print("tipedefes", self.variables["typedef"])

    def inteiro_declarations(self, line):
        # print("chamando line", line)
        arr = re.findall(
            r'[a-z]{1,} ::= [a-z]{1,};|[a-z]{1,} ::= [0-9]{1,};', line)
        # print("arr", arr)
        if len(arr) > 0:
            arr[0] = arr[0].replace(";", "")
            sentenca = arr[0].split("::=")  # ex: a ::= node
            variavel_declarada = sentenca[0].replace(" ", "")
            variavel_recebida = sentenca[1].replace(" ", "")
            inteirodeclarations = self.variables["inteiro"]
            w = inteirodeclarations.get(variavel_recebida)
            if w != None:
                # tenta transformar pra numero
                inteirodeclarations[variavel_declarada] = w
            else:
                try:
                    number = int(variavel_recebida)
                    inteirodeclarations[variavel_declarada] = number
                except:
                    print("Erro ", variavel_recebida, "não é valido")
                    sys.exit()
        else:
            print("Erro declaração de palavra", line)
            sys.exit()
        print("inteirodeclarations", inteirodeclarations)

    def function_declarations(self, line):
        print("aqui", line)
        words = re.findall(r'[a-z]+|\(|\)|:', line)
        tam = len(words)
        line = line.replace(" ", "")
        nome = words[0]
        par1 = words[1]
        pt2 = words[tam - 1]
        par2 = words[tam - 2]
        c = line.find("(")
        subline = line[c:]
        # print("subline", subline)
        if par1 != "(":
            print("erro de declaração de função")
            sys.exit()
        if par2 != ")":
            print("erro de declaração de função")
            sys.exit()
        if pt2 != ":":
            print("erro de declaração de função")
            sys.exit()
        for i in range(2, tam - 2):
            # print("wi", words[i], i)
            s = words[i]
            l1 = subline.find(s)
            l = len(s)
            if i < tam - 3:
                # print("i + l", l1, l, subline[l1 + l])
                if subline[l1 + l] != ",":
                    print("erro pos ','")
                    sys.exit()
        # print("funcao correta", words)
    # def is_valid_declarations(self, word):
    #     return len(re.findall(r'variable|array|inteiro|real', word)) > 0


class Delimitators:
    TYPE = "Delimiter"

    PARLEFT = 0  # (
    PARRIGHT = 1  # )
    LESSTHEN = 2
    BIGGERTHEN = 3
    SBLEFT = 4
    SBRIGHT = 5
    SUM = 6
    COLON = 7  # :
    SEMICOLON = 8  # ;
    COMMA = 9  # ,
    OR = 10  # |
    SUB = 11  # -
    SLASH = 12  # /
    ASTRSC = 13  # *

    dictionary_delimitators = {
        "(": PARLEFT,
        ")": PARRIGHT,
        "<": LESSTHEN,
        ">": BIGGERTHEN,
        "[": SBLEFT,
        "]": SBRIGHT,
        "+": SUM,
        ":": COLON,
        ";": SEMICOLON,
        ",": COMMA,
        "|": OR,
        "-": SUB,
        "/": SLASH,
        "*": ASTRSC
    }

    def par_left_function(self):
        pass

    def par_right_function(self):
        pass

    delimitatorsFunctions = [par_left_function, par_right_function]


class CompoundDelimiters:
    TYPE = "compound delimiter"
    ASSIGNMENT = 1
    ARROW = 2
    TWOPOINTS = 3
    BIGGEREQUAL = 4
    LESSEQUAL = 5
    EQUAL = 6

    dictionary_delimiters_compound = {
        "::=": ASSIGNMENT,
        "<-": ARROW,
        "..": TWOPOINTS,
        ">=": BIGGEREQUAL,
        "<=": LESSEQUAL,
        "==": EQUAL
    }


class Tokens:
    RESERVED_WORDS = ReservedWords()
    DELIMITATORS = Delimitators()
    COMPOUND = CompoundDelimiters()

