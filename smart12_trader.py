import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime

# ===================== LOGIN SYSTEM =====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("🚀 Smart12Trader - Private App")
    st.subheader("Login for Friends")
    
    col1, col2 = st.columns([1,2])
    with col1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary"):
            # 3 Friends + Admin
            users = {
                "Suresh": "Sure7383",   # dost 1
                "Sonu": "Sonu7786",   # dost 2
                "Vik": "Vik2026##",   # dost 3
                "admin": "Vik2026##"
            }
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Galat username ya password")

    st.info("Admin: admin / admin123\nFriend1: friend1 / pass123 (example)")

if not st.session_state.logged_in:
    login_page()
else:
    # ================= MAIN APP =================
    st.title(f"Smart12Trader - Welcome {st.session_state.username}")
    
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    capital = st.sidebar.number_input("Your Capital (₹)", value=50000, min_value=10000)
    st.sidebar.write("---")
    st.sidebar.write("Only for 3 Friends")

    base_stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
                   'BHARTIARTL.NS', 'SBIN.NS', 'HINDUNILVR.NS', 'ITC.NS', 'BAJFINANCE.NS',
                   'AXISBANK.NS', 'LT.NS', 'SUNPHARMA.NS', 'TRENT.NS', 'POWERGRID.NS']

    def get_stock_data(sym):
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period="1y")
            if hist.empty or len(hist) < 30:
                hist = ticker.history(period="6mo")
            if hist.empty or len(hist) < 20:
                return None, None
            return hist, ticker.info
        except:
            return None, None

    tab1, tab2, tab3 = st.tabs(["📊 Today's Top", "🔍 Scanner", "📈 Details"])

    with tab1:
        st.subheader(f"Auto Top Recommendations - {datetime.now().strftime('%d %b %Y')}")
        results = []
        for sym in base_stocks:
            hist, info = get_stock_data(sym)
            if hist is None or hist.empty:
                continue
            close = hist['Close']
            current = close.iloc[-1]
            ret1y = ((current / close.iloc[0]) - 1) * 100
            ret3m = ((current / close.iloc[-63]) - 1) * 100 if len(close) > 63 else 0
            rsi = ta.rsi(close).iloc[-1] if len(close) > 14 else 50
            
            pe = info.get('trailingPE', 999)
            fund = max(40, 95 - pe*1.2) if pe < 999 else 50
            tech = 80 if 35 < rsi < 68 else 45
            score = round(fund*0.45 + tech*0.35 + (ret3m*0.2), 1)
            
            signal = "🟢 STRONG BUY" if score >= 78 else "🟡 BUY" if score >= 68 else "HOLD"
            
            results.append({'Stock': sym.replace('.NS',''), 'Price': round(current,2), 
                          'Score': score, 'Signal': signal, '1Y%': round(ret1y,1), 'RSI': round(rsi,1)})
        
        if results:
            df = pd.DataFrame(results).sort_values('Score', ascending=False)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("Data loading...")

    with tab2:
        st.subheader("Stock Scanner")
        selected = st.multiselect("Select Stocks", [s.replace('.NS','') for s in base_stocks], default=base_stocks[:8])
        # Simple filter logic
        st.write("Selected stocks analysis coming...")

    with tab3:
        stock = st.selectbox("Choose Stock for Chart", [s.replace('.NS','') for s in base_stocks])
        hist, _ = get_stock_data(stock + ".NS")
        if hist is not None:
            fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            st.plotly_chart(fig, use_container_width=True)

    st.caption("Private App for 3 Friends | Updates by Admin")
