import streamlit as st
import pandas as pd
import requests

# আপনার API Key
GEMINI_API_KEY = "AIzaSyDmrHoPXjfyIjt4gmMnYj4TIrn3KQ3GWOo"

def get_trend_signal(pair):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={pair}"
    try:
        data = requests.get(url).json()
        price = float(data['lastPrice'])
        change = float(data['priceChangePercent'])
        
        # Advance AI Prompt for Future Trending
        prompt = f"""
        Act as a professional Crypto Future Trader. 
        Token: {pair}, Current Price: {price}, 24h Change: {change}%.
        Analyze the trend bias. If the trend is clearly bullish or bearish, output a signal.
        If the market is choppy or uncertain, output "NO_TREND_WAIT".
        
        Format:
        TREND: [BULLISH / BEARISH / NO_TREND_WAIT]
        ENTRY: [Price to enter]
        TP: [Take Profit Price]
        SL: [Stop Loss Price]
        LEVERAGE: [Suggested Leverage 5x-20x]
        """
        
        ai_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        res = requests.post(ai_url, json={"contents": [{"parts": [{"text": prompt}]}]}).json()
        return res['candidates'][0]['content']['parts'][0]['text']
    except:
        return "TREND: ERROR\nREASON: Data unavailable"

st.title("📈 Advanced Future Trend Analyzer")
pair = st.selectbox("Select Pair", ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"])

if st.button("Analyze Trend"):
    signal = get_trend_signal(pair)
    st.markdown(f"### 🤖 AI Trend Report:\n```\n{signal}\n```")
    st.warning("⚠️ ফিউচার ট্রেডিংয়ে ঝুঁকি অনেক বেশি। সর্বদা SL ব্যবহার করবেন।")
        
