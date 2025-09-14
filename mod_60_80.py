import Aanlyze_Sleep as AS
import Excel1 as EX
import Volume as V
import logging

logging.info("🚀 Analyzer [10-20] started...")

tickers = EX.Price.list(60, 80)
tickers = [t + '.NS' for t in tickers]

while True:
    for ticker in tickers:
        AS.analyze_real_time(ticker)
    V.is_volume_breakout()
    AS.wait_until_next_15_min()