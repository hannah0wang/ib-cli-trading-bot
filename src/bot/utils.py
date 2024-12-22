from ib_insync import *

def fetch_account_balance(ib, currency='USD'):
    """Fetch total cash balance in the specified currency."""
    account_values = ib.accountValues()
    filtered = list(filter(lambda acc: acc.currency == currency and acc.tag == 'TotalCashBalance', account_values))
    if filtered:
        return float(filtered[0].value)
    else:
        print(f"No TotalCashBalance found for {currency}.")
        return 0.0

def is_market_open(ib, symbol):
    """Check if the market is open for specific symbol."""
    contract = Stock(symbol=symbol, exchange='SMART', currency='USD')
    details = ib.reqContractDetails(contract)
    return details[0].tradingHours

def fetch_positions(ib):
    """Fetch all current positions in the portfolio."""
    return ib.positions()

def get_real_time_price(ib, symbol):
    """Fetch latest price for a stock."""
    contract = Stock(symbol=symbol, exchange='SMART', currency='USD')
    ticker = ib.reqMktData(contract)
    ib.sleep(2)  # Data needs to populate
    return ticker.last

def fetch_historical_data(ib, symbol, duration='1 D', bar_size='1 min'):
    """Fetch historical data for the given symbol."""
    contract = Stock(symbol=symbol, exchange='SMART', currency='USD')
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr=duration,
        barSizeSetting=bar_size,
        whatToShow='MIDPOINT',
        useRTH=True
    )
    return bars

def bid_ask_spread(ib, symbol):
    """
    Calculate difference between bid price (highest price a buyer is willing to pay) and ask price 
    (lowest price a seller is willing to accept)
    """
    # Create stock contract
    contract = Stock(symbol=symbol, exchange='SMART', currency='USD')
    
    # Request market data for the contract
    ticker = ib.reqMktData(contract)
    ib.sleep(2)  # market data needs to populate

    # Check if bid and ask prices are available
    if ticker.bid and ticker.ask:
        spread = ticker.ask - ticker.bid
        return {
            "symbol": symbol,
            "bid": ticker.bid,
            "ask": ticker.ask,
            "spread": spread
        }
    else:
        print(f"Bid or ask price not available for {symbol}.")
        return None

def place_limit_order(ib, symbol, quantity, price, action='BUY'):
    """Place a limit order for the given symbol."""
    contract = Stock(symbol=symbol, exchange='SMART', currency='USD')
    order = Order(action=action, totalQuantity=quantity, orderType='LMT', lmtPrice=price)
    trade = ib.placeOrder(contract, order)
    return trade

def place_market_order(ib, symbol, quantity=1, action='BUY'):
    """Place a market order for a stock."""
    contract = Stock(symbol=symbol, exchange='SMART', currency='USD')
    order = Order(action=action, totalQuantity=quantity, orderType='MKT')
    trade = ib.placeOrder(contract, order)
    return trade

def place_batch_orders(ib, orders):
    """Place multiple orders."""
    trades = []
    for order_details in orders:
        symbol, quantity, price, action = order_details
        trade = place_limit_order(ib, symbol, quantity, price, action)
        trades.append(trade)
    return trades

def change_limit_price(ib, trade, new_price):
    # Check if the existing trade has an order
    if not trade or not trade.order:
        print("No order found to modify.")
        return None

    # Cancel existing order
    print(f"Cancelling order ID {trade.order.orderId} with limit price {trade.order.lmtPrice}...")
    ib.cancelOrder(trade.order)
    ib.sleep(2)  # Wait for cancellation to process

    # Create new order with updated limit price
    contract = trade.contract
    new_order = Order(
        action=trade.order.action,
        totalQuantity=trade.order.totalQuantity,
        orderType='LMT',
        lmtPrice=new_price
    )
    new_trade = ib.placeOrder(contract, new_order)

    print(f"New order placed with limit price {new_price}")
    return new_trade

def get_order_status(ib, trade):
    """Check the status of an order."""
    return trade.orderStatus.status

def cancel_order(ib, trade):
    """Cancel a pending order."""
    ib.cancelOrder(trade.order)
    print(f"Order {trade.order.orderId} canceled.")

def set_stop_loss(ib, symbol, quantity, stop_price):
    """Place a stop-loss order."""
    contract = Stock(symbol=symbol, exchange='SMART', currency='USD')
    order = Order(action='SELL', totalQuantity=quantity, orderType='STP', auxPrice=stop_price)
    trade = ib.placeOrder(contract, order)
    return trade

def calculate_pos_size(account_bal, risk_perc, entry_price, stop_loss_price):
    """Calculate position size to buy based on account balance, risk tolerance, and stop-loss distance."""
    # risk amount
    risk_amt = account_bal * (risk_perc / 100)
    # stop-loss distance
    stop_loss_dist = abs(entry_price - stop_loss_price)
    #  position size
    if stop_loss_dist == 0:
        raise ValueError("Stop-loss distance cannot be zero.")
    pos_size = risk_amt / stop_loss_dist

    return pos_size

def test_order(ib, symbol, quantity=1, action='BUY'):
    """Simulating orders to check for errors or margin impact"""
    contract = Stock(symbol=symbol, exchange='SMART', currency='USD')
    order = Order(action=action, totalQuantity=quantity, orderType='MKT')
    validation = ib.whatIfOrder(contract, order)
    print(f"Order validation: {validation}")

def get_trade_by_id(ib, order_id):
    """Retrieve a Trade object by its order ID."""
    for trade in ib.trades():
        if trade.order.orderId == order_id:
            return trade
    print(f"Trade with ID {order_id} not found.")
    return None
