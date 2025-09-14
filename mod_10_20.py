import Aanlyze_Sleep as AS
import Volume as V
import Excel1 as EX
import logging

logging.info("🚀 Analyzer [10-20] started...")

tickers = EX.Price.list(10, 20)
tickers = [t + '.NS' for t in tickers]

while True:
    for ticker in tickers:
        AS.analyze_real_time(tickers)
    #V.is_volume_breakout()
    AS.wait_until_next_15_min()