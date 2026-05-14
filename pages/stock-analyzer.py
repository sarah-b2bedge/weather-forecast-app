import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.title("Stock Analyzer")
stock_code = st.text_input("Enter stock tickers (comma-separated): ", value="")

if stock_code:
    tickers = [t.strip().upper() for t in stock_code.split(',')]

    stocks_data = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info

        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        previous_close = info.get('previousClose', 0)

        if previous_close > 0:
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100
        else:
            change = 0
            change_percent = 0

        volume = info.get('volume', 0)
        market_cap = info.get('marketCap', 0)
        week_52_high = info.get('fiftyTwoWeekHigh', 0)
        week_52_low = info.get('fiftyTwoWeekLow', 0)

        stocks_data.append({
            'ticker': ticker,
            'price': current_price,
            'change': change,
            'change_percent': change_percent,
            'volume': volume,
            'market_cap': market_cap,
            'week_52_high': week_52_high,
            'week_52_low': week_52_low
        })

    st.subheader("Stock Market Data")

    data_dict = {}

    for stock in stocks_data:
        price_str = f"${stock['price']:.2f}"
        change_str = f"{'+' if stock['change'] >= 0 else ''}{stock['change']:.2f}"
        change_pct_str = f"{'+' if stock['change_percent'] >= 0 else ''}{stock['change_percent']:.2f}%"

        volume_str = f"{stock['volume'] / 1_000_000:.1f}M" if stock['volume'] > 0 else "N/A"

        if stock['market_cap'] >= 1_000_000_000_000:
            market_cap_str = f"${stock['market_cap'] / 1_000_000_000_000:.2f}T"
        elif stock['market_cap'] >= 1_000_000_000:
            market_cap_str = f"${stock['market_cap'] / 1_000_000_000:.2f}B"
        elif stock['market_cap'] >= 1_000_000:
            market_cap_str = f"${stock['market_cap'] / 1_000_000:.2f}M"
        else:
            market_cap_str = "N/A"

        data_dict[stock['ticker']] = [price_str, change_str, change_pct_str, volume_str, market_cap_str]


    data_matrix = pd.DataFrame(
        data_dict,
        index=["Price", "Change", "Change%", "Volume", "Market Cap"],
    )
    data_matrix = data_matrix.T
    st.table(data_matrix, border="horizontal")


    st.subheader("\n52-Week Range:")
    range_dict = {}
    for stock in stocks_data:
        if stock['week_52_low'] > 0 and stock['week_52_high'] > 0:
            range_dict[stock['ticker']] = [f"${stock['week_52_low']:.2f}", f"${stock['week_52_high']:.2f}"]

    range_matrix = pd.DataFrame(
        range_dict,
        index=["Low", "High"],
    )
    range_matrix = range_matrix.T
    st.table(range_matrix, border="horizontal")

    st.text("")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    st.text(f"\nLast Updated: {now} EST")

