# Trade and Account Strategy Performance Analysis Repository

This repository contains a Jupyter Notebook that analyzes trading data using vectorbtpro library. It also includes the necessary data files for the analysis.

## Folders

- `OKX Strategy Analysis`
  - files related to analyzing historical performance by relevant assets of the OKX copy traders.
  - `get_data.py`: looks at the min max dates for each of the OKX strategies and then gets BTCUSDT and ETHUSDT for the relevant time period storing it in a pickle file for use in the analysis.
  - `okx_strat_loop.py`: loops over each of the strategies in the google drive (change this link on your machine) to calculate and store the historical stats and results in a vbt format.
  - `results`: folder for outptut from the `okx_strat_loop.py` file. This folder is the data folder for the streamlit analysis app.
  - `st_eval_strats.py`: Streamlit app for analysis of the OKX strategies based on their ETH and BTC trading history. 
- `elk-bfc-account-analysis`: Contains the files for analyzing our own data from our database we first built this analyzing the elk strategy.
  - `perf_analysis_v1.ipynb`: The main Jupyter Notebook file that contains the analysis code.
  - `trade history - 12.2023.xlsx`: The trading data file used in the analysis.

## Requirements

To run the notebook, you need the following dependencies:

- Python 3.10
- Jupyter Notebook
- vectorbtpro
- pandas
- numpy
