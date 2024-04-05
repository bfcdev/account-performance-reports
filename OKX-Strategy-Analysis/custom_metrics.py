from vectorbtpro import *

######################## Custom Metrics ########################
## Usage
# Example of how to create a custom metric
# https://vectorbt.dev/api/portfolio/base/#custom-metrics

# 1. Define a function that calculates the custom metric
# 2. Create a tuple with the metric name and a dictionary containing the title and the calculation function
# 3. Add the tuple to the custom_metrics_dict
# 4. Add the metric name to the desired_order list to reorder the metrics
# 5. Run the code

# Now call the stats method with the ordered metrics
# pf.stats(metrics=ordered_metrics)


def calc_capital_weighted_time_in_market(portfolio):
    portfolio_trades = portfolio.trades.records_readable
    # Calculate trade duration and convert to seconds
    trade_duration_seconds = (
        portfolio_trades["Exit Index"] - portfolio_trades["Entry Index"]
    ).dt.total_seconds()
    capital_invested = portfolio_trades.Size * portfolio_trades["Avg Entry Price"]
    weighted_time = (trade_duration_seconds * capital_invested).sum()
    # Calculate total time in seconds
    total_time_seconds = (
        portfolio.wrapper.index[-1] - portfolio.wrapper.index[0]
    ).total_seconds()
    capital_weighted_time_pct = (
        weighted_time / (total_time_seconds * portfolio.value.mean())
    ) * 100
    return capital_weighted_time_pct


# Define your custom metrics
max_winning_streak = (
    "max_winning_streak",
    dict(title="Max Winning Streak", calc_func="trades.winning_streak.max"),
)

max_losing_streak = (
    "max_losing_streak",
    dict(title="Max Losing Streak", calc_func="trades.losing_streak.max"),
)

capital_weighted_time_exposure = (
    "capital_weighted_time_exposure",
    dict(
        title="Capital Weighted Time Exposure [%]",
        calc_func=lambda self, group_by: calc_capital_weighted_time_in_market(self),
    ),
)

custom_metrics_dict = {
    "max_winning_streak": max_winning_streak,
    "max_losing_streak": max_losing_streak,
    "capital_weighted_time_exposure": capital_weighted_time_exposure,
}

# Retrieve the default metrics and convert them to a dictionary
default_metrics_dict = dict(vbt.Portfolio.metrics)


# Reorder metrics according to desired_order
desired_order = [
    "start",
    "end",
    "period",
    "start_value",
    "min_value",
    "max_value",
    "end_value",
    "cash_deposits",
    "cash_earnings",
    "total_return",
    "bm_return",
    "total_time_exposure",
    "capital_weighted_time_exposure",
    "max_gross_exposure",
    "max_dd",
    "max_dd_duration",
    "total_orders",
    "total_fees_paid",
    "total_trades",
    "win_rate",
    "max_winning_streak",
    "max_losing_streak",
    "best_trade",
    "worst_trade",
    "avg_winning_trade",
    "avg_losing_trade",
    "avg_winning_trade_duration",
    "avg_losing_trade_duration",
    "profit_factor",
    "expectancy",
    "sharpe_ratio",
    "calmar_ratio",
    "omega_ratio",
    "sortino_ratio",
]

# Reorder metrics according to desired_order
def get_ordered_metrics():
    ordered_metrics = []
    for metric_name in desired_order:
        if metric_name in custom_metrics_dict:
            # Add custom metric
            ordered_metrics.append(custom_metrics_dict[metric_name])
        elif metric_name in default_metrics_dict:
            # Add default metric
            ordered_metrics.append(metric_name)
        else:
            print(f"Warning: Metric '{metric_name}' not found.")
    return ordered_metrics


