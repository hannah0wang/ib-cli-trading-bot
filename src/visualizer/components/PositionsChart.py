import plotly.graph_objects as go

class PositionsChart:  
    @staticmethod  
    def show_chart(st, df):  
        fig = go.Figure()  
        fig.add_trace(  
            go.Pie(  
                labels=list(df["symbol"]),  
                values=list(df["market_value"].abs()),  
                sort=False  
            )  
        )  
        fig.update_layout(  
            margin=dict(l=0, r=0, t=10, b=0)  
        )  
        st.plotly_chart(fig, use_container_width=True)  

    # Helper function to fetch historical bars
    def fetch_historical_data(ib, contract, duration='5 Y', bar_size='1 day'):
        """
        Fetch historical data for a given contract.

        :param ib: IB instance
        :param contract: IB contract object
        :param duration: Duration string (e.g., '5 Y' for 5 years)
        :param bar_size: Bar size (e.g., '1 day')
        :return: DataFrame with historical data
        """
        bars = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr=duration,
            barSizeSetting=bar_size,
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1
        )
        return pd.DataFrame(bars)

    # Fetch portfolio data
    portfolio_df = portfolio_items(ib)

    # Fetch and display historical data for each symbol
    st.markdown("## Historical Data")
    for index, row in portfolio_df.iterrows():
        symbol = row['symbol']
        contract = row['contract']

        # Create Stock contract
        stock = Stock(symbol=contract.symbol, exchange=contract.primaryExchange)

        # Fetch historical data
        bars_df = fetch_historical_data(ib, stock)

        # Display historical data
        if not bars_df.empty:
            st.markdown(f"### Historical Data for {symbol}")
            st.dataframe(bars_df)
        else:
            st.warning(f"No historical data available for {symbol}.")