import streamlit as st
import streamlit.components.v1 as components
import requests
import os

# API Key লোড করুন (রেন্ডার এনভায়রনমেন্ট থেকে)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

st.set_page_config(page_title="AI Pro Trading", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0b0e14; }
    .indicator-box { background-color: #161a21; padding: 20px; border-radius: 15px; border: 1px solid #333; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI-Powered Trading Dashboard")

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("AI Analysis")
    st.markdown('<div class="indicator-box">', unsafe_allow_html=True)
    
    # এআই সিগন্যাল লজিক
    if st.button("🚀 ANALYZE MARKET"):
        if not GEMINI_API_KEY:
            st.error("AIzaSyAP6uvU1ubqILNkgxtT6sZmM05m8w5RaIA")
        else:
            with st.spinner("AI প্রসেসিং করছে..."):
                prompt = "Analyze BTC market trend. Return short signal (BUY/SELL) and Confidence %."
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}).json()
                result = response['candidates'][0]['content']['parts'][0]['text']
                st.write(result)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # ট্রেডিং ভিউ চার্ট
    chart_html = """
    <div class="tradingview-widget-container">
      <div id="tradingview_chart"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
      "width": "100%", "height": 500,
      "symbol": "BINANCE:BTCUSDT",
      "interval": "5", "theme": "dark",
      "style": "1", "container_id": "tradingview_chart"
    });
    </script>
    </div>
    """
    components.html(chart_html, height=520)
        
