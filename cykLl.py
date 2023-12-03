# Implementação do algoritmo CYK modificado para 2NF
def cykLl(gramatica, sentenca):
    n = len(sentenca)

    # Inicializando a tabela CYK
    tabela = [[set() for _ in range(n + 1)] for _ in range(n + 1)]

    # Preenchendo a diagonal principal da tabela
    for i in range(1, n + 1):
        tabela[i][i] = gramatica.obter_relacao_unitaria({sentenca[i - 1]})

    # Preenchendo as demais células da tabela
    for j in range(2, n + 1):
        for i in range(j - 1, 0, -1):
            tabela[i][j] = set()
            for h in range(i, j):
                for variavel in gramatica.variaveis:
                    for producao in gramatica.regras[variavel]:
                        if len(producao) == 2:  # Regra do tipo X -> YZ
                            Y, Z = producao
                            if Y in tabela[i][h] and Z in tabela[h + 1][j]:
                                tabela[i][j].add(variavel)

                # Verificar regras unitárias
                for variavel_unitaria in gramatica.obter_relacao_unitaria(tabela[i][h]):
                    tabela[i][j].add(variavel_unitaria)

    # Verificando se o símbolo inicial está na célula T1,n
    return gramatica.inicial in tabela[1][n]

