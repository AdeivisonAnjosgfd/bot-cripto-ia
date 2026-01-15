class PaperTradingBot:
    def __init__(self):
        self.saldo = 1000
        self.moedas = 0
        self.historico = []

    def comprar(self, preco):
        if self.saldo > 0:
            self.moedas = self.saldo / preco
            self.saldo = 0
            self.historico.append({"Ação": "COMPRA", "Preço": preco})

    def vender(self, preco):
        if self.moedas > 0:
            self.saldo = self.moedas * preco
            self.moedas = 0
            self.historico.append({"Ação": "VENDA", "Preço": preco})

    def resultado(self, preco):
        return self.saldo + (self.moedas * preco)

    def decidir(self, rsi, preco):
        if rsi < 40:
            self.comprar(preco)
            return "COMPRANDO"
        elif rsi > 70:
            self.vender(preco)
            return "VENDENDO"
        else:
            return "AGUARDANDO"
