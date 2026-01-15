import backtrader as bt
import yfinance as yf
import pandas as pd
import numpy as np

class RSIStrategy(bt.Strategy):
    params = (
        ('rsi_buy', 30),
        ('rsi_sell', 70),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close)

    def next(self):
        if not self.position:
            if self.rsi < self.p.rsi_buy:
                self.buy(size=1)
        else:
            if self.rsi > self.p.rsi_sell:
                self.sell(size=1)

def rodar_teste(rsi_buy, rsi_sell):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(RSIStrategy, rsi_buy=rsi_buy, rsi_sell=rsi_sell)

    data = yf.download("BTC-USD", start="2022-01-01")
    feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(feed)

    cerebro.broker.setcash(1000)
    cerebro.run()

    return cerebro.broker.getvalue()

resultados = []

for rsi_buy in range(20, 36, 2):
    for rsi_sell in range(65, 81, 2):
        final = rodar_teste(rsi_buy, rsi_sell)
        lucro = final - 1000
        resultados.append((rsi_buy, rsi_sell, round(lucro,2)))
        print(f"RSI BUY {rsi_buy} | RSI SELL {rsi_sell} | Lucro: {lucro:.2f}")

df = pd.DataFrame(resultados, columns=["RSI_BUY","RSI_SELL","LUCRO"])
print("\n🏆 MELHOR CONFIGURAÇÃO:")
print(df.sort_values("LUCRO", ascending=False).head())
