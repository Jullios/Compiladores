import re


class ReservedWords:
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

    def is_valid_declarations(self, word):
        return len(re.findall(r'variable|array|inteiro|real', word)) > 0


class Delimitators:
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
        ")": PARRIGHT
    }

    def par_left_function(self):
        pass

    def par_right_function(self):
        pass

    delimitatorsFunctions = [par_left_function, par_right_function]


class Tokens:
    RESERVED_WORDS = ReservedWords()
    DELIMITATORS = Delimitators()
