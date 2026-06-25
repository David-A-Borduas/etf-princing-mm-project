# all functions annotations are stored as strings automatically so they are not evaluated at the function definition time.
from __future__ import annotations
# pathlib is a built-in library that provides a path object that represents a file or directory path.
from pathlib import Path

import pandas as pd
import yfinance as yf

from src import config

def _cache_path(ticker: str) -> Path:
    """Return the cache path for a given ticker. You hand it a ticker, it hands you back the full file path where that ticker should be saved."""
    safe = ticker.replace("^", "").upper()
    return config.RAW_DIR / f"{safe}.parquet"
# The rule of thumb worth internalizing: parquet for the data your code reads and writes; 
# CSV only when a human needs to open the file directly (or when you're handing data to someone whose tools demand CSV).

def fetch_one(ticker: str, *, auto_adjust: bool = False, start: str | None = None, end: str | None = None, force: bool = False) -> pd.DataFrame:
    """Download one series and cache it as parquet. Re-reads cache unless force=True."""
# Everything after the * are keyword-only arguments. They are not required, but if you provide them, you must provide them by name to not 
# confuse them with the positional arguments.
# force is the switch that decides one thing: when you call the function, should it download fresh data, or just reuse the file it saved last time?
# auto_adjust controls whether Yahoo hands you the raw historical prices that actually printed,
# or prices that have been mathematically rewritten to account for dividends and splits. For this project, 
# that distinction is the difference between a correct premium/discount series and a quietly broken one — so it's worth understanding properly.
    
    # If the user didn't provide a start or end date, use the default start and end dates from the config.
    start = start or config.START_DATE
    end = end or config.END_DATE
    # Get the full file path where the data should be saved.
    path = _cache_path(ticker)
    # If the file already exists and the user didn't ask to force a re-download, read the file from the cache.
    if path.exists() and not force:
        return pd.read_parquet(path)
    # Download the data from Yahoo Finance.
    df = yf.download(ticker, start=start, end=end, auto_adjust=auto_adjust, progress=False)
    # If the data is a MultiIndex, get the second level of the columns. Makes it robust across yfinance versions.
    if isinstance(df.columns, pd.MultiIndex):
        df.colomns = df.columns.get_level_values(1)
    # If the data is empty, raise an error.
    if df.empty:
        raise ValueError(f"No data found for {ticker} between {start} and {end}")
    # Set the index name to "date" for clarity and consistency.
    df.index.name = "date"
    # Save the data to the cache.
    df.to_parquet(path)
    # Return the data.
    return df

def fetch_all(force: bool = False) -> dict[str, pd.DataFrame]:
    """Pull every ticker in config.TICKERS, each with its own auto_adjust rule."""
    results = {}
    for t, aa in config.ETF_TICKERS.items():
        df = fetch_one(t, auto_adjust=aa, force=force)
        results[t] = df
    return results

    