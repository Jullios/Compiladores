import re
import sys
tabela = []
functionsline = {}
escope = {}
currentescope = 0
lines = []
jump = 0
executions = {}
executionstack = []


def initializefunctions():
    global functionsline
    global executions
    file = open("./input.txt", "r")
    cnt = 0
    for line in file:
        if line == "\n":
            continue
        l = re.findall(
            r'[A-Z0-9]+|[0-9]{1,}|::=|<-|\+|-|\*|\/|;|\*|<=|<|>=|>|<|\(|\)|==|[|]|:|,', line)

        i = 0
        for i in range(0, len(l)):
            if l[i] == "MAIN":
                functionsline["MAIN"] = cnt
                break
            if l[i] == "PROCEDURE":
                functionsline[l[i + 1]] = cnt
                break
        cnt += 1

    # print("functionslines", functionsline)

    global lines
    file = open("./input.txt", "r")
    lines = file.readlines()

    i = len(lines) - 1
    while i >= 0:
        if lines[i] == "\n":
            lines.pop(i)
        i -= 1

    executionstack = []
    for i in range(0, len(lines)):
        l = re.findall(
            r'[A-Z0-9]+|[0-9]{1,}|::=|<-|\+|-|\*|\/|;|\*|<=|<|>=|>|<|\(|\)|==|[|]|:|,', lines[i])
        # print("linha", i, l)
        if l[0] == "MAIN":
            executionstack.append({
                "TYPE": "MAIN",
                "IDX": i,
            })
        if l[0] == "PROCEDURE":
            executionstack.append({
                "TYPE": "PROCEDURE",
                "IDX": i,
            })
        if l[0] == "WHILE":
            # print("ENCONTRA WHILE?")
            executionstack.append({
                "TYPE": "WHILE",
                "IDX": i,
            })
        if l[0] == "IF":
            executionstack.append({
                "TYPE": "IF",
                "IDX": i,
            })
        if l[0] == "ELSE":
            # ii = len(executionstack)
            executionstack[-1]["ELSE"] = i
        if l[0] == "END":
            ii = len(executionstack)
            # print("exe stack", executionstack)
            # print("indice", ii)
            executionstack[-1]["END"] = i
            a = executionstack.pop()
            executions[a["IDX"]] = a

    # print("STACK", executionstack)
    # print("EXEC ", executions)


def inputf(list):
    # INPUT Z;
    global escope
    global currentescope
    variablename = list[1]
    val = escope[currentescope].get(variablename)
    if val:
        valtype = val.get("TYPE")
        v = input(variablename + ":")
        if valtype == "INTEIRO":
            try:
                value = int(v)
                val["VALUE"] = value
            except:
                print("Erro de execução: Entrada inválida")
                sys.exit()
    else:
        print("Erro semantico: variável", variablename, "não declarada")


def outputf(list):
    global tabela
    global currentescope
    global escope
    # print("output curr escopo", currentescope, escope[currentescope])
    variablename = list[2]
    variable = escope[currentescope].get(variablename)
    if variable:
        if variable["TYPE"] == "PROCEDURE":
            pass
        else:
            print(variable["VALUE"])
    else:
        print("Erro de execução: variável", variablename, "não declarada")
        sys.exit()


def division(a, b):
    if b != 0:
        return a / b
    else:
        print("divisao por 0 encontrada")
        sys.exit()


def multiplication(a, b):
    return a * b


def sumfunction(a, b):
    return a + b


def subtration(a, b):
    return a - b


