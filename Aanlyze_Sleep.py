import yfinance as yf
import pandas as pd
import math
import logging
import os
import time as tm
from datetime import datetime, timedelta , time
import Threshold_Ange as TA
import Volume as V

# --- Logging Setup ---
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "Main.log")
if not logging.getLogger().handlers:
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

# --- Global Buy State ---
buy_triggered = {}

def analyze_real_time(ticker):
    now = datetime.now().time()
    # --- Time Range ---
    start_time = time(9, 00)
    end_time = time(14, 55)

    T = 1

    if (start_time <= now <= end_time and 0 <= datetime.now().weekday() <= 4) or T == 1:  # Monday to Friday
        #logging.info(f"Analyzing {ticker}")

        try:
            data = yf.download(ticker, interval='15m', period='2d', progress=False, auto_adjust=True)
        except Exception as e:
            logging.error(f"[{ticker}] Download error: {e}")
            return

        if data.empty or len(data) < 9:
            logging.warning(f"[{ticker}] Not enough data.")
            return

        data.index = data.index.tz_convert('Asia/Kolkata')
        data = data.between_time("09:15", "15:30")

        df = data[['Open', 'High', 'Low', 'Close']].copy()
        ha_df = pd.DataFrame(index=df.index, columns=['Open', 'High', 'Low', 'Close'])
        ha_df['Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4

        ha_df['Open'] = 0.0
        for i in range(len(df)):
            if i == 0:
                ha_df.iloc[i, ha_df.columns.get_loc('Open')] = (df['Open'].iloc[i] + df['Close'].iloc[i]) / 2
            else:
                ha_df.iloc[i, ha_df.columns.get_loc('Open')] = (ha_df['Open'].iloc[i-1] + ha_df['Close'].iloc[i-1]) / 2

        ha_df['High'] = pd.concat([df['High'], ha_df['Open'], ha_df['Close']], axis=1).max(axis=1)
        ha_df['Low'] = pd.concat([df['Low'], ha_df['Open'], ha_df['Close']], axis=1).min(axis=1)

        ema9 = ha_df['Close'].ewm(span=9, adjust=False).mean()

        last_candle_time = ha_df.index[-1].to_pydatetime()
        now = datetime.now(last_candle_time.tzinfo)

        # If last candle timestamp is "future" relative to now → use -2
        if last_candle_time > now:
            i = -2   # last completed candle
        else:
            i = -1   # forming candle

        signal_price = ha_df['Close'].iloc[i]

        try:
            ema_diff = ema9.iloc[i] - ema9.iloc[i-1]
            angle = math.degrees(math.atan(ema_diff))
        except IndexError:
            logging.error(f"[{ticker}] Not enough candles for angle calculation.")
            return
        if data.empty or "Volume" not in data.columns:
            logging.warning(f"[{ticker}] No volume data available")

        data = data[~data.index.duplicated(keep="last")]
        data["VMA_5"] = data["Volume"].rolling(window=5).mean()
        latest_volume = data["Volume"].iloc[-1]
        latest_vma5 = data["VMA_5"].iloc[-1]

        if hasattr(latest_volume, "item"):
            latest_volume = latest_volume.item()
        if hasattr(latest_vma5, "item"):
            latest_vma5 = latest_vma5.item()

        if pd.notnull(latest_volume) and pd.notnull(latest_vma5):
            if latest_volume >= 2 * latest_vma5:
                Vol = True
            else:
                #logging.info(f"[{ticker}] No volume breakout: Volume={latest_volume}, VMA_5={latest_vma5}")
                Vol = False
            

        threshold = TA.Angle.get_angle_threshold(signal_price)
        strong_green = ha_df['Close'].iloc[i-1] > ha_df['Open'].iloc[i-1] and ha_df['Open'].iloc[i-1] == ha_df['Low'].iloc[i-1]
        can_buy = strong_green and angle >= threshold 

        if ticker not in buy_triggered:
            buy_triggered[ticker] = False

        if can_buy and not buy_triggered[ticker] and Vol:
            signal_time = ha_df.index[i].strftime('%Y-%m-%d %H:%M')
            current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open("buy_tickers.txt", "a") as f:
                f.write(f"{ticker},{signal_price:.2f},{signal_time},{current_time_str},{i}\n")
        
            buy_triggered[ticker] = True
        else:
            pass
            #logging.info(f"[{ticker}] No signal or already triggered.")
    else:
        pass
        #logging.info(f" Skipping analysis for {ticker}.")
    
    now = datetime.now().strftime("%H:%M")
    if "08:25" <= now <= "08:35":  # 8:30 AM range
        open(log_file_path, "w").close()
        open("buy_tickers.txt", "w").close()

# --- Utility ---
def wait_until_next_15_min(buffer_seconds=0):
    now = datetime.now()
    #V.is_volume_breakout()
    # Get to the next 15-minute boundary
    next_time = (now + timedelta(minutes=15))
    next_time = next_time.replace(second=0, microsecond=0)
    next_time -= timedelta(minutes=next_time.minute % 15)

    # Add buffer (e.g., 30 seconds) to ensure the candle is fully formed
    next_time += timedelta(seconds=buffer_seconds)

    wait_seconds = (next_time - now).total_seconds()
    logging.info(f"Waiting {int(wait_seconds)}s until next cycle at {next_time.strftime('%H:%M:%S')}")
    tm.sleep(wait_seconds)
# Wait for 1 min!!
def wait_until_next_1_min():
    now = datetime.now()
    next_time = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    next_time -= timedelta(minutes=next_time.minute % 1)
    wait_seconds = (next_time - now).total_seconds()
    logging.info(f"Waiting {int(wait_seconds)}s until next cycle at {next_time.strftime('%H:%M:%S')}")
    tm.sleep(wait_seconds)
#nohup pytnon3 -u script.py &
#ps aux | grep python3
#kill  PID
#pkill -f python'''
