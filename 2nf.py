import copy
from gramatica import gramatica
from cnf import criar_regras_duas_vars
from cnf import formatar
from cnf import validar
from cnf import start

def converter_para_2nf(gramatica):
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
    converter_para_2nf(gram)
    print(
        "3------------------------------------------------------------------------------------------------------------------------------------"
    )
    print(gram)


main()  #