def calculate(list):
    # print("calulate list", list)
    global currentescope
    global escope
    l = len(list)
    if l <= 1:
        variablename = list[0]
        if escope[currentescope].get(variablename):
            list[0] = escope[currentescope].get(variablename)
        else:
            try:
                a = list[0]
                # list[0] = {
                #     "VALUE": int(a)
                # }
                list[0] = int(a)
            except:
                print("Erro de execução: formato inválido em:", a)
    else:
        l = l - 1
        while l >= 0:
            if list[l] == '*':
                a = list[l - 1]
                b = list[l + 1]

                if escope[currentescope].get(a):
                    a = escope[currentescope][a]["VALUE"]
                    # print("a", a)
                else:
                    try:
                        a = int(a)
                        # print("a", a)
                    except:
                        print("valor inválido como inteiro")
                        sys.exit()

                if escope[currentescope].get(b):
                    b = escope[currentescope][b]["VALUE"]
                    # print("b", b)
                else:
                    try:
                        b = int(b)
                        # print("b", b)
                    except:
                        print("valor inválido como inteiro")
                        sys.exit()
                list[l] = multiplication(a, b)
                list.pop(l + 1)
                list.pop(l - 1)
                l = l - 1
            if list[l] == "/":
                a = list[l - 1]
                b = list[l + 1]
                if escope[currentescope].get(a):
                    a = escope[currentescope][a]["VALUE"]
                else:
                    try:
                        a = int(a)
                    except:
                        print("valor inválido como inteiro")
                        sys.exit()

                if escope[currentescope].get(b):
                    b = escope[currentescope][b]["VALUE"]
                else:
                    try:
                        b = int(b)
                    except:
                        print("valor inválido como inteiro")
                        sys.exit()
                list[l] = division(a, b)
                list.pop(l + 1)
                list.pop(l - 1)
            l = l - 1

        l = len(list) - 1
        while l >= 0:
            if list[l] == '+':
                a = list[l - 1]
                b = list[l + 1]
                if escope[currentescope].get(a):
                    a = escope[currentescope][a]["VALUE"]
                    # a = escope[currentescope].get(a)
                else:
                    try:
                        a = int(a)
                    except:
                        print("valor inválido como inteiro")
                        sys.exit()

                if escope[currentescope].get(b):
                    b = escope[currentescope][b]["VALUE"]
                else:
                    try:
                        b = int(b)
                    except:
                        print("valor inválido como inteiro")
                        sys.exit()
                list[l] = sumfunction(a, b)
                list.pop(l + 1)
                list.pop(l - 1)
                l = l - 1
            if list[l] == "-":
                a = list[l - 1]
                b = list[l + 1]
                if escope[currentescope].get(a):
                    a = escope[currentescope][a]["VALUE"]
                else:
                    try:
                        a = int(a)
                    except:
                        print("valor inválido como inteiro")
                        sys.exit()

                if escope[currentescope].get(b):
                    b = escope[currentescope][b]["VALUE"]
                else:
                    try:
                        b = int(b)
                    except:
                        print("valor inválido como inteiro")
                        sys.exit()
                list[l] = subtration(a, b)
                list.pop(l + 1)
                list.pop(l - 1)
            l = l - 1
    # print("list antes de retornar", list)
    return list


def variable(list):
    global currentescope
    global escope
    # print("variable ll", list)
    variablename = list[0]
    variable = escope[currentescope].get(variablename)
    if variable:
        if variable["TYPE"] == "PROCEDURE":
            pass
        else:
            list.pop(0)
            list.pop(0)
            l = len(list)
            list.pop(l - 1)
            a = calculate(list)
            variable["VALUE"] = a[0]
    else:
        print("Erro de execução: variável", variablename, "não declarada")
        sys.exit()


def condition(list):
    conditions = {
        "==": "IGUAL",
        "<=": "MENORIGUAL",
        ">=": "MAIORIGUAL",
        ">": "MAIOR",
        "<": "MENOR"
    }
    arr1 = []
    arr2 = []
    conditional = 0
    for i in range(0, len(list)):
        if conditions.get(list[i]):
            for j in range(0, i):
                arr1.append(list[j])
            for j in range(i + 1, len(list)):
                arr2.append(list[j])
            conditional = list[i]
            break
    # print("arr2", arr2)
    r1 = calculate(arr1)[0]
    r2 = calculate(arr2)[0]
    if type(r1) is dict:
        r1 = r1["VALUE"]
    if type(r2) is dict:
        r2 = r2["VALUE"]
    if conditional == "==":
        if r1 == r2:
            return True
    if conditional == "<=":
        if r1 <= r2:
            return True
    if conditional == ">=":
        if r1 >= r2:
            return True
    if conditional == ">":
        if r1 > r2:
            return True
    if conditional == "<":
        if r1 < r2:
            return True
    return False


def whilef(list):
    global escope
    global currentescope
    global canread
    global executions
    global executionstack
    global jump
    listlen = len(list)
    list.pop(listlen - 1)
    list.pop(0)
    list.pop(0)
    current = executions.get(jump)
    if condition(list):
        idx = jump
        # print("entra em condition?")
        executionstack.append(current)
        while(condition(list)):
            reader(idx + 1)

    jump = current["END"] + 1
    # print("while jump", jump)
    executionstack.pop()
    return jump


def iff(list):
    global escope
    global currentescope
    global canread
    global executions
    global executionstack
    global jump
    listlen = len(list)
    list.pop(listlen - 1)
    list.pop(0)
    list.pop(0)
    current = executions.get(jump)
    idx = 0
    if condition(list):
        idx = jump
        executionstack.append(current)
        reader(idx + 1)
    elif current["ELSE"]:
        idx = current["ELSE"]
        executionstack.append(current)
        reader(idx + 1)
    jump = current["END"] + 1
    # print("while jump", jump)
    executionstack.pop()
    return jump


