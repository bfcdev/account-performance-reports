import os
from vectorbtpro import *
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

folder = "results"
master_results_filename = folder + "/master_stats.csv"
files = os.listdir(folder)
files = [f for f in files if f.endswith(".pkl")]
# Sort files alphabetically
files.sort()
master_results = pd.read_csv(master_results_filename)

# Display the data in the Streamlit app
st.dataframe(master_results)
# Create a selectbox for the user to select a file
selected_file = st.selectbox('Select a file', files)

# Load the selected file
pf = vbt.load(folder+"/"+selected_file)
st.plotly_chart(pf.plot())

