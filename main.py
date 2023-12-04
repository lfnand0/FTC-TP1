from bnf import converter_para_bnf
from cyk import cyk
from cykLl import cykLl
from gramatica import gramatica
from cnf import converter_para_cnf
import time

def carregar_gramatica(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.read().splitlines()

    variaveis = eval(linhas[0].split('=')[1].strip())
    terminais = eval(linhas[1].split('=')[1].strip())
    inicial = eval(linhas[2].split('=')[1].strip())
    regras = eval(linhas[3].split('=')[1].strip())

    return variaveis, terminais, inicial, regras

def testar_sentencas1(gramatica, sentencas):
    gramatica = converter_para_cnf(gramatica)
    # Implemente aqui o código para testar as sentenças usando a gramática
    for sentenca in sentencas:
        cyk(gramatica.regras_dict(), sentenca)
        # if cyk(gramatica.regras_dict(), sentenca):
        #     print(f'A sentença "{sentenca}" é válida.')
        # else:
        #     print(f'A sentença "{sentenca}" NÃO é válida.')

def testar_sentencas2(gramatica, sentencas):
    gramatica = converter_para_bnf(gramatica)
    # Implemente aqui o código para testar as sentenças usando a gramática
    for sentenca in sentencas:
        cykLl(gramatica, sentenca)
        # if cykLl(gramatica, sentenca):
        #     print(f'A sentença "{sentenca}" é válida.')
        # else:
        #     print(f'A sentença "{sentenca}" NÃO é válida.')


if __name__ == "__main__":
    # Substitua pelo caminho correto do seu arquivo

    iterations = 1000
    
    testes = ["inputs\\gramatica.txt", "inputs\\gramatica2.txt", "inputs\\gramatica3.txt"]
    for teste in testes:
        res_cyk = 0
        res_cykLl = 0
        caminho_arquivo = teste
        param = carregar_gramatica(caminho_arquivo)
        
        sentencas = []
        leitura_sentencas = False

        with open(caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                if linha.strip() == "":
                    leitura_sentencas = True
                    continue
                if leitura_sentencas:
                    sentencas.append(linha.strip())
                        
        for i in range(0, iterations):
            gram = gramatica(param[0], param[1], param[2], param[3])

            # get time
            start = time.time()
            testar_sentencas1(gram, sentencas)
            end = time.time()
            res_cyk += end - start
            
            start = time.time()
            testar_sentencas2(gram, sentencas)
            end = time.time()
            res_cykLl += end - start
        
        print("-------------------------TESTE: " + teste + "-------------------------")
        print("cyk: " + str(res_cyk))
        print("cykLl: " + str(res_cykLl))
