import pandas as pd 
import datetime
import vectorbtpro as vbt

min_date = datetime.datetime(year=2023, month=11, day=1)
max_date = datetime.datetime.now()

# print(f"Pulling data for dates {min_date} to {max_date}")
# main_symbols = ['BTCUSDT', 'ETHUSDT']
# data = vbt.BinanceData.pull(main_symbols, start=min_date, end=max_date, timeframe='1m')
# data.save('price_data_1m.pkl')
# print(f"Data saved for dates to OKX-Strategy-Analysis/price_data.pkl")

data = vbt.BinanceData.load('price_data_1m.pkl')
symbol = "BTCUSDT"
symbol_data = data.get(symbol=symbol)
print(symbol_data.Close)
# symbol_orders = orders[orders["symbol"] == symbol]