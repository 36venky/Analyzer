import yfinance as yf
import pandas as pd

def get_rsi(data, length=14):
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/length, min_periods=length).mean()
    avg_loss = loss.ewm(alpha=1/length, min_periods=length).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def main():
    ticker = "STEL.ns"
    data = yf.download(ticker, period="2d", interval="15m", progress=False, auto_adjust=True)

    # Calculate RSI
    data['RSI'] = get_rsi(data, length=14)

    # Print only the latest RSI and Close price
    latest_close = data['Close'].iloc[-1]
    latest_rsi = data['RSI'].iloc[-1]
    print(f"RSI(14): {latest_rsi:.2f}")

if __name__ == "__main__":
    main()