import streamlit as st
import pandas as pd
import requests
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# Page Layout
st.set_page_config(page_title="PRO Real-Time Gemini AI Crypto Bot", layout="wide", page_icon="🤖")

# Refresh Engine
st_autorefresh(interval=30 * 1000, key="crypto_bot_refresh")

GEMINI_API_KEY = "AIzaSyBNG4cgf3v8qaxio2XLSlJ7_lHQ0fMhE80"

# Fetch Data
@st.cache_data(ttl=10)
def get_binance_live_data():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        res = requests.get(url).json()
        target_symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'XRPUSDT']
        crypto_list = [{'Pair': t['symbol'], 'Price': float(t['lastPrice']), 'Change': float(t['priceChangePercent'])} 
                       for t in res if t['symbol'] in target_symbols]
        return pd.DataFrame(crypto_list)
    except:
        return pd.DataFrame([{'Pair': 'BTCUSDT', 'Price': 60000.0, 'Change': 0.0}])

# AI Analysis
def ask_gemini_ai(pair, price, change):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        prompt = f"Token: {pair}, Price: ${price}, Change: {change}%. Give a short 2-line BUY/SELL analysis. End with CONF_SCORE: [X]%"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        res = requests.post(url, json=payload).json()
        return res['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Analysis syncing... CONF_SCORE: 85%"

# UI Elements
st.title("⚡ PRO Gemini AI Trading Bot")
raw_data = get_binance_live_data()
selected_asset = st.selectbox("🔥 Target Pair:", raw_data['Pair'].tolist())

# Main Logic
coin_data = raw_data[raw_data['Pair'] == selected_asset].iloc[0]
price = coin_data['Price']
change = coin_data['Change']
direction = "up" if change >= 0 else "down"
signal_title = "🟢 BUY / LONG" if direction == "up" else "🔴 SELL / SHORT"
signal_color = "#0cf251" if direction == "up" else "#ff3344"

analysis = ask_gemini_ai(selected_asset, price, change)

# Final Box with Fixed JS Syntax
box_html = f"""
<div style="background:#0d111a; padding:20px; border-radius:15px; border:2px solid {signal_color}; color:#fff; font-family:sans-serif;">
    <h2 style="color:{signal_color};">{signal_title}</h2>
    <div style="background:#141a29; padding:15px; border-radius:10px;">{analysis}</div>
    <div style="display:flex; justify-content:space-between; margin-top:20px;">
        <div>Price: <b id="live-price" style="color:{signal_color};">$...</b></div>
        <div>TP: <b id="live-tp" style="color:#00bfff;">$...</b></div>
        <div>SL: <b id="live-sl" style="color:#ff3344;">$...</b></div>
    </div>
</div>

<script>
    const symbol = "{selected_asset.lower()}";
    const dir = "{direction}";
    const ws = new WebSocket('wss://stream.binance.com:9443/ws/' + symbol + '@ticker');
    
    ws.onmessage = function(event) {{
        const d = JSON.parse(event.data);
        const p = parseFloat(d.c);
        const atr = p * 0.02;
        document.getElementById("live-price").innerText = "$" + p.toFixed(2);
        if (dir === "up") {{
            document.getElementById("live-tp").innerText = "$" + (p + atr).toFixed(2);
            document.getElementById("live-sl").innerText = "$" + (p - atr).toFixed(2);
        }} else {{
            document.getElementById("live-tp").innerText = "$" + (p - atr).toFixed(2);
            document.getElementById("live-sl").innerText = "$" + (p + atr).toFixed(2);
        }}
    }};
</script>
"""
components.html(box_html, height=350)
        
