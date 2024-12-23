import asyncio
import streamlit as st
from components.PositionsTable import PositionsTable
from components.PositionsChart import PositionsChart
from components.StockChart import StockChart
import yfinance as yf
import pandas as pd

st.set_page_config(
    layout="wide",
    page_title="My Dashboard"
)

# Create or get the event loop
def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop

# Ensure event loop is created before using ib_insync
loop = get_or_create_eventloop()
asyncio.set_event_loop(loop)

# Initialize IB instance.
# Using ib_insync with Streamlit presents challenges because ib_insync relies on an asynchronous event loop, 
# which conflicts with Streamlit's synchronous execution model. to combat this, we run an event loop at the 
# beginning of the page before importing the ib_insync library
from ib_insync import IB, Stock, util
ib = IB()

# Ensure IB is connected
if not ib.isConnected():
    try:
        ib.connect(
            "127.0.0.1",  # IB Gateway or TWS IP address
            4001,         # Port for live trading or paper trading
            clientId=1,   # Unique client ID
            timeout=5
        )
    except ConnectionRefusedError:
        st.info("Open IB Gateway and log in.")
        if st.button("Press here after done"):
            st.stop()
    except RuntimeError:
        loop = get_or_create_eventloop()
        asyncio.set_event_loop(loop)
    except TimeoutError:
        st.warning("Connection timed out. Please retry.")

def portfolio_items(ib):  
    def create_portfolio_item(item):  
        cds = ib.reqContractDetails(item.contract)[0]  
        perc_change = (item.marketPrice / item.averageCost - 1) * 100  
        if item.position < 0:  
            perc_change = (item.averageCost / item.marketPrice - 1) * 100  

        return {
            'contract': item.contract,
            'symbol': item.contract.symbol,
            'name': cds.longName,
            'position': item.position,
            'avg_cost': item.averageCost,
            'market_price': item.marketPrice,
            'market_value': item.marketValue,
            'perc_change': perc_change,
            'unrealized_pnl': item.unrealizedPNL,
            'realized_pnl': item.realizedPNL
        }
    
    _portfolio_items = ib.portfolio()
    items_dicts = [create_portfolio_item(item) for item in _portfolio_items]
    df = pd.DataFrame.from_records(items_dicts)
    return df

# Fetch historical data for a symbol from IB or fallback to Yahoo Finance if no subscription
def fetch_historical_data(ib, symbol, exchange, duration='5 Y', bar_size='1 day'):
    try:
        contract = Stock(symbol=symbol, exchange=exchange)
        bars = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr=duration,
            barSizeSetting=bar_size,
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1
        )
        
        bars_df = pd.DataFrame(util.df(bars))
        if not bars_df.empty:
            return bars_df
    except Exception as e:
        print(f"Error fetching data from IB for {symbol}: {e}")
    
    # Fallback to Yahoo Finance
    print(f"Falling back to Yahoo Finance for {symbol}.")
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=duration)
    df = df.reset_index()
    df.rename(columns={
        'Date': 'date', 'Open': 'open', 'High': 'high',
        'Low': 'low', 'Close': 'close', 'Volume': 'volume'
    }, inplace=True)
    return df


with st.container():
    col1, col2 = st.columns([5, 3])

    portfolio_df = portfolio_items(ib)

    PositionsTable.show_table(col1, portfolio_df)
    PositionsChart.show_chart(col2, portfolio_df)
    
    for index, row in portfolio_df.iterrows():
        symbol = row['symbol']
        exchange = row['contract'].primaryExchange
        # st.write(f"Fetching historical data for {symbol}...")
        
        # Fetch historical data for each symbol
        historical_df = fetch_historical_data(ib, symbol, exchange)
        if not historical_df.empty:
            st.write(f"Historical data for {symbol}:")
            st.dataframe(historical_df.head())

        StockChart.show_chart(col2, symbol)