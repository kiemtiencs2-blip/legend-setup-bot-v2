import pandas as pd
from indicators import add_indicators, atr
from config import MIN_SCORE, MIN_RR

def _trend(x):
    last = x.iloc[-1]
    if last["ma20"] > last["ma50"] and last["close"] > last["ma20"]:
        return "BULLISH"
    if last["ma20"] < last["ma50"] and last["close"] < last["ma20"]:
        return "BEARISH"
    return "NEUTRAL"

def _liquidity(x, lookback=20):
    w = x.tail(lookback)
    return float(w["low"].min()), float(w["high"].max())

def _sweep_and_mss(x, side):
    if len(x) < 12:
        return False, False
    prev = x.iloc[-7:-1]
    last = x.iloc[-1]
    if side == "LONG":
        sweep = last["low"] < prev["low"].min() and last["close"] > prev["low"].min()
        mss = last["close"] > x.iloc[-7:-1]["high"].max()
    else:
        sweep = last["high"] > prev["high"].max() and last["close"] < prev["high"].max()
        mss = last["close"] < x.iloc[-7:-1]["low"].min()
    return bool(sweep), bool(mss)

def _retest(x, side):
    if len(x) < 5:
        return False
    last = x.iloc[-1]
    prev = x.iloc[-5:-1]
    if side == "LONG":
        return bool(last["low"] <= prev["high"].max() and last["close"] > last["open"])
    return bool(last["high"] >= prev["low"].min() and last["close"] < last["open"])

def analyze(symbol: str, df: pd.DataFrame):
    x = add_indicators(df).dropna().reset_index(drop=True)
    if len(x) < 60:
        return None

    trend = _trend(x)
    side = "LONG" if trend == "BULLISH" else "SHORT" if trend == "BEARISH" else None
    if side is None:
        return None

    last = x.iloc[-1]
    support, resistance = _liquidity(x)
    sweep, mss = _sweep_and_mss(x, side)
    retest = _retest(x, side)
    volume = bool(last["volume"] > last["vol_ma20"])
    rsi = bool(45 <= last["rsi"] <= 70) if side == "LONG" else bool(30 <= last["rsi"] <= 55)

    score = 25 + (20 if sweep else 0) + (25 if mss else 0) + (15 if retest else 0) + (10 if volume else 0) + (5 if rsi else 0)
    if score < MIN_SCORE or not (sweep and mss and retest):
        return None

    volatility = atr(x)
    entry = float(last["close"])
    if side == "LONG":
        sl = min(support, entry - 1.2 * volatility)
        tp1 = entry + 1.5 * (entry - sl)
        tp2 = resistance
        rr = (tp2 - entry) / max(entry - sl, 1e-9)
    else:
        sl = max(resistance, entry + 1.2 * volatility)
        tp1 = entry - 1.5 * (sl - entry)
        tp2 = support
        rr = (entry - tp2) / max(sl - entry, 1e-9)

    if rr < MIN_RR or (side == "LONG" and tp2 <= entry) or (side == "SHORT" and tp2 >= entry):
        return None

    grade = "A+" if score >= 90 else "A"
    return {
        "symbol": symbol, "direction": side, "grade": grade, "score": score,
        "entry": round(entry, 4), "stop_loss": round(sl, 4),
        "take_profit_1": round(tp1, 4), "take_profit_2": round(tp2, 4),
        "rr": round(rr, 2), "trend": trend,
        "liquidity_sweep": sweep, "mss": mss, "retest": retest,
        "volume_confirmation": volume, "rsi_confirmation": rsi,
    }
