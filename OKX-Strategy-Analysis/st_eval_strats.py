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