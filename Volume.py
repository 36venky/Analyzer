import pandas as pd
import yfinance as yf
import logging
import Messages as MQ 
import Aanlyze_Sleep as AS   
import os
from datetime import datetime
import Messages as MQ   

# ==== CONFIG ====
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "Main.log")
processed_file = "processed_tickers.json"  # where we save already processed tickers

# ==== LOGGING ====
if not logging.getLogger().handlers:
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def is_volume_breakout():
    pass
    '''
    file_path = "buy_tickers.txt"

    # Read all lines first
    with open(file_path, "r") as file:
        lines = file.readlines()

    remaining_lines = []  # will keep unprocessed lines here

    for line in lines:
        line = line.strip()
        if not line:
            continue

        try:
            ticker, price, timestamp = line.split(",")
            price = float(price)
        except ValueError:
            logging.warning(f"Skipping malformed line: {line}")
            continue

        df = yf.download(
            ticker,
            period="2d",
            interval="15m",
            progress=False,
            auto_adjust=True
        )

        if df.empty or "Volume" not in df.columns:
            logging.warning(f"[{ticker}] No volume data available")
            remaining_lines.append(line + "\n")  # keep it for retry later
            continue

        df = df[~df.index.duplicated(keep="last")]
        df["VMA_5"] = df["Volume"].rolling(window=5).mean()
        latest_volume = df["Volume"].iloc[-1]
        latest_vma5 = df["VMA_5"].iloc[-1]

        if hasattr(latest_volume, "item"):
            latest_volume = latest_volume.item()
        if hasattr(latest_vma5, "item"):
            latest_vma5 = latest_vma5.item()

        if pd.notnull(latest_volume) and pd.notnull(latest_vma5):
            if latest_volume >= 2 * latest_vma5:
                logging.info(f"[{ticker}] ✅ Volume breakout detected: Volume={latest_volume}, VMA_5={latest_vma5}")
                msg = f"✅ BUY Signal\nStock: {ticker}\nTime: {timestamp}\nPrice: ₹{price:.2f}\nSL: ₹{(price - (price * 0.003)):.2f}\nTarget: ₹{(price + (price * 0.01)):.2f}"
                MQ.queue_whatsapp_message(msg)
                with open("Confirmed.txt", "a") as f:
                    f.write(f"{ticker},{price},{timestamp}\n")
                # ⚠ processed → do NOT keep it in remaining_lines
            else:
                logging.info(f"[{ticker}] No volume breakout: Volume={latest_volume}, VMA_5={latest_vma5}")
                # not confirmed → keep it for retry
                remaining_lines.append(line + "\n")
        else:
            logging.info(f"[{ticker}] Volume or VMA_5 is NaN, cannot determine breakout.")
            remaining_lines.append(line + "\n")

    # ✅ rewrite buy_tickers.txt with only remaining unprocessed ones
    with open(file_path, "w") as file:
        file.writelines(remaining_lines)
    #CL.clean_buy_tickers()

    # === CLEANUP at 08:30 PM ===
    now = datetime.now().strftime("%H:%M")
    if "20:25" <= now <= "20:35":  # 8:30 PM range
        open(log_file_path, "w").close()
        open("buy_tickers.txt", "w").close()'''