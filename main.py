from bnf import converter_para_bnf
from cyk import cyk
from cykLl import cykLl
from gramatica import gramatica
from cnf import converter_para_cnf


def carregar_gramatica(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.read().splitlines()

    variaveis = eval(linhas[0].split('=')[1].strip())
    terminais = eval(linhas[1].split('=')[1].strip())
    inicial = eval(linhas[2].split('=')[1].strip())
    regras = eval(linhas[3].split('=')[1].strip())

    return variaveis, terminais, inicial, regras

# def testar_sentencas(gramatica, sentencas):
#     gramatica = converter_para_cnf(gramatica)
#     # Implemente aqui o código para testar as sentenças usando a gramática
#     for sentenca in sentencas:
#         if cyk(gramatica.regras_dict(), sentenca):
#             print(f'A sentença "{sentenca}" é válida.')
#         else:
#             print(f'A sentença "{sentenca}" NÃO é válida.')

def testar_sentencas(gramatica, sentencas):
    gramatica = converter_para_bnf(gramatica)
    # Implemente aqui o código para testar as sentenças usando a gramática
    for sentenca in sentencas:
        if cykLl(gramatica, sentenca):
            print(f'A sentença "{sentenca}" é válida.')
        else:
            print(f'A sentença "{sentenca}" NÃO é válida.')


if __name__ == "__main__":
    # Substitua pelo caminho correto do seu arquivo
    caminho_arquivo = "inputs\\gramatica.txt"
    param = carregar_gramatica(caminho_arquivo)
    gram = gramatica(param[0], param[1], param[2], param[3])

    sentencas = []
    leitura_sentencas = False

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            if linha.strip() == "":
                leitura_sentencas = True
                continue
            if leitura_sentencas:
                sentencas.append(linha.strip())

    testar_sentencas(gram, sentencas)
