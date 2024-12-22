class PositionsTable:  

    @staticmethod  
    def show_table(st, df):  
        def highlight_up(val):  
            color = 'green' if val > 0 else 'red'  
            return f'background-color: {color}'  
        portfolio_df = df.style. \  
            format(precision=2, thousands='.', decimal=','). \  
            map(highlight_up, subset=['perc_change'])  
        st.dataframe(portfolio_df, column_config={  
            'contract': None,  
            'symbol': 'Symbol',  
            'name': 'Name',  
            'avg_cost': 'Price',  
            'position': 'Size',  
            'market_price': 'Current Price',  
            'market_value': None,  
            'perc_change': 'Change%',  
            'unrealized_pnl': 'Unrealized PNL',  
            'realized_pnl': None  
        }, hide_index=True)