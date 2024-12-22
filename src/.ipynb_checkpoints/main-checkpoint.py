from ib_insync import *
import nest_asyncio

from utils import *

nest_asyncio.apply()

def show_help():
    """Display available commands."""
    print("""
Available Commands:
  fetch_balance                                            - Fetch account balance
  is_market_open <symbol>                                  - Check if the market is open for a specific symbol
  fetch_positions                                          - Fetch all current positions
  get_price <symbol>                                       - Get real-time stock price (e.g., get_price AAPL)
  fetch_historical <symbol>                                - Fetch historical data for a symbol
  bid_ask_spread <symbol>                                  - Get bid-ask spread (e.g., bid_ask_spread AAPL)
  place_limit_order <symbol> <quantity> <price> <action>   - Place a limit order (e.g., place_limit_order AAPL 10 150.0 BUY)
  place_market_order <symbol> <quantity> <action>          - Place a market order (e.g., place_market_order AAPL 10 BUY)
  place_batch_orders [<symbol>, <quantity>, <price>, ...]  - Place multiple orders as a batch
  change_limit_price <trade> <new_price>                   - Modify an existing limit order's price
  get_order_status <tradeId>                               - Get the order status of a trade
  cancel_order <tradeId>                                    - Cancel a pending order
  set_stop_loss <symbol> <quantity> <stop_price>           - Place a stop-loss order for a symbol
  calculate_pos_size <acc_balance> <risk%> <entry> <stop_loss>
                                                          - Calculate position size based on account balance and risk
  test_order <symbol> <quantity> <action>                  - Simulate an order to check for errors or margin impact
  help                                                     - Show available commands
  exit                                                     - Exit the CLI
""")

def main():
    # Connect to IB Gateway
    ib = IB()
    ib.connect('127.0.0.1', 4002, clientId=1)
    print("Connected to IB Gateway")
    show_help()

    while True:
        try:
            # Read user input
            command = input(">>> ").strip()

            # Exit condition
            if command == "exit":
                print("Exiting the CLI... Unlike your trades, this exit is guaranteed!")
                break

            # Process commands
            if command == "fetch_balance":
                balance = fetch_account_balance(ib)
                print(f"Account balance: {balance}")

            elif command.startswith("is_market_open"):
                _, symbol = command.split()
                is_open = is_market_open(ib, symbol)
                print(f"Market is {is_open}")

            elif command == "fetch_positions":
                positions = fetch_positions(ib)
                for pos in positions:
                    print(pos)

            elif command.startswith("get_price"):
                _, symbol = command.split()
                price = get_real_time_price(ib, symbol)
                print(f"Real-time price for {symbol}: {price}")

            elif command.startswith("fetch_historical"):
                _, symbol = command.split()
                bars = fetch_historical_data(ib, symbol)
                for bar in bars:
                    print(bar)

            elif command.startswith("bid_ask_spread"):
                _, symbol = command.split()
                spread = bid_ask_spread(ib, symbol)
                print(f"Bid-Ask Spread for {symbol}: {spread}")

            elif command.startswith("place_market_order"):
                _, symbol, quantity, action = command.split()
                trade = place_market_order(ib, symbol, int(quantity), action)
                print(f"Market order placed. Status: {trade.orderStatus.status} OrderId: {trade.order.orderId}")

            elif command.startswith("place_limit_order"):
                _, symbol, quantity, price, action = command.split()
                trade = place_limit_order(ib, symbol, int(quantity), float(price), action)
                print(f"Limit order placed. Status: {trade.orderStatus.status} OrderId: {trade.order.orderId}")

            elif command.startswith("place_batch_orders"):
                try:
                    # Extract batch orders from the input after the command
                    batch_input = command[len("place_batch_orders"):].strip()
                    
                    # Ensure input is not empty
                    if not batch_input:
                        print("No orders provided. Format: <symbol,quantity,price,action> (e.g., AAPL,10,150.0,BUY TSLA,5,700.0,SELL)")
                        return
                    
                    # Parse orders from the batch input
                    # Format: AAPL,10,150.0,BUY TSLA,5,700.0,SELL
                    orders = []
                    for order in batch_input.split():
                        try:
                            symbol, quantity, price, action = order.split(',')
                            quantity = int(quantity)
                            price = float(price)
                            action = action.upper()
            
                            # Validate the action
                            if action not in {"BUY", "SELL"}:
                                print(f"Invalid action for {symbol}. Use 'BUY' or 'SELL'. Skipping this order...")
                                continue
            
                            # Add the parsed order to the list
                            orders.append((symbol, quantity, price, action))
                        except ValueError:
                            print(f"Invalid format for order: {order}. Use <symbol,quantity,price,action>. Skipping this order...")
            
                    # Check if any valid orders exist
                    if not orders:
                        print("No valid orders to place.")
                        return
            
                    # Place batch orders
                    print(f"Placing the following batch orders: {orders}")
                    trades = place_batch_orders(ib, orders)
            
                    # Print results of the trades
                    for trade in trades:
                        print(f"Order for {trade.contract.symbol}: Status = {trade.orderStatus.status} OrderId = {trade.order.orderId}")
            
                except Exception as e:
                    print(f"An error occurred while processing batch orders: {e}")

            # elif command.startswith("get_order_status"):
                
            # elif command.startswith("cancel_order"):
                
            
            elif command == "help":
                show_help()

            else:
                print("Invalid command. Type 'help' to see available commands.")

        except Exception as e:
            print(f"An error occurred: {e}")

    # Disconnect from IB Gateway
    ib.disconnect()
    print("Disconnected from IB Gateway.")

if __name__ == "__main__":
    main()
