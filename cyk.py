from gramatica import gramatica
from cnf import converter_para_cnf


def cyk(regras, sentencas):
    n = len(sentencas)
    r = len(regras)

    # Inicializa a tabela CYK
    table = [[set() for _ in range(n)] for _ in range(n)]

    # Preenche a tabela CYK para substrings de tamanho 1
    for i in range(n):
        for rule in regras:
            if sentencas[i] in regras[rule]:
                table[i][i].add(rule)

    # Preenche a tabela CYK para substrings de tamanho maior que 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for rule in regras:
                    for producao in regras[rule]:
                        if (
                            len(producao) == 2
                            and producao[0] in table[i][k]
                            and producao[1] in table[k + 1][j]
                        ):
                            table[i][j].add(rule)

    # Verifica se a sentença pode ser gerada pela gramática
    return "S" in table[0][n - 1]


variaveis = ["S", "A", "B", "C"]
terminais = ["a", "b"]
inicial = "S"
regras = {"S": ["AB", "BC"], "A": ["a", "bA", "CCA"],
          "B": ["CC", "b"], "C": ["AB", "a"]}

gramatica = gramatica(variaveis, terminais, inicial, regras)
converter_para_cnf(gramatica)
gramatica.regras_dict()

# Exemplo de uso
sentenca = "bbbbbbbbbbbbab"

resultado = cyk(gramatica.regras, sentenca)
if resultado:
    print("A gramática pode gerar a sentença.")
else:
    print("A gramática não pode gerar a sentença.")
