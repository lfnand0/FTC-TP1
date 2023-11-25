class gramatica:
    def __init__(self, variaveis, terminais, inicial, regras):
        self.variaveis = variaveis  # char[]
        self.terminais = terminais  # char[]
        self.inicial = inicial  # char
        self.regras = regras
        # regras na forma X>Y|a|$ ou dict com X: [Y, a, $]
        # usar funções regras_dict() e regras_arr() para converter

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

    def arr_to_dict(arr):
        # converts rules from array of strings to dict
        regras = {}
        for regra in arr:
            variavel, producoes = regra.split(">")
            regras[variavel] = producoes.split("|")

        return regras

    def dict_to_arr(d):
        # converts rules from dict to array of strings
        regras = []
        for variavel in d:
            str = variavel + ">"
            for producao in d[variavel]:
                str += producao + "|"
            str = str[:-1]
            if str[-1] != ">":
                regras.append(str)

        return regras

    def regras_dict(self):
        if type(self.regras) is list:
            self.regras = gramatica.arr_to_dict(self.regras)

        return self.regras

    def regras_arr(self):
        if type(self.regras) is dict:
            self.regras = gramatica.dict_to_arr(self.regras)

        return self.regras
