import streamlit as st
from app.config import BotConfig

config = BotConfig()
with open('style.css') as f:  
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    config.parameter_block(st.sidebar)
    if st.sidebar.button("Update Settings"):
        config.update()

with st.container():  
    st.markdown(f'# My <span style="color:orange">{config.MODE}</span> Portfolio', unsafe_allow_html=True)