import yfinance as yf
import matplotlib.pyplot as plt

ticker = "AMZN"
stock = yf.Ticker(ticker)
hist = stock.history(period='3mo')

hist["SMA_5"] = hist["Close"].rolling(window=5).mean()
hist["SMA_8"] = hist["Close"].rolling(window=8).mean()
hist["SMA_13"] = hist["Close"].rolling(window=13).mean()

def detect_crossover(df):
    buy_signals=[]
    sell_signals=[]
    for i in range(1, len(df)):
        if df['SMA_5'].iloc[i] > df['SMA_13'].iloc[i] and df['SMA_8'].iloc[i] > df['SMA_13'].iloc[i] and df['SMA_5'].iloc[i-1] <= df['SMA_13'].iloc[i-1]:
            buy_signals.append((df.index[i], df['Close'].iloc[i]))
        elif df['SMA_13'].iloc[i] > df['SMA_8'].iloc[i] > df['SMA_5'].iloc[i] and df['SMA_8'].iloc[i - 1] >= df['SMA_13'].iloc[i - 1]:
            sell_signals.append((df.index[i], df['Close'].iloc[i]))
    return buy_signals, sell_signals

buy_signals, sell_signals=detect_crossover(hist)
plt.figure(figsize=(14,7))
plt.plot(hist['Close'], label='AMZN Close', alpha=1.0)
plt.plot(hist['SMA_5'], label='SMA_5', alpha=1.0)
plt.plot(hist['SMA_8'], label='SMA_8', alpha=1.0)
plt.plot(hist['SMA_13'], label='SMA_13', alpha=1.0)

for signal in buy_signals:
    plt.plot(signal[0], signal[1], marker='o', markersize=10, color='green', label="Buy Signal")

for signal in sell_signals:
    plt.plot(signal[0], signal[1], marker='o', markersize=10, color='red', label="Sell Signal")

plt.title("AMZN Closure Prices and SMA Crossovers")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()