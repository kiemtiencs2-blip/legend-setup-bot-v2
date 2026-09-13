import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def format_signal(signal: dict) -> str:
    emoji = "🟢" if signal["direction"] == "LONG" else "🔴"
    return (
        f"{emoji} {signal['direction']} — {signal['symbol']}\n"
        f"Score: {signal['score']}/100\n"
        f"Entry: {signal['entry']}\n"
        f"SL: {signal['stop_loss']}\n"
        f"TP: {signal['take_profit']}\n"
        f"R:R: 1:{signal['rr']}\n"
        f"Trend: {signal['trend']}\n"
        f"Liquidity: {'OK' if signal['liquidity_sweep'] else 'NO'}\n"
        f"MSS: {'OK' if signal['mss'] else 'NO'}\n"
        f"Volume: {'OK' if signal['volume_confirmation'] else 'NO'}\n"
        f"RSI: {'OK' if signal['rsi_confirmation'] else 'NO'}"
    )

def send_telegram(signal: dict):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": format_signal(signal),
    }, timeout=15)
