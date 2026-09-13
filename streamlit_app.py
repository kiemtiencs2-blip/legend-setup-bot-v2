import streamlit as st
import pandas as pd
from strategy import analyze

st.set_page_config(page_title="Legend Setup Bot v2", page_icon="🎯", layout="wide")
st.title("🎯 Legend Setup Bot v2")
st.caption("BOT MỚI • ĐỘC LẬP • PRICE ACTION / MARKET STRUCTURE")

st.markdown("**HTF Bias → Liquidity → Sweep → MSS → Retest → Entry → SL → TP**")
st.warning("Signal-only: bot không tự đặt lệnh. Dữ liệu mặc định là mẫu để kiểm thử giao diện.")

uploaded = st.file_uploader("Upload dữ liệu OHLCV (.csv)", type=["csv"])
df = pd.read_csv(uploaded) if uploaded else pd.read_csv("data/sample.csv")
symbol = st.text_input("Mã cổ phiếu", "NVDA")

if st.button("🎯 TÌM SETUP A / A+", use_container_width=True):
    try:
        signal = analyze(symbol, df)
        if signal is None:
            st.info("⚪ NO TRADE — chưa đủ toàn bộ điều kiện.")
        else:
            st.success(f"{'🟢 LONG' if signal['direction'] == 'LONG' else '🔴 SHORT'} — {signal['symbol']} — {signal['grade']}")
            cols = st.columns(5)
            cols[0].metric("Score", f"{signal['score']}/100")
            cols[1].metric("Entry", signal["entry"])
            cols[2].metric("SL", signal["stop_loss"])
            cols[3].metric("TP1", signal["take_profit_1"])
            cols[4].metric("TP2", signal["take_profit_2"])
            st.write(f"**R:R:** 1:{signal['rr']}  |  **HTF:** {signal['trend']}")
            checks = {
                "Liquidity Sweep": signal["liquidity_sweep"],
                "MSS": signal["mss"],
                "Retest": signal["retest"],
                "Volume": signal["volume_confirmation"],
                "RSI": signal["rsi_confirmation"],
            }
            st.subheader("Xác nhận")
            st.write("  ".join(f"{'✅' if v else '❌'} {k}" for k, v in checks.items()))
    except Exception as exc:
        st.error(f"Lỗi dữ liệu: {exc}")

with st.expander("Luật bot"):
    st.markdown("""
**Không có Sweep + MSS + Retest = không trade.**

- Bias khung lớn phải rõ.
- Chờ thanh khoản bị quét.
- Chờ market structure shift.
- Chờ retest thay vì đuổi giá.
- SL theo cấu trúc/ATR.
- TP1 theo R:R, TP2 theo liquidity đối diện.
- Chỉ báo A/A+ khi đủ điều kiện.
""")
