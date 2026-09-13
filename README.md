# Legend Stock Setup Bot

Bot mới hoàn toàn, độc lập với mọi bot khác.

## Chiến lược
1. HTF trend
2. Key level / support / resistance
3. Liquidity sweep
4. Market Structure Shift (MSS)
5. Confirmation bằng volume + RSI
6. Entry zone
7. Stop loss theo cấu trúc
8. Take profit theo swing/resistance
9. Chỉ phát tín hiệu khi R:R đạt ngưỡng

Bot mặc định là **signal-only**: không tự đặt lệnh.

## Chạy thử
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Dữ liệu mẫu nằm trong `data/sample.csv`.

## Quan trọng
Bản này chưa giả mạo dữ liệu Trade Republic/LS Exchange. Adapter dữ liệu được tách riêng để sau này nối nguồn giá phù hợp. Telegram cũng là module tùy chọn và không chứa token thật.
