import streamlit as st
from shared.config import BotConfig

# Load configuration
config = BotConfig()

# Apply custom CSS
with open('static/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar settings
config.parameter_block(st.sidebar)
if st.sidebar.button("Update Settings"):
    config.update()

# Main content
st.markdown(f'# My <span style="color:orange">{config.MODE}</span> Portfolio', unsafe_allow_html=True)
