"""Optional helper: download BTC/USDT daily candles from Binance into a NEW file,
btc_binance_daily_refetched.csv, to check where data/btc_binance_daily.csv came from.

The notebooks use the frozen file in data/. Do not overwrite it: a refreshed series
changes the Table 9 numbers.

Usage:
    pip install requests pandas
    python fetch_btc_data.py
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pandas as pd
import requests

BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"
SYMBOL = "BTCUSDT"
INTERVAL = "1d"
OUTPUT_PATH = Path("btc_binance_daily_refetched.csv")


def fetch_all_daily_klines(symbol: str, interval: str) -> pd.DataFrame:
    """Page through Binance's public klines endpoint from the earliest
    available bar to now, 1000 rows per request (the API's per-call limit)."""
    all_rows = []
    start_time = 0  # 0 = let Binance return from the earliest available bar
    while True:
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": 1000,
            "startTime": start_time,
        }
        response = requests.get(BINANCE_KLINES_URL, params=params, timeout=30)
        response.raise_for_status()
        rows = response.json()
        if not rows:
            break
        all_rows.extend(rows)
        last_close_time = rows[-1][6]
        start_time = last_close_time + 1
        if len(rows) < 1000:
            break

    columns = [
        "open_time", "Open", "High", "Low", "Close", "Volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote", "ignore",
    ]
    df = pd.DataFrame(all_rows, columns=columns)
    df["Date"] = pd.to_datetime(df["open_time"], unit="ms").dt.strftime("%Y-%m-%d")
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]].astype(
        {"Open": float, "High": float, "Low": float, "Close": float, "Volume": float}
    )
    return df


def main() -> None:
    access_time = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    df = fetch_all_daily_klines(SYMBOL, INTERVAL)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Retrieved {len(df)} daily rows for {SYMBOL} from {BINANCE_KLINES_URL}")
    print(f"Date range: {df['Date'].iloc[0]} to {df['Date'].iloc[-1]}")
    print(f"Access time: {access_time}")
    print(f"Saved to: {OUTPUT_PATH.resolve()}")
    print()


if __name__ == "__main__":
    main()
