# Get market data based on min max dates from okx strategy files

from vectorbtpro import *
import pandas as pd
import os

# Load strategy files
FOLDER = "/Users/ericervin/Library/CloudStorage/GoogleDrive-eervin@blockforcecapital.com/Shared drives/AI/data/Copy Trading/Data"
files = os.listdir(FOLDER)
files = [f for f in files if f.endswith(".csv")]
TIMEFRAME = '1T'
# Create a list of all the files in the data folder
# Initialize min and max dates
absolute_min_date = pd.Timestamp.max.tz_localize("UTC")
absolute_max_date = pd.Timestamp.min.tz_localize("UTC")
for file in files:
    filename = f"{FOLDER}/{file}"
    trades = pd.read_csv(filename)
    # print(f'Processing {filename}')
    if trades.empty:
        continue
    # Convert to datetime and coerce errors to NaT
    trades["open_date"] = pd.to_datetime(trades["open_date"], errors="coerce")
    trades["close_date"] = pd.to_datetime(trades["closed_date"], errors="coerce")

    # Apply timezone only to non-NaT values
    trades.loc[trades["open_date"].notna(), "open_date"] = (
        trades.loc[trades["open_date"].notna(), "open_date"]
        .dt.tz_localize("America/Chicago")
        .dt.tz_convert("UTC")
    )
    trades.loc[trades["close_date"].notna(), "close_date"] = (
        trades.loc[trades["close_date"].notna(), "close_date"]
        .dt.tz_localize("America/Chicago")
        .dt.tz_convert("UTC")
    )

    # Drop rows where either open_date or close_date is NaT
    trades.dropna(subset=["open_date", "close_date"], inplace=True)

    # Find min and max dates
    min_date = trades["open_date"].min().floor("D")
    max_date = trades["close_date"].max().ceil("D")

    # Update absolute min and max dates
    absolute_min_date = min(min_date, absolute_min_date)
    absolute_max_date = max(max_date, absolute_max_date)

print(f"Pulling data for dates {absolute_min_date} to {absolute_max_date}")
main_symbols = ['BTCUSDT', 'ETHUSDT']
data = vbt.BinanceData.pull(main_symbols, start=min_date, end=max_date, timeframe=TIMEFRAME)
data.save('OKX-Strategy-Analysis/price_data.pkl')
print(f"Data saved for dates to OKX-Strategy-Analysis/price_data.pkl {absolute_min_date} to {absolute_max_date} with timeframe {TIMEFRAME}")
