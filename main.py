import pandas as pd
from strategy import analyze
from data_adapter import load_csv
from notifier import send_telegram

def main():
    df = load_csv("data/sample.csv")
    signal = analyze("DEMO", df)

    if signal is None:
        print("NO SETUP")
        return

    print("\n=== SIGNAL ===")
    for key, value in signal.items():
        print(f"{key}: {value}")

    send_telegram(signal)

if __name__ == "__main__":
    main()
