from pathlib import Path

# paths (to not have to hardcode paths everywhere)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Create directories if they don't exist
RAW_DIR.mkdir(parents=True, exist_ok=True) # parents creates the whole path if it doesn't exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True) # exists_ok=True means don't raise an error if the directory already exists and just do nothing

# dates (includes COVID vol spike for stress testing)
START_DATE = "2020-01-01"
END_DATE = "2025-12-31"

# etf tickers (every ticker has auto_adjust to false to avoid adjustments for dividends, splits, etc. However, it only matters for QYLD)
ETF_TICKERS = {"^NDX": False, # Black-Scholes underlying. QYLD writes options on the Nasdaq-100 index itself, cash-settled and European. 
# This is the reason why the project is exactly correct with BS pricing as European + cash-settled on an index means no early exercise, no physical-delivery, no single-stock-dividend mess.
# The ^ prefix is Yahoo's convention for an index rather than a tradable security
    "QQQ": False, # A sanity cross-check only, never a pricing input. (Should no diverge from NDX)
    "QYLD": False, # The instrument and validation target.
    "^VXN": False, # The implied-vol input (the sigma)
    "^IRX": False, # The risk-free rate input (the r). This is the 13-week (3-month) T-bill yield, which feeds the r in BS.
}