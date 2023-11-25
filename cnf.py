import copy
from gramatica import gramatica


def converter_para_cnf(gramatica):
    gramatica.regras_arr()
    print("---------- CONVERTER PARA CNF ")
    if not validar(gramatica):
        return

    # criar regra s0
    print("\n---------- CRIAR REGRA S0 (START)-----------")
    start(gramatica)
    print(gramatica)

    print("\n---------- REMOVER MAIS DE 2 VARIÁVEIS (BIN)-----------")
    criar_regras_duas_vars(gramatica)
    print(gramatica)

    print("\n---------- REMOVER VAZIO (DEL)-----------")
    remover_vazio(gramatica)
    print(gramatica)

    print("\n---------- REMOVER REGRAS UNITÁRIAS (UNIT)-----------")
    remover_unitarias(gramatica)
    print(gramatica)

    print("\n---------- REMOVER TERMINAIS (TERM)-----------")
    remover_terminais(gramatica)
    print(gramatica)

    return gramatica


def remover_vazio(gramatica):
    regras = {
        variable: production.split("|")
        for variable, production in [rule.split(">") for rule in gramatica.regras]
    }
    variaveis = gramatica.variaveis

    # list with keys of empty regras
    regras_vazias = []

    # find non-terminal regras and add them in list
    regras_copia = copy.deepcopy(regras)
    for key in regras_copia:
        values = regras_copia[key]
        for i in range(len(values)):
            # if key gives an empty state and is not in the list, add it
            if values[i] == "$" and key not in regras_vazias:
                regras_vazias.append(key)
                # remove empty state
                regras[key].remove(values[i])
        # if key doesn't contain any values, remove it from the dictionary
        if len(regras[key]) == 0:
            if key not in regras:
                variaveis.remove(key)
            regras.pop(key, None)

    print("----DEBUG:", regras_vazias)
    for regra in regras[gramatica.inicial]:
        if regra in regras_vazias:
            regras[gramatica.inicial].append("$")
            break
    # if initial variable produces one of the ruls in regras_vazia, add $ to its productions

    # delete empty regras
    regras_copia = copy.deepcopy(regras)
    print("----DEBUG:", regras_copia)
    for key in regras_copia:
        if key != gramatica.inicial:
            values = regras_copia[key]
            for i in range(len(values)):
                # check for regras in the form A->BC or A->CB, where B is in regras_vazias
                # and C in vocabulary
                if len(values[i]) == 2:
                    # check for the rule in the form A->BC, excluding the case that
                    # gives A->A as a result)
                    if values[i][0] in regras_vazias and key != values[i][1]:
                        regras.setdefault(key, []).append(values[i][1])
                    # check for the rule in the form A->CB, excluding the case that
                    # gives A->A as a result)
                    if values[i][1] in regras_vazias and key != values[i][0]:
                        if values[i][0] != values[i][1]:
                            regras.setdefault(key, []).append(values[i][0])

    # Convert the regras back to the format used in the Gramatica class
    regras_copia = [
        f"{key}>{'|'.join(values) if values else '$'}" for key, values in regras.items()
    ]
    gramatica.regras = regras_copia
    gramatica.variaveis = variaveis


def start(gramatica):
    # encontrar regra inicial
    regra_inicial = False
    for k in range(len(gramatica.regras)):
        regra2 = gramatica.regras[k]
        arr2 = regra2.split(">")
        var2 = arr2[0]
        if var2 == gramatica.inicial:
            regra_inicial = regra2
            break

    if not regra_inicial:
        raise ValueError("Regra inicial não encontrada")

    producoes_regra_inicial = regra_inicial.split(">")[1]

    # remover regras que produzem a inicial
    for i in range(len(gramatica.regras)):
        regra = gramatica.regras[i]
        if regra != regra_inicial:
            arr = regra.split(">")
            var = arr[0]
            producoes = arr[1]
            if gramatica.inicial in producoes:
                # substituir com as producoes da regra inicial)
                producoes = producoes.replace(
                    gramatica.inicial, producoes_regra_inicial
                )

                # substituir aparições da variável inicial com a var da regra atual
                producoes = producoes.replace(gramatica.inicial, var)
                producoes = "|".join(list(set(producoes.split("|"))))

                gramatica.regras[i] = var + ">" + producoes

    s0 = gramatica.inicial + "0"
    gramatica.regras.append(s0 + ">" + gramatica.inicial)
    gramatica.inicial = s0


