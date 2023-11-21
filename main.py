class gramatica:
    def __init__(self, variaveis, terminais, inicial, regras):
        self.variaveis = variaveis  # char[]
        self.terminais = terminais  # char[]
        self.inicial = inicial  # char
        self.regras = regras  # string[], regras na forma X>Y|a|$

    def __repr__(self):
        return (
            "Variáveis: "
            + str(self.variaveis)
            + "\nTerminais: "
            + str(self.terminais)
            + "\nInicial: "
            + str(self.inicial)
            + "\nRegras: "
            + str(self.regras)
        )

    def converter_para_cnf(self):
        print("---------- CONVERTER PARA CNF ")
        if not self.validar():
            return

        # criar regra s0
        print("\n---------- CRIAR REGRA S0 (START)-----------")
        self.start()

        print("\n---------- REMOVER TERMINAIS (TERM)-----------")
        self.remover_terminais()
        print(self)

        print("\n---------- REMOVER MAIS DE 2 VARIÁVEIS (BIN)-----------")
        self.criar_regras_duas_vars()
        print(self)

        print("\n---------- REMOVER VAZIO (DEL)-----------")
        self.remover_vazio()
        print(self)

        print("\n---------- REMOVER REGRAS UNITÁRIAS (UNIT)-----------")
        self.remover_unitarias()
        print(self)

    def start(self):
        # encontrar regra inicial
        regra_inicial = False
        for k in range(len(self.regras)):
            regra2 = self.regras[k]
            arr2 = regra2.split(">")
            var2 = arr2[0]
            if var2 == self.inicial:
                regra_inicial = regra2
                break

        print("regra inicial: ", regra_inicial)

        if not regra_inicial:
            raise ValueError("Regra inicial não encontrada")

        producoes_regra_inicial = regra_inicial.split(">")[1]

        # remover regras que produzem a inicial
        for i in range(len(self.regras)):
            regra = self.regras[i]
            if regra != regra_inicial:
                arr = regra.split(">")
                var = arr[0]
                producoes = arr[1]
                if self.inicial in producoes:
                    # substituir com as producoes da regra inicial)
                    print(
                        "producoes before: ",
                        producoes,
                        self.inicial,
                        producoes_regra_inicial,
                    )
                    producoes = producoes.replace(self.inicial, producoes_regra_inicial)

                    print("producoes after1: ", producoes)

                    # substituir aparições da variável inicial com a var da regra atual
                    producoes = producoes.replace(self.inicial, var)

                    print("producoes after2: ", producoes)

                    self.regras[i] = var + ">" + producoes

        s0 = self.inicial + "0"
        self.regras.append(s0 + ">" + self.inicial)
        self.inicial = s0
        print(self)

    def formatar(self):
        # remover espaços, etc
        for i in range(len(self.variaveis)):
            self.variaveis[i] = self.variaveis[i].replace(" ", "")

        # se existir mais de uma regra para uma variável, juntar em uma só
        for i in range(len(self.regras)):
            arr = self.regras[i].split(">")
            var = arr[0]
            producoes = arr[1].split("|")
            for j in range(len(producoes)):
                producoes[j] = producoes[j].replace(" ", "")
            self.regras[i] = self.reescrever_regra(var, producoes)

    def validar(self):
        # checa se inicial está em variaveis
        if self.inicial not in self.variaveis:
            print("ERRO: inicial não está em variáveis")
            return False
        # checa se variaveis e terminais são disjuntos
        for variavel in self.variaveis:
            if variavel in self.terminais:
                print("ERRO: variáveis e terminais não são disjuntos")
                return False

        # checa se regras são válidas
        for regra in self.regras:
            # checa se regra está na forma X>Y|a|$
            arr = regra.split(">")
            if len(arr) != 2:
                print("ERRO: regra não está na forma X>Y|a|$")
                return False
            # checa se X está em variaveis
            if arr[0] not in self.variaveis:
                print(f"ERRO: {arr[0]} não está em variáveis")
                return False
            producoes = arr[1].split("|")
            for producao in producoes:
                for char in producao:
                    # checa se produção é válida
                    if (
                        char not in self.variaveis
                        and char not in self.terminais
                        and char != "$"
                    ):
                        print("ERRO: produção não é válida. char: ", char)
                        return False

        return True

    def reescrever_regra(self, var, producoes):
        # recebe um array e retorna a string X|Y|...|Z
        string = ""
        for i in range(len(producoes)):
            string += producoes[i]
            if i != len(producoes) - 1:
                string += "|"

        if string == "":
            string = "$"

        return var + ">" + string

    def criar_variavel(self, producoes):
        # cria uma nova variável e retorna a regra
        nova_var = "A"
        while (
            (ord(nova_var) < ord("Z"))
            and (nova_var in self.variaveis)
            or (nova_var in self.terminais)
        ):
            nova_var = chr(ord(nova_var) + 1)

        if nova_var == "Z" and nova_var in self.variaveis:
            raise ValueError("Não há mais variáveis disponíveis")

        nova_regra = self.reescrever_regra(nova_var, producoes)

        self.variaveis.append(nova_var)
        self.regras.append(nova_regra)
        return nova_regra

    def remover_vazio(self):
        restart = False
        i = 0
        while i < len(self.regras):
            print("----DEBUG: ", i, self.regras)
            regra = self.regras[i]
            arr = regra.split(">")
            var = arr[0]
            if var != self.inicial:
                producoes = arr[1].split("|")
                for j in range(len(producoes)):
                    if j < len(producoes) and producoes[j] == "$":
                        producoes.pop(j)
                        for k in range(len(self.regras)):
                            arr2 = self.regras[k].split(">")
                            var2 = arr2[0]
                            producoes2 = arr2[1].split("|")
                            for l in range(len(producoes2)):
                                if var in producoes2[l]:
                                    char = producoes2[l].replace(var, "")
                                    if char == "":
                                        char = "$"
                                    producoes2.append(char)

                            self.regras[k] = self.reescrever_regra(var2, producoes2)
                            restart = True

                self.regras[i] = self.reescrever_regra(var, producoes)
            if restart:
                i = 0
                restart = False
            else:
                i += 1

    def remover_terminais(self):
        for i in range(len(self.terminais)):
            # encontrar todas as regras que produzem a terminal
            regras_com_terminal = []
            for j in range(len(self.regras)):
                regra = self.regras[j]
                arr = regra.split(">")
                producoes = arr[1].split("|")
                for k in range(len(producoes)):
                    if producoes[k] == self.terminais[i]:
                        regras_com_terminal.append(regra)
                        break

            unitaria = False
            # ver se alguma dessas regras produz apenas a terminal
            for j in range(len(regras_com_terminal)):
                regra = regras_com_terminal[j]
                arr = regra.split(">")
                producoes = arr[1].split("|")
                if len(producoes) == 1 and producoes[0] == self.terminais[i]:
                    unitaria = regra
                    break

            if unitaria:
                # remover ela do arr regras
                regras_com_terminal.remove(unitaria)
            else:
                unitaria = self.criar_variavel([self.terminais[i]])

            # substituir todas as regras que produzem a terminal pela unitaria
            for j in range(len(regras_com_terminal)):
                regra = regras_com_terminal[j]
                arr = regra.split(">")
                var = arr[0]
                producoes = arr[1].split("|")
                for k in range(len(producoes)):
                    producoes[k] = producoes[k].replace(
                        self.terminais[i], unitaria.split(">")[0]
                    )

                nova_regra = self.reescrever_regra(var, producoes)

                # encontrar posicao da regra no arr self.regras
                for k in range(len(self.regras)):
                    if self.regras[k] == regra:
                        self.regras[k] = nova_regra
                        break

        return

    def remover_unitarias(self):
        regras = self.regras
        # regras = arr de strings
        for i in range(len(regras)):
            regra = regras[i]
            arr = regra.split(">")
            var = arr[0]
            producoes = arr[1].split("|")

            for j in range(len(producoes)):
                producao = producoes[j]
                if len(producao) == 1 and producao in self.variaveis:
                    for k in range(len(regras)):
                        if k != i:
                            regra2 = regras[k]
                            arr2 = regra2.split(">")
                            var2 = arr2[0]
                            producoes2 = arr2[1].split("|")

                            if var2 == producao:
                                producoes = producoes + producoes2
                                break

                elif len(producao) == 1 and producao in self.terminais:
                    # checar se existe alguma regra que produz apenas producao
                    regra_unitaria = False
                    for k in range(len(regras)):
                        if k != i:
                            regra2 = regras[k]
                            arr2 = regra2.split(">")
                            var2 = arr2[0]
                            producoes2 = arr2[1].split("|")

                            if len(producoes2) == 1 and producoes2[0] == producao:
                                regra_unitaria = regras[k]
                                break

                    if regra_unitaria:
                        producoes[j] = regra_unitaria.split(">")[0]
                    else:
                        regra_unitaria = self.criar_variavel([producao])
                        producoes[j] = regra_unitaria.split(">")[0]

            producoes = list(set(producoes))  # remover producoes duplicadas
            self.regras[i] = self.reescrever_regra(var, producoes)

    def obter_arr_vars(self, regras):
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

    def criar_regras_duas_vars(self):
        regras = self.regras
        # passo 1:  encontrar conjunto de duas variaveis que mais aparece em producoes com 3 ou mais variaveis

        arr_vars = self.obter_arr_vars(regras)
        while len(arr_vars) > 0:
            # encontrando duplicada mais frequente
            dup_mais_frequente = arr_vars[0]
            for i in range(1, len(arr_vars)):
                if dup_mais_frequente[1] < arr_vars[i][1]:
                    dup_mais_frequente = arr_vars

            # passo2:   checar se já existe uma regra que produz apenas a duplicada
            #           ou criar uma regra nova com a produção
            regra_dup = False
            for i in range(len(regras)):
                regra = regras[i]
                arr = regra.split(">")
                var = arr[0]
                producoes = arr[1].split("|")

                if len(producoes) == 1 and producoes[0] == dup_mais_frequente[0]:
                    print("ACHOU ")
                    regra_dup = regra
                    break

            if not regra_dup:
                regra_dup = self.criar_variavel([dup_mais_frequente[0]])

            # passo 3:  substituir todas as producoes de dup com a regra
            for i in range(len(regras)):
                regra = regras[i]
                print(regra_dup != regra)
                if regra_dup != regra:
                    arr = regra.split(">")
                    var = arr[0]
                    producoes = arr[1].split("|")
                    for j in range(len(producoes)):
                        producoes[j] = producoes[j].replace(
                            dup_mais_frequente[0], regra_dup.split(">")[0]
                        )

                    self.regras[i] = self.reescrever_regra(var, producoes)

            # passo 4:  encontrar novamente variáveis duplas
            regras = self.regras
            arr_vars = self.obter_arr_vars(regras)


def main():
    # variaveis = input("Variáveis: ")
    # terminais = input("Terminais: ")
    # inicial = input("Inicial: ")
    # regras = input("Regras: ")

    variaveis = ["S", "A", "B", "F"]
    terminais = ["a", "b"]
    inicial = "S"
    regras = ["S>ABF|a|ABS|ASB|BSA", "A>B|a|b", "B>b|a|$", "F>a|$|S|SF|$"]

    gram = gramatica(variaveis, terminais, inicial, regras)
    print("1-----------")
    print(gram)
    gram.formatar()
    print("2-----------")
    print(gram)
    gram.converter_para_cnf()
    print("3-----------")
    print(gram)


main()
