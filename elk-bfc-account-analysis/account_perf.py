
import plotly.express as px
import pandas as pd
import vectorbtpro as vbt
import numpy as np

vbt.settings.set_theme("dark")
vbt.settings.plotting["layout"]["width"] = 800
vbt.settings.plotting['layout']['height'] = 200
vbt.settings.plotting.use_resampler = True # Need to pip install https://github.com/predict-idlab/plotly-resampler


#data 
data = vbt.BinanceData.load('price_data_1m.pkl')
btc_data = data.get(symbol="BTCUSDT")
eth_data = data.get(symbol="ETHUSDT")

filename = 'astra.xlsx'

trades = pd.read_excel(filename, sheet_name='Sheet1', index_col='datetime', parse_dates=True)
# If open-short and close-long then quantity should be negative else positive
trades['trade_direction'] = trades.apply(lambda x: -1 if (x['direction'] == 'open-short' or x['direction'] == 'close-long') else 1, axis=1)
trades['trade_quantity'] = trades['trade_direction'] * trades['quantity']
# Load data from pickle file
# eth_data = vbt.BinanceData.load('DEC2023_eth_minutely_data.pkl')
# btc_daily_data = vbt.BinanceData.load('DEC2023_btc_daily_data.pkl')
yos_eth_fast_trades = trades[trades['strategy']=='Yosemite ETH Fast']
seq_eth_fast_trades = trades[trades['strategy']=='Yosemite ETH Fast V3']
yos_eth_slow_trades = trades[trades['strategy']=='Yosemite ETH Slow']
seq_eth_slow_trades = trades[trades['strategy']=='Yosemite ETH Slow V3']

trades.index = pd.to_datetime(trades.index, format='ISO8601')
eth_data.index = pd.to_datetime(eth_data.index)
print(eth_data)
print(trades)
duplicate_indices = trades.index[trades.index.duplicated()]
start = '2024-03-01'
end = '2024-04-01'

eth_data = eth_data.loc[start:end]
trades = trades.loc[start:end]

# Print duplicate index values
print("Duplicate index values:", duplicate_indices.unique())


elk_pf = vbt.Portfolio.from_orders(
    close = eth_data.Close, # Note, here we are using the minutely data for ETH
    size = trades['trade_quantity'],  # Here we are only looking at the trades dataframe
    price = trades['price'],
    size_type = 'amount',
    fixed_fees = trades['fees'],
    init_cash = 400000,
    leverage=4,
    leverage_mode=vbt.pf_enums.LeverageMode.Eager,    
    freq = '1T',
)

# yos_eth_fast_pf = vbt.Portfolio.from_orders(
#     close = eth_data.Close,
#     size = yos_eth_fast_trades['trade_quantity'],
#     price = yos_eth_fast_trades['price'],
#     size_type = 'amount',
#     fixed_fees = yos_eth_fast_trades['fees'],
#     init_cash = 500,
#     leverage = 4, 
#     leverage_mode=vbt.pf_enums.LeverageMode.Eager,
#     freq = '1T',
#     direction = 'Both',
# )


# seq_eth_fast_pf = vbt.Portfolio.from_orders(
#     close = eth_data.Close,
#     size = seq_eth_fast_trades['trade_quantity'],
#     price = seq_eth_fast_trades['price'],
#     size_type = 'amount',
#     fixed_fees = seq_eth_fast_trades['fees'],
#     init_cash = 1000,
#     freq = '1T',
#     direction = 'Both',
#     leverage = 4,
#     leverage_mode=vbt.pf_enums.LeverageMode.Eager,
# )

# yos_eth_slow_pf = vbt.Portfolio.from_orders(
#     close = eth_data.Close,
#     size = yos_eth_slow_trades['trade_quantity'],
#     price = yos_eth_slow_trades['price'],
#     size_type = 'amount',
#     fixed_fees = yos_eth_slow_trades['fees'],
#     init_cash = 500,
#     freq = '1T',
#     direction = 'Both',
#     leverage = 4,
#     leverage_mode=vbt.pf_enums.LeverageMode.Eager,
# )

# seq_eth_slow_pf = vbt.Portfolio.from_orders(
#     close = eth_data.Close,
#     size = seq_eth_slow_trades['trade_quantity'],
#     price = seq_eth_slow_trades['price'],
#     size_type = 'amount',
#     fixed_fees = seq_eth_slow_trades['fees'],
#     init_cash = 500,
#     freq = '1T',
#     direction = 'Both',
#     leverage = 4,
#     leverage_mode=vbt.pf_enums.LeverageMode.Eager,
# )


def calc_capital_weighted_time_in_market(portfolio):
    '''Calculates the capital weighted time in market as a percentage of the total time multiplied by the average capital invested'''
    portfolio_trades = portfolio.trades.records_readable
    trade_duration = portfolio_trades['Exit Index'] - portfolio_trades['Entry Index']
    capital_invested = portfolio_trades.Size * portfolio_trades['Avg Entry Price']
    weighted_time = (trade_duration * capital_invested).sum()
    total_time = portfolio.wrapper.index[-1]-portfolio.wrapper.index[0]
    capital_weighted_time_pct = (weighted_time.total_seconds() / (total_time.total_seconds() * portfolio.value.mean())) * 100
    return capital_weighted_time_pct

# print(f'Capital Weighted Time Invested [%]: {calc_capital_weighted_time_in_market(elk_pf):.2f}%')

# Example of how to create a custom metric
# https://vectorbt.dev/api/portfolio/base/#custom-metrics
max_winning_streak = (
    'max_winning_streak',
    dict(
        title='Max Winning Streak',
        calc_func='trades.winning_streak.max'
    )
)

max_losing_streak = (
    'max_losing_streak',
    dict(
        title='Max Losing Streak',
        calc_func='trades.losing_streak.max'
    )
)

capital_weighted_time_exposure = (
    'capital_weighted_time_exposure',
    dict(
        title='Capital Weighted Time Exposure [%]',
        calc_func=lambda self, group_by:
        calc_capital_weighted_time_in_market(self)
    )
)

# Add the custom metric to the portfolio stats as the last item
# elk_pf.metrics['max_winning_streak'] = max_winning_streak[1]
# elk_pf.metrics['max_losing_streak'] = max_losing_streak[1]
# elk_pf.metrics['capital_weighted_time_exposure'] = capital_weighted_time_exposure[1]

my_metrics = list(elk_pf.metrics.items())
vbt.settings.portfolio['stats']['metrics'] = my_metrics

# Create a dict of the different portfolios with the key being the name of the portfolio
portfolios = {
    'ELK': elk_pf,
    # 'Yosemite ETH Fast': yos_eth_fast_pf,
    # 'Yosemite ETH Slow': yos_eth_slow_pf,
    # 'Seq ETH Fast': seq_eth_fast_pf,
    # 'Seq ETH Slow': seq_eth_slow_pf
}
# output the stats and plots for each portfolio strategy
for portfolio in portfolios: 
    print(portfolio)
    print(portfolios[portfolio].stats())
    portfolios[portfolio].plot(title=f"{portfolio}").show()

