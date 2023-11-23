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