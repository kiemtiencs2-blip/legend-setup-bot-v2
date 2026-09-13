import pandas as pd

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    required = {"open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    return df.dropna().reset_index(drop=True)

# Live market-data adapters should be implemented here.
# Keep the source separate from strategy.py so the strategy can be
# tested/backtested without touching broker accounts.