def procedureexecute(list):
    global escope
    global currentescope
    global canread
    global executions
    global executionstack
    global functionsline
    global jump
    # print("linha do procedimento", list)
    # list.pop(-1)
    # list.pop(0)
    # list.pop(0)
    # list.pop(0)
    parameters = []
    for i in range(2, len(list)):
        if list[i] == ":":
            continue
        elif list[i] == "INTEIRO":
            continue
        elif list[i] == "(":
            continue
        elif list[i] == ")":
            continue
        else:
            parameters.append([
                "",
                list[i]
            ])
    # current = executions.get()
    # print("executions", executions)
    current = executions.get(currentescope)
    # print("current", current)
    param = current["PARAMETERS"]
    # print("LEN PARAMT", len(parameters))
    # print("param", param)
    for i in range(0, len(parameters)):
        typedef_createvariable(parameters[i])
        ll = [
            parameters[i][1],  # nome da variavel
            "<-",
            param[i],
            ";"
        ]
        variable(ll)

    # print("escopo", escope)


def functionf(list):
    global escope
    global currentescope
    global canread
    global executions
    global executionstack
    global functionsline
    global jump
    # listlen = len(list)
    idx = jump
    cscope = currentescope
    # print("lista ", list)
    list.pop(-1)
    list.pop(-1)
    functioname = list.pop(0)
    list.pop(0)
    list2 = []
    currescope = escope[currentescope]
    # print("current escopo", currescope)
    for i in list:
        if currescope[i]:
            list2.append(currescope[i]["VALUE"])
        else:
            list2.append(int(i))
    # print("parametros", list)
    # print("parametros 2", list2)
    # print("fun name", functioname)
    nextscope = functionsline[functioname]
    addescope(nextscope)
    current = executions.get(nextscope)
    current["PARAMETERS"] = list2
    reader(nextscope)
    # print("RETORNOU PARA FUNC F")
    currentescope = cscope
    return idx + 1


def typedef_createvariable(list):
    # print("typedef create val", list)
    global tabela
    global escope
    global currentescope
    variablename = list[1]
    # tabela_tamanho = len(tabela)
    # find = False
    # valuetype = ""
    value = None
    # for i in range(0, tabela_tamanho):
    #     if tabela[i][0] == variablename:
    #         valuetype = tabela[i][3]
    #         value = None
    #         find = True
    #         break

    # if find:
    #     escope[currentescope][variablename] = {
    #         "NAME": variablename,
    #         "TYPE": valuetype,
    #         "VALUE": value
    #     }
    escope[currentescope][variablename] = {
        "NAME": variablename,
        "TYPE": "INTEIRO",
        "VALUE": value
    }


def addescope(idx):
    global escope
    global currentescope
    currentescope = idx
    escope[currentescope] = {}


def reader(idx):
    global lines
    global canread
    # global endignore
    global escope
    global currentescope
    global jump
    global functionsline
    jump = idx
    lineslen = len(lines)
    # for jump in range(idx, lineslen):
    while jump < lineslen:
        l = re.findall(
            r'[A-Z0-9]+|[0-9]{1,}|::=|<-|\+|-|\*|\/|;|\*|<=|<|>=|>|<|\(|\)|==|[|]|:|,', lines[jump])
        print("Escopo", escope)
        print("Escopo atual", currentescope)
        # print("LLLL", l)
        if l[0] == "TYPEDEF":
            typedef_createvariable(l)
            # continue
        if l[0] == "INPUT":
            inputf(l)
            # continue
        if l[0] == "OUTPUT":
            outputf(l)
            # continue
        if l[0] == "WHILE":
            jump = whilef(l)
            continue
        if l[0] == "PROCEDURE":
            procedureexecute(l)
        if l[0] == "IF":
            jump = iff(l)
            continue
        if l[0] == "ELSE":
            return
        if l[0] == "END":
            return
        fl = functionsline.get(l[0])
        if fl != None:
            # print("chama aqui?")
            jump = functionf(l)
            continue
        if escope[currentescope].get(l[0]):
            # print("ta chamando aqui sera??????",
            #       l)
            variable(l)
        jump += 1


def begin():
    global functionsline
    global canread
    canread = True
    mainidx = functionsline["MAIN"]
    addescope(mainidx)
    reader(mainidx + 1)


def run(table):
    global tabela
    tabela = table

    initializefunctions()
    begin()
