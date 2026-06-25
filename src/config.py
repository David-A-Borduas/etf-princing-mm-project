from pathlib import Path

def find_project_root(marker: str = "pyproject.toml") -> Path:
    """Return the project root by climbing upward from this file until a directory
    containing `marker` (e.g. pyproject.toml) is found. This anchors all paths to the
    repo's location on disk rather than the working directory, so they resolve correctly
    no matter where Python is run from. Raises FileNotFoundError if no marker is found."""
    for parent in Path(__file__).parents:
        if (parent / marker).exists():
            return parent
    raise FileNotFoundError(f"No {marker} found in any parent directory of {Path(__file__)}")

# paths (to not have to hardcode paths everywhere)
PROJECT_ROOT = find_project_root()
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# dates (includes COVID vol spike for stress testing)
START_DATE = "2020-01-01"
END_DATE = "2025-12-31"

# etf tickers (every ticker has auto_adjust to false to avoid adjustments for dividends, splits, etc. However, it only matters for QYLD)
ETF_TICKERS = {"^NDX": False, # Black-Scholes underlying. QYLD writes options on the Nasdaq-100 index itself, cash-settled and European. 
# This is the reason why the project is exactly correct with BS pricing as European + cash-settled on an index means no early exercise, no physical-delivery, no single-stock-dividend mess.
# The ^ prefix is Yahoo's convention for an index rather than a tradable security
    "QQQ": False, # A sanity cross-check only, never a pricing input. (Should no diverge from NDX)
    "QYLD": False, # The instrument and validation target.
    "^VNX": False, # The implied-vol input (the sigma)
    "IRX": False, # The risk-free rate input (the r). This is the 13-week (3-month) T-bill yield, which feeds the r in BS.
}