from pathlib import Path

def find_project_root(marker: str = "pyproject.toml") -> Path:

# --- Paths ---
PROJECT_ROOT = find_project_root()
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"