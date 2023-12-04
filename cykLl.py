from bnf import converter_para_bnf
from gramatica import gramatica

# Implementação do algoritmo CYK modificado para 2NF
def cykLl(gramatica, sentenca):
    n = len(sentenca)

    # Inicializando a tabela CYK
    tabela = [[set() for _ in range(n + 1)] for _ in range(n + 1)]

    # Preenchendo a diagonal principal da tabela
    for i in range(1, n + 1):
        tabela[i][i] = gramatica.obter_relacao_unitaria({sentenca[i - 1]})

    # Preenchendo as demais células da tabela
    for j in range(1, n + 1):
        for i in range(j - 1, 0, -1):
            tabela[i][j] = set()

            # Adiciona regras unitárias das células à esquerda
            for h in range(i, j):
                for variavel_unitaria in tabela[i][h]:
                    tabela[i][j].update(gramatica.obter_relacao_unitaria({variavel_unitaria}))

            # Verifica regras compostas X -> YZ
            for h in range(i, j):
                for variavel in gramatica.variaveis:
                    for producao in gramatica.regras[variavel]:
                        if len(producao) == 2:  # Regra do tipo X -> YZ
                            Y, Z = producao
                            if Y in tabela[i][h] and Z in tabela[h + 1][j]:
                                tabela[i][j].add(variavel)

    # Verificando se o símbolo inicial está na célula T1,n
    return gramatica.inicial in tabela[1][n]

# # Exemplo de uso
# variaveis = ["S", "A", "B", "C"]
# terminais = ["a", "b"]
# inicial = "S"
# regras = {"S": ["AB", "BC"], "A": ["a", "bA", "CCA"], "B": ["CC", "b"], "C": ["AB", "a"]}
# gramatica = converter_para_bnf(gramatica(variaveis, terminais, inicial, regras))

# # Teste com as sentenças
# sentenca1 = "bab"
# sentenca2 = "aba"

# print(cykLl(gramatica, sentenca1))  # Deve imprimir True
# print(cykLl(gramatica, sentenca2))  # Deve imprimir True
