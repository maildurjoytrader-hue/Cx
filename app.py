import streamlit as st
import streamlit.components.v1 as components

# Page Layout Configuration
st.set_page_config(page_title="PRO AI Crypto Trading Workspace", layout="wide", page_icon="📈")

st.title("⚡ PRO AI Crypto Interactive Multi-Chart Workspace")
st.markdown("### Powered by TradingView Advanced Real-Time Analytics Engine")

# Crypto Market Ticker Tape Widget (Top Bar)
ticker_html = """
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [
    {"proName": "BINANCE:BTCUSDT", "title": "Bitcoin"},
    {"proName": "BINANCE:ETHUSDT", "title": "Ethereum"},
    {"proName": "BINANCE:SOLUSDT", "title": "Solana"},
    {"proName": "BINANCE:BNBUSDT", "title": "Binance Coin"},
    {"proName": "BINANCE:XRPUSDT", "title": "XRP"}
  ],
  "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": false, "displayMode": "adaptive", "locale": "en"
}
  </script>
</div>
"""
components.html(ticker_html, height=50)

st.markdown("---")

# Layout Columns
left_col, right_col = st.columns([1, 3])

with left_col:
    st.subheader("⚙️ Control Panel")
    
    # Asset Selection
    selected_asset = st.selectbox(
        "🔥 Choose Trading Pair:",
        ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGE-USD", "LINKUSDT"],
        index=0
    )
    
    # Timeframe Selection
    selected_tf = st.selectbox(
        "⏳ Chart Timeframe:",
        ["1", "5", "15", "60", "240", "D"],
        format_func=lambda x: "1 Minute" if x=="1" else "5 Minutes" if x=="5" else "15 Minutes" if x=="15" else "1 Hour" if x=="60" else "4 Hours" if x=="240" else "1 Day",
        index=2
    )
    
    st.markdown("---")
    
    # Technical Gauge Widget (Side Panel Analytics)
    gauge_html = f"""
    <div class="tradingview-widget-container" style="margin-top:20px;">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{
      "interval": "{selected_tf if selected_tf != 'D' else '1d'}",
      "width": "100%", "isTransparent": false, "height": 380,
      "symbol": "BINANCE:{selected_asset}", "showIntervalTabs": true,
      "displayMode": "single", "locale": "en", "theme": "dark"
    }}
      </script>
    </div>
    """
    components.html(gauge_html, height=400)

with right_col:
    st.subheader(f"📈 Live Interactive Advanced Chart: {selected_asset}")
    
    # Main Technical Analysis Chart Widget
    tv_symbol = f"BINANCE:{selected_asset}"
    chart_html = f"""
    <div class="tradingview-widget-container" style="height:600px;width:100%;">
      <div id="tradingview_advanced_chart" style="height:600px;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true,
        "symbol": "{tv_symbol}",
        "interval": "{selected_tf}",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#131722",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "details": true,
        "hotlist": true,
        "calendar": true,
        "studies": [
          "RSI@tv-basicstudies",
          "MASimple@tv-basicstudies"
        ],
        "container_id": "tradingview_advanced_chart"
      }});
      </script>
    </div>
    """
    components.html(chart_html, height=610)
