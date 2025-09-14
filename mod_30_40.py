import Aanlyze_Sleep as AS
import Excel1 as EX
import logging
import Volume as V

logging.info("🚀 Analyzer [10-20] started...")

tickers = EX.Price.list(30, 40)
tickers = [t + '.NS' for t in tickers]

while True:
    for ticker in tickers:
        AS.analyze_real_time(ticker)
    V.is_volume_breakout()
    AS.wait_until_next_15_min()