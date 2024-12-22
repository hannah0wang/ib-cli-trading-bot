import asyncio
from ib_insync import IB
import streamlit as st

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop" in str(ex) or "Event loop is closed" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

def setup_ib_connection(port=4001, client_id=1):
    loop = get_or_create_eventloop()
    asyncio.set_event_loop(loop)
    ib = IB()

    if not ib.isConnected():
        try:
            ib.connect('127.0.0.1', port, clientId=client_id)
        except Exception as e:
            st.error(f"Could not connect to IB Gateway: {e}")
            st.stop()
    return ib

def portfolio_items(ib):
    """Fetch portfolio items and format them into a DataFrame."""
    import pandas as pd
    portfolio = ib.portfolio()
    items = [
        {
            'symbol': item.contract.symbol,
            'position': item.position,
            'avg_cost': item.averageCost,
            'market_price': item.marketPrice,
            'market_value': item.marketValue,
            'unrealized_pnl': item.unrealizedPNL,
        }
        for item in portfolio
    ]
    return pd.DataFrame(items)
