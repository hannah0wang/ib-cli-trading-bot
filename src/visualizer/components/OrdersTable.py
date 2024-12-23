import streamlit as st
import pandas as pd

class OrdersTable:    
    @staticmethod  
    def show_table(st, df):  
        orders_df = df.style. \  
            format(precision=2, thousands='.', decimal=',')  
        st.dataframe(orders_df, column_config={  
            'symbol': 'Symbol',  
            'action': 'Action',  
            'qty': 'Quantity',  
            'type': 'Order type',  
            'stop_price': 'Stop price',  
            'avg_cost': None,  
            'dist_avg_cost': 'Dist. entry %',  
            'dist_market_price': 'Dist. curr. price %'  
        }, hide_index=True)