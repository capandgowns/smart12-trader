import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime

# Login System
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

def login():
    st.title("🚀 Smart12Trader - Private")
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        users = {"Suresh": "Sure7383", "Sonu": "Sonu7786", "Vikram": "Vik2026##", "admin": "Vik2026##"}
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome {username}!")
            st.rerun()
        else:
            st.error("Invalid login")

if not st.session_state.logged_in:
    login()
else:
    st.title(f"Smart12Trader - {st.session_state.username}")
    st.sidebar.success(f"Logged in: {st.session_state.username}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    capital = st.sidebar.number_input("Capital (₹)", value=50000)

    base_stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
                   'BHARTIARTL.NS', 'SBIN.NS', 'HINDUNILVR.NS', 'ITC.NS', 'BAJFINANCE.NS',
                   'AXISBANK.NS', 'LT.NS', 'SUNPHARMA.NS', 'TRENT.NS', 'POWERGRID.NS']

    def get_data(sym):
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period="1y")
            if hist.empty or len(hist) < 20:
                return None, None
            return hist, ticker.info
        except:
            return None, None

    tab1, tab2, tab3 = st.tabs(["📊 Today's Top", "🔍 Scanner", "📈 Chart"])

    with tab1:
        st.subheader(f"Top Recommendations ({datetime.now().strftime('%d %b %Y')})")
        results = []
        for sym in base_stocks:
            hist, info = get_data(sym)
            if hist is None or hist.empty:
                continue
            close = hist['Close']
            curr = close.iloc[-1]
            ret1y = ((curr / close.iloc[0]) - 1) * 100
            rsi = ta.rsi(close).iloc[-1] if len(close) > 14 else 50
            score = round(65 + (ret1y * 0.4) - (rsi - 50) * 0.3, 1)
            signal = "🟢 STRONG BUY" if score > 75 else "🟡 BUY" if score > 65 else "HOLD"
            results.append({
                'Stock': sym.replace('.NS', ''),
                'Price': round(curr, 2),
                'Score': score,
                'Signal': signal,
                '1Y %': round(ret1y, 1),
                'RSI': round(rsi, 1)
            })
        
        if results:
            df = pd.DataFrame(results).sort_values('Score', ascending=False)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("Market data abhi load nahi ho raha. Thodi der baad try karo.")

    with tab2:
        st.subheader("Stock Scanner")
        st.info("Yahan advanced filters aayenge future mein.")

    with tab3:
        stock = st.selectbox("Stock Chart", [s.replace('.NS','') for s in base_stocks])
        hist, _ = get_data(stock + ".NS")
        if hist is not None and not hist.empty:
            fig = go.Figure(data=[go.Candlestick(x=hist.index,
                        open=hist['Open'], high=hist['High'],
                        low=hist['Low'], close=hist['Close'])])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Chart data abhi available nahi.")

    st.caption("Private App for 3 Friends")
