from gramatica import gramatica
from cnf import *


def converter_para_bnf(gramatica):
    gramatica.regras_arr()
    # print("---------- CONVERTER PARA BNF ")
    if not validar(gramatica):
        return

    # criar regra s0
    # print("\n---------- CRIAR REGRA S0 (START)-----------")
    start(gramatica)
    # print(gramatica)
    
    # print("\n---------- REMOVER TERMINAIS (TERM)-----------")
    # remover_terminais(gramatica)
    # print(gramatica)

    # print("\n---------- REMOVER MAIS DE 2 VARIÁVEIS (BIN)-----------")
    criar_regras_duas_vars(gramatica)
    # print(gramatica)

    gramatica.regras_dict()
    return gramatica