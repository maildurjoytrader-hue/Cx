import streamlit as st
import streamlit.components.v1 as components

# Page Layout Configuration
st.set_page_config(page_title="PRO AI Crypto Signals & Charts", layout="wide", page_icon="⚡")

st.title("⚡ PRO AI Crypto Intelligence Dashboard")
st.markdown("### Real-Time Live AI Trading Signals & Dynamic Chart Engine")

st.markdown("---")

# Layout Columns - split screen for Control and Signals
left_col, right_col = st.columns([1.2, 3])

with left_col:
    st.subheader("⚙️ Control Control Panel")
    
    # Asset Selection Dropdown
    selected_asset = st.selectbox(
        "🔥 Choose Trading Pair:",
        ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "LINKUSDT"],
        index=0
    )
    
    # Timeframe Selection Dropdown
    selected_tf = st.selectbox(
        "⏳ Candle Timeframe:",
        ["15m", "1h", "4h", "1d"],
        index=0
    )
    
    st.markdown("---")
    
    # Map timeframe string to TradingView Widget Values
    gauge_tf = "15m" if selected_tf == "15m" else "1h" if selected_tf == "1h" else "4h" if selected_tf == "4h" else "1d"
    
    st.subheader("🤖 Live AI Bot Signal Message")
    st.info(f"👉 Check the gauge below for the real-time **{selected_tf}** candle action alert for **{selected_asset}**.")
    
    # 🎯 THE TRADINGVIEW LIVE BUY/SELL GAUGE & MESSAGE WIDGET
    # This renders directly in the browser, bypassing Render server blocks completely!
    gauge_html = f"""
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{
      "interval": "{gauge_tf}",
      "width": "100%", "isTransparent": false, "height": 380,
      "symbol": "BINANCE:{selected_asset}", "showIntervalTabs": false,
      "displayMode": "single", "locale": "en", "theme": "dark"
    }}
      </script>
    </div>
    """
    components.html(gauge_html, height=400)

with right_col:
    st.subheader(f"📈 Real-Time Advanced Chart: {selected_asset} ({selected_tf})")
    
    # Map timeframe for the Advanced Main Chart
    tv_tf = "15" if selected_tf == "15m" else "60" if selected_tf == "1h" else "240" if selected_tf == "4h" else "D"
    tv_symbol = f"BINANCE:{selected_asset}"
    
    # Main TradingView Advanced Technical Analysis Chart
    chart_html = f"""
    <div class="tradingview-widget-container" style="height:580px;width:100%;">
      <div id="tv_advanced_chart" style="height:580px;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true, "symbol": "{tv_symbol}", "interval": "{tv_tf}",
        "timezone": "Etc/UTC", "theme": "dark", "style": "1", "locale": "en",
        "toolbar_bg": "#131722", "enable_publishing": false, "hide_side_toolbar": false,
        "allow_symbol_change": true, "details": true, "hotlist": true,
        "calendar": true,
        "studies": [
          "RSI@tv-basicstudies",
          "MASimple@tv-basicstudies"
        ], 
        "container_id": "tv_advanced_chart"
      }});
      </script>
    </div>
    """
    components.html(chart_html, height=590)
    