def formatar(gramatica):
    # remover espaços, etc
    for i in range(len(gramatica.variaveis)):
        gramatica.variaveis[i] = gramatica.variaveis[i].replace(" ", "")

    # se existir mais de uma regra para uma variável, juntar em uma só
    for i in range(len(gramatica.regras)):
        arr = gramatica.regras[i].split(">")
        var = arr[0]
        producoes = arr[1].split("|")
        for j in range(len(producoes)):
            producoes[j] = producoes[j].replace(" ", "")
        gramatica.regras[i] = reescrever_regra(var, producoes)


def validar(gramatica):
    # checa se inicial está em variaveis
    if gramatica.inicial not in gramatica.variaveis:
        print("ERRO: inicial não está em variáveis")
        return False
    # checa se variaveis e terminais são disjuntos
    for variavel in gramatica.variaveis:
        if variavel in gramatica.terminais:
            print("ERRO: variáveis e terminais não são disjuntos")
            return False

    # checa se regras são válidas
    for regra in gramatica.regras:
        # checa se regra está na forma X>Y|a|$
        arr = regra.split(">")
        if len(arr) != 2:
            print("ERRO: regra não está na forma X>Y|a|$")
            return False
        # checa se X está em variaveis
        if arr[0] not in gramatica.variaveis:
            print(f"ERRO: {arr[0]} não está em variáveis")
            return False
        producoes = arr[1].split("|")
        for producao in producoes:
            for char in producao:
                # checa se produção é válida
                if (
                    char not in gramatica.variaveis
                    and char not in gramatica.terminais
                    and char != "$"
                ):
                    print("ERRO: produção não é válida. char: ", char)
                    return False

    return True


def reescrever_regra(var, producoes):
    # recebe um array e retorna a string X|Y|...|Z
    string = ""
    for i in range(len(producoes)):
        string += producoes[i]
        if i != len(producoes) - 1:
            string += "|"

    if string == "":
        string = "$"

    # remover regras duplicadas
    string = "|".join(list(set(string.split("|"))))

    return var + ">" + string


def criar_variavel(gramatica, producoes):
    # cria uma nova variável e retorna a regra
    nova_var = "A"
    while (
        (ord(nova_var) < ord("Z"))
        and (nova_var in gramatica.variaveis)
        or (nova_var in gramatica.terminais)
    ):
        nova_var = chr(ord(nova_var) + 1)

    if nova_var == "Z" and nova_var in gramatica.variaveis:
        raise ValueError("Não há mais variáveis disponíveis")

    nova_regra = reescrever_regra(nova_var, producoes)

    gramatica.variaveis.append(nova_var)
    gramatica.regras.append(nova_regra)
    return nova_regra


def remover_terminais(gramatica):
    for i in range(len(gramatica.terminais)):
        # encontrar todas as regras que produzem a terminal
        regras_com_terminal = [
            regra
            for regra in gramatica.regras
            if gramatica.terminais[i] in regra.split(">")[1]
        ]

        print("regras_com_terminal: ", regras_com_terminal)

        unitaria = False
        # ver se alguma dessas regras produz apenas a terminal
        for j in range(len(regras_com_terminal)):
            regra = regras_com_terminal[j]
            arr = regra.split(">")
            producoes = arr[1].split("|")
            if len(producoes) == 1 and producoes[0] == gramatica.terminais[i]:
                unitaria = regra
                j = len(regras_com_terminal)

        if unitaria:
            # remover ela do arr regras
            regras_com_terminal.remove(unitaria)
        else:
            unitaria = criar_variavel(gramatica, [gramatica.terminais[i]])

        # substituir todas as regras que produzem a terminal pela unitaria
        for j in range(len(regras_com_terminal)):
            regra = regras_com_terminal[j]
            arr = regra.split(">")
            var = arr[0]
            producoes = arr[1].split("|")
            for k in range(len(producoes)):
                if len(producoes[k]) > 1:
                    producoes[k] = producoes[k].replace(
                        gramatica.terminais[i], unitaria.split(">")[0]
                    )

            nova_regra = reescrever_regra(var, producoes)
            # encontrar posicao da regra no arr gramatica.regras
            for k in range(len(gramatica.regras)):
                if gramatica.regras[k] == regra:
                    gramatica.regras[k] = nova_regra
                    k = len(gramatica.regras)

    return


