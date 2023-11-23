from gramatica import gramatica

def cyk(rules, sentence):
    n = len(sentence)
    r = len(rules)

    # Inicializa a tabela CYK
    table = [[set() for _ in range(n)] for _ in range(n)]

    # Preenche a tabela CYK para substrings de tamanho 1
    for i in range(n):
        for rule in rules:
            if sentence[i] in rules[rule]:
                table[i][i].add(rule)

    # Preenche a tabela CYK para substrings de tamanho maior que 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for rule in rules:
                    for production in rules[rule]:
                        if len(production) == 2 and production[0] in table[i][k] and production[1] in table[k + 1][j]:
                            table[i][j].add(rule)

    # Verifica se a sentença pode ser gerada pela gramática
    return 'S' in table[0][n - 1]

variaveis = ["S", "X", "Y"]
terminais = ["a", "b"]
inicial = "S"
regras = {
    'S': ['AB', 'BC'],
    'A': ['BA', 'a'],
    'B': ['CC', 'b'],
    'C': ['AB', 'a']
}

gramatica = gramatica(variaveis, terminais, inicial, regras)

# Exemplo de uso
sentenca = "ababbaabbaabab"

resultado = cyk(gramatica.regras, sentenca)
if resultado:
    print("A gramática pode gerar a sentença.")
else:
    print("A gramática não pode gerar a sentença.")


