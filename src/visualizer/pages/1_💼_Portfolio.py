import streamlit as st
from visualizer.helpers.ib_helpers import setup_ib_connection
from visualizer.components.PositionsTable import PositionsTable
from visualizer.components.PositionsChart import PositionsChart

# Setup IB connection
ib = setup_ib_connection()

# Fetch and display portfolio
with st.container():
    col1, col2 = st.columns([5, 3])
    portfolio_df = ib_helpers.portfolio_items(ib)
    PositionsTable.show_table(col1, portfolio_df)
    PositionsChart.show_chart(col2, portfolio_df)


# Render portfolio visualization
with st.container():  
    col1, col2 = st.columns([5, 3])  

    portfolio_df = portfolio_items(ib)  
    PositionsTable.show_table(col1, portfolio_df)
    PositionsChart.show_chart(col2, portfolio_df)