def remover_unitarias(gramatica):
    regras = gramatica.regras
    # regras = arr de strings
    for i in range(len(regras)):
        regra = regras[i]
        arr = regra.split(">")
        var = arr[0]
        producoes = arr[1].split("|")

        for j in range(len(producoes)):
            producao = producoes[j]
            if len(producao) == 1 and producao in gramatica.variaveis:
                for k in range(len(regras)):
                    if k != i:
                        regra2 = regras[k]
                        arr2 = regra2.split(">")
                        var2 = arr2[0]
                        producoes2 = arr2[1].split("|")

                        if var2 == producao:
                            producoes = producoes + producoes2
                            producoes = [p for p in producoes if p != producao]
                            break

        producoes = list(set(producoes))  # remover producoes duplicadas

        gramatica.regras[i] = reescrever_regra(var, producoes)


def obter_arr_vars(gramatica, regras):
    arr_vars = []

    for i in range(len(regras)):
        regra = regras[i]
        arr = regra.split(">")
        var = arr[0]
        producoes = arr[1].split("|")

        for j in range(len(producoes)):
            producao = producoes[j]
            if len(producao) > 2:
                for k in range(len(producao) - 1):
                    regra_dupla = "" + producao[k] + producao[k + 1]
                    guardada = False
                    for l in range(len(arr_vars)):
                        vars = arr_vars[l]
                        if vars[0] == regra_dupla:
                            vars[1] += 1
                            guardada = True
                            arr_vars[l] = vars
                            break

                    if not guardada:
                        arr_vars.append([regra_dupla, 1])
    return arr_vars


def criar_regras_duas_vars(gramatica):
    regras = gramatica.regras
    # passo 1:  encontrar conjunto de duas variaveis que mais aparece em producoes com 3 ou mais variaveis

    arr_vars = obter_arr_vars(gramatica, regras)
    while len(arr_vars) > 0:
        # encontrando duplicada mais frequente
        dup_mais_frequente = arr_vars[0]
        for i in range(1, len(arr_vars)):
            if dup_mais_frequente[1] < arr_vars[i][1]:
                dup_mais_frequente = arr_vars[i]

        # passo2:   checar se já existe uma regra que produz apenas a duplicada
        #           ou criar uma regra nova com a produção
        regra_dup = False
        for i in range(len(regras)):
            regra = regras[i]
            arr = regra.split(">")
            var = arr[0]
            producoes = arr[1].split("|")

            if len(producoes) == 1 and producoes[0] == dup_mais_frequente[0]:
                regra_dup = regra
                break

        if not regra_dup:
            regra_dup = criar_variavel(gramatica, [dup_mais_frequente[0]])

        # passo 3:  substituir todas as producoes de dup com a regra
        for i in range(len(regras)):
            regra = regras[i]
            if regra_dup != regra:
                arr = regra.split(">")
                var = arr[0]
                producoes = arr[1].split("|")
                for j in range(len(producoes)):
                    producoes[j] = producoes[j].replace(
                        dup_mais_frequente[0], regra_dup.split(">")[0]
                    )

                gramatica.regras[i] = reescrever_regra(var, producoes)

        # passo 4:  encontrar novamente variáveis duplas
        regras = gramatica.regras
        arr_vars = obter_arr_vars(gramatica, regras)


def main():
    # variaveis = input("Variáveis: ")
    # terminais = input("Terminais: ")
    # inicial = input("Inicial: ")
    # regras = input("Regras: ")

    variaveis = ["S", "X", "Y"]
    terminais = ["a", "b"]
    inicial = "S"
    regras = ["S>XY|$", "X>SY|a|bb", "Y>aa"]

    gram = gramatica(variaveis, terminais, inicial, regras)
    print(
        "1------------------------------------------------------------------------------------------------------------------------------------"
    )
    print(gram)
    formatar(gram)
    print(
        "2-----------------------------------------------------------------------------------------------------------------------------------"
    )
    print(gram)
    gram.regras_arr()
    converter_para_cnf(gram)
    print(
        "3------------------------------------------------------------------------------------------------------------------------------------"
    )
    print(gram)


main()  #
