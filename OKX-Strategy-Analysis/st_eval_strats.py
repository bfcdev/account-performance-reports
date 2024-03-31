import os
import streamlit as st
import pandas as pd
from vectorbtpro import *

st.set_page_config(layout="wide")

SAVE_FOLDER = "/Users/ericervin/Documents/Coding/account-performance-reports/OKX-Strategy-Analysis/results"
master_results_filename = SAVE_FOLDER + "/master_stats.csv"
files = os.listdir(SAVE_FOLDER)
files = [f for f in files if f.endswith(".pkl")]
files.sort()
master_results = pd.read_csv(master_results_filename)

st.dataframe(master_results)

selected_file = st.selectbox('Select a file', files)

pf = vbt.load(SAVE_FOLDER+"/"+selected_file)

# st.write(pf.stats())
# st.plotly_chart(pf.plot())

# Create two columns for stats and plot
col1, col2 = st.columns([1,2])

# Display the stats in the first column
with col1:
    st.dataframe(pf.stats(), height=900)

# Display the plot in the second column
with col2:
    st.plotly_chart(pf.plot(width=600, height=900))


# Trade Analysis
st.subheader("Trade Analysis")
st.plotly_chart(pf.plot_trade_signals())

# Create two columns for stats and plot
col3, col4 = st.columns([3,4])
width = 500
with col3:
    st.plotly_chart(pf.trades.plot_expanding_mae_returns(title='Worst Trades', width=width)) # This is the maximum adverse excursion (MAE)
    st.plotly_chart(pf.trades.plot_mae_returns(title='Worst Trades', width=width))
with col4:
    st.plotly_chart(pf.trades.plot_expanding_mfe_returns(title='Best Trades', width=width)) # This is the maximum favorable excursion (MFE)
    st.plotly_chart(pf.trades.plot_mfe_returns(title='Best Trades', width=width))
    
# Give the user the option to see all the trades
if st.checkbox('Show all trades'):
    st.dataframe(pf.trade_history)

if st.checkbox('Show detailed trade records'):
    st.dataframe(pf.trades.records_readable)
    
if st.checkbox('Show all orders'):
    st.dataframe(pf.orders.records_readable)