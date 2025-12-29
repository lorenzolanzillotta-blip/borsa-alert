import yfinance as yf
import requests
import os
from datetime import datetime

# CONFIG
TICKER = "DCAM.PA"
THRESHOLD = -2.0  # percento

PUSHOVER_USER = os.environ["PUSHOVER_USER"]
PUSHOVER_TOKEN = os.environ["PUSHOVER_TOKEN"]

def send_notification(message):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "title": "📉 Alert Borsa",
            "message": message,
            "priority": 1
        },
        timeout=10
    )

def main():
    ticker = yf.Ticker(TICKER)

    # dati intraday (1 giorno)
    data = ticker.history(period="1d", interval="5m")

    if data.empty:
        print("Nessun dato disponibile")
        return

    open_price = data.iloc[0]["Open"]
    last_price = data.iloc[-1]["Close"]

    change_pct = (last_price - open_price) / open_price * 100

    print(f"{TICKER} | Open: {open_price:.2f} | Last: {last_price:.2f} | {change_pct:.2f}%")

    if change_pct <= THRESHOLD:
        now = datetime.now().strftime("%H:%M")
        send_notification(
            f"{TICKER} è a {change_pct:.2f}%\n"
            f"Apertura: {open_price:.2f}\n"
            f"Ultimo: {last_price:.2f}\n"
            f"Ora: {now}"
        )

if __name__ == "__main__":
    main()
