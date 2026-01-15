import streamlit as st
import pandas as pd
import ta
from binance.client import Client
from config import API_KEY, API_SECRET
from bot import PaperTradingBot

st.set_page_config(page_title="Bot Cripto - Simulador", layout="centered")

client = Client(API_KEY, API_SECRET)

st.title("🤖 Bot Cripto - Simulador de Investimentos")

# Inicializa o bot virtual
if "bot" not in st.session_state:
    st.session_state.bot = PaperTradingBot()

# Seleção de par
par = st.selectbox("Escolha o par", ["BTCUSDT", "ETHUSDT"])

# Carregar dados
def carregar_dados(simbolo):
    klines = client.get_klines(symbol=simbolo, interval=Client.KLINE_INTERVAL_1MINUTE, limit=100)
    df = pd.DataFrame(klines, columns=[
        "time", "open", "high", "low", "close", "volume",
        "ct", "qav", "nt", "tb", "tq", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    return df

df = carregar_dados(par)

# Indicador RSI
df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()

preco = float(df["close"].iloc[-1])
rsi_atual = df["rsi"].iloc[-1]

st.metric("Preço Atual", f"R$ {preco:.2f}")
st.metric("RSI Atual", f"{rsi_atual:.2f}")
acao = st.session_state.bot.decidir(rsi_atual, preco)
st.warning(f"🧠 IA: {acao}")


# Exibe status
st.write(f"💰 Saldo virtual: R$ {st.session_state.bot.saldo:.2f}")
st.write(f"🪙 Moedas: {st.session_state.bot.moedas:.6f}")
st.write(f"📊 Patrimônio: R$ {st.session_state.bot.resultado(preco):.2f}")

# Botões manuais
col1, col2 = st.columns(2)
with col1:
    if st.button("Simular COMPRA"):
        st.session_state.bot.comprar(preco)

with col2:
    if st.button("Simular VENDA"):
        st.session_state.bot.vender(preco)

# Histórico
st.subheader("📜 Histórico de Operações")
if len(st.session_state.bot.historico) > 0:
    st.dataframe(pd.DataFrame(st.session_state.bot.historico))
else:
    st.write("Nenhuma operação realizada ainda.")
