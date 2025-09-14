import Aanlyze_Sleep as AS
import Excel1 as EX
import logging

logging.info("🚀 Analyzer [10-20] started...")

tickers = EX.Price.list(125, 150)
tickers = [t + '.NS' for t in tickers]

while True:
    for ticker in tickers:
        AS.analyze_real_time(ticker)
    AS.wait_until_next_15_min()