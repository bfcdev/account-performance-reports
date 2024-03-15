# Get market data based on min max dates from okx strategy files

from vectorbtpro import *
import pandas as pd
import os

# Load strategy files
folder = "/Users/ericervin/Library/CloudStorage/GoogleDrive-eervin@blockforcecapital.com/Shared drives/AI/data/Copy Trading/Data"
files = os.listdir(folder)
files = [f for f in files if f.endswith(".csv")]

# Create a list of all the files in the data folder
import os

files = os.listdir("data")
files = [f for f in files if f.endswith(".csv")]
# Initialize min and max dates
absolute_min_date = pd.Timestamp.max.tz_localize("UTC")
absolute_max_date = pd.Timestamp.min.tz_localize("UTC")
for file in files:
    filename = f"data/{file}"
    trades = pd.read_csv(filename)
    # print(f'Processing {filename}')

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

print(f"Absolute Minimum date: {absolute_min_date}")
print(f"Absolute Maximum date: {absolute_max_date}")


main_symbols = ['BTCUSDT', 'ETHUSDT']
data = vbt.BinanceData.pull(main_symbols, start=min_date, end=max_date, timeframe='15T')
data.save('price_data.pkl')
# data = vbt.Data.load('price_data.pkl')
# data['Close'].get().tail()
