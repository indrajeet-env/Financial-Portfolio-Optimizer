from data import fetch_stock_data, calculate_daily_returns
from optimizer import calculate_statistics, generate_random_portfolios, find_max_sharpe_portfolio, find_min_variance_portfolio
from plots import plot_efficient_frontier

symbols = ["AAPL", "GOOGL", "MSFT", "NVDA"]

prices = fetch_stock_data(symbols)
returns = calculate_daily_returns(prices)

annual_mean_returns, covariance_matrix = calculate_statistics(returns)

portfolios = generate_random_portfolios(
    num_portfolios=10000,
    annual_mean_returns=annual_mean_returns,
    covariance_matrix=covariance_matrix,
)

max_sharpe = find_max_sharpe_portfolio(portfolios)
min_variance = find_min_variance_portfolio(portfolios)

print(annual_mean_returns)
print("-"*50)
print(covariance_matrix)
print("-" * 50)
print("Random Portfolios")
print(portfolios)


print("-" * 50)
print("Maximum Sharpe Portfolio")
print(max_sharpe)

print("-" * 50)
print("Minimum Variance Portfolio")
print(min_variance)


plot_efficient_frontier(
    portfolios,
    max_sharpe,
    min_variance,
)