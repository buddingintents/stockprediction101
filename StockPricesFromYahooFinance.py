import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import numpy as np

st.set_page_config(page_title="Ankit's Stock Price Watcher App")
st.title("Ankit's Stock Price Watcher App")
st.header("Create a streamlit app using python that extracts stock price data from yahoo finance using a ticker input in text box, add data ranges selection, create a candle stick chart for last 30 days, add SMA 50 days & SMA 100 days lines to candle stick chart, create a table for average return and standard deviation of return for last 90 days and also add RSI chart. Update the data on ticker change.")

# Sidebar for ticker input and date range
st.sidebar.header("Stock Price Analysis")
ticker_symbol = st.sidebar.text_input("Enter a Stock Ticker (e.g., AAPL, MSFT):", value="AAPL")

start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

if ticker_symbol:
    # Fetch data from Yahoo Finance
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

    if not stock_data.empty:
        # Ensure the index is in datetime format
        stock_data.index = pd.to_datetime(stock_data.index)

        # Display stock data
        st.write(f"Stock Data for {ticker_symbol}")
        st.dataframe(stock_data.tail(10))

        # Line Chart with markers for last 30 days
        last_30_days_data = stock_data[-30:]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=last_30_days_data.index, y=last_30_days_data['Close'],
            mode='lines+markers', name='Close Price'
        ))

        # Add SMA lines
        last_30_days_data['SMA_50'] = last_30_days_data['Close'].rolling(window=50).mean()
        last_30_days_data['SMA_100'] = last_30_days_data['Close'].rolling(window=100).mean()
        fig.add_trace(go.Scatter(x=last_30_days_data.index, y=last_30_days_data['SMA_50'], mode='lines', name='SMA 50'))
        fig.add_trace(go.Scatter(x=last_30_days_data.index, y=last_30_days_data['SMA_100'], mode='lines', name='SMA 100'))

        st.write("Line Chart with SMA (50 & 100 Days)")
        st.plotly_chart(fig)

        # Compute returns and statistics for last 90 days
        stock_data['Daily Return'] = stock_data['Close'].pct_change()
        last_90_days_data = stock_data[-90:]
        avg_return = last_90_days_data['Daily Return'].mean()
        std_return = last_90_days_data['Daily Return'].std()

        st.write("## Statistics for Last 90 Days")
        st.table({"Average Daily Return": [avg_return], "Standard Deviation of Return": [std_return]})

        # RSI Calculation
        delta = stock_data['Close'].diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        stock_data['RSI'] = rsi

        st.write("## RSI (Relative Strength Index)")
        rsi_fig = go.Figure()
        rsi_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['RSI'], mode='lines', name='RSI'))
        st.plotly_chart(rsi_fig)
    else:
        st.error("No data found for the ticker symbol. Please check the input.")
