""" 
    The file is responsible for:
    - Downloading the daily returns of the stocks 
    - Calculating the expected annual returns(μ)
    - Calculating the covariance matrix (Σ)
    - Generating 10,000 random portfolios
    - Calculating the portfolio return (R)
    - Calculating the portfolio risk (σ)
    - Calculating the sharpe ratio (Sharpe)
    - Finding the maximum sharpe portfolio (Max Sharpe)
    - Finding the minimum variance portfolio (Min Variance)  
"""

import numpy as np
import pandas as pd

def calculate_statistics(daily_returns: pd.DataFrame):
    """
    Calculate the annualized expected returns (μ) and covariance matrix (Σ).

    Parameters:
        daily_returns (pd.DataFrame): Daily percentage returns for each stock.

    Returns:
        tuple:
            mean_returns (pd.Series): Annualized expected returns.
            covariance_matrix (pd.DataFrame): Annualized covariance matrix.
    """

    # we multiply by 252 because there are approximately 252 trading days in a year
    annual_mean_returns = daily_returns.mean() * 252 # convering daily expected return into annual expected return, which is the convention used in Modern Portfolio Theory.
    covariance_matrix = daily_returns.cov() * 252 

    return annual_mean_returns, covariance_matrix
  


def portfolio_performance(weights: np.ndarray,
                          annual_mean_returns: pd.Series,
                          covariance_matrix: pd.DataFrame):
    """
    Calculate the expected annual return and annual risk of a portfolio.

    Parameters:
        weights (np.ndarray): Portfolio weights.
        annual_mean_returns (pd.Series): Expected annual returns for each stock.
        covariance_matrix (pd.DataFrame): Annual covariance matrix.

    Returns:
        tuple:
            (portfolio_return, portfolio_risk)
    """

    portfolio_return = np.dot(weights, annual_mean_returns) # portfolio return is the sum of the expected returns of the stocks in the portfolio multiplied by the weights of the stocks

    portfolio_variance = np.dot(weights.T, np.dot(covariance_matrix, weights)) # weights.T is the transpose of the weights array, covariance_matrix is the covariance matrix of the stocks, weights is the weights of the stocks in the portfolio.

    portfolio_risk = np.sqrt(portfolio_variance) #portfolio risk is almost always referring to portfolio volatility, which is the standard deviation of the portfolio’s returns.

    return portfolio_return, portfolio_risk
  


def generate_random_portfolios(num_portfolios: int,
                               annual_mean_returns: pd.Series,
                               covariance_matrix: pd.DataFrame):
    """
    Generate random portfolios and calculate their
    return and risk.

    Parameters:
        num_portfolios (int): Number of portfolios to generate.
        annual_mean_returns (pd.Series): Expected annual returns.
        covariance_matrix (pd.DataFrame): Annual covariance matrix.

    Returns:
        pd.DataFrame
    """

    results = []

    for _ in range(num_portfolios):
        # Generate random weights for all stocks
        weights = np.random.random(len(annual_mean_returns))

        # Normalize weights so they sum to 1 (100% of the capital invested)
        weights /= np.sum(weights)

        # Calculate that particular portfolio's expected return and risk
        portfolio_return, portfolio_risk = portfolio_performance(
            weights,
            annual_mean_returns,
            covariance_matrix,
        )
        
        sharpe_ratio = calculate_sharpe_ratio(
            portfolio_return,
            portfolio_risk,
        )
        # Store the portfolio's performance and allocation
        results.append({
            "Return": portfolio_return,
            "Risk": portfolio_risk,
            "Sharpe": sharpe_ratio,
            **dict(zip(annual_mean_returns.index, weights)), # zip is a built-in function that combines the two lists into a dictionary, annual_mean_returns.index is the list of stock names, weights is the list of weights for each stock
        })
        # we get something like this:
        """      
          {
            "Return": 0.218,
            "Risk": 0.243,
            "Sharpe": 0.897,
            "AAPL": 0.37,
            "GOOGL": 0.11,
            "MSFT": 0.44,
            "NVDA": 0.08,
          }
        """
    return pd.DataFrame(results)
  
  
# Calculating the Sharpe Ratio
def calculate_sharpe_ratio(portfolio_return: float,
                           portfolio_risk: float,
                           risk_free_rate: float = 0.06):
    """
    Calculate the Sharpe Ratio of a portfolio.

    Parameters:
        portfolio_return (float): Expected annual portfolio return.
        portfolio_risk (float): Annual portfolio volatility.
        risk_free_rate (float): Annual risk-free rate (default 6%).

    Returns:
        float: Sharpe Ratio.
    """

    return (portfolio_return - risk_free_rate) / portfolio_risk  # Sharpe Ratio is the portfolio return minus the risk-free rate divided by the portfolio risk, risk-free rate is usually the rate of return on a risk-free asset like a government bond, and here it is set to 6% as a default value.

def find_max_sharpe_portfolio(portfolios: pd.DataFrame):
    """
    Return the portfolio with the highest Sharpe Ratio.
    """
    return portfolios.loc[portfolios["Sharpe"].idxmax()] # portfolios["Sharpe"].idxmax() returns the index of the maximum value in the "Sharpe" column, and portfolios.loc[...] returns the row corresponding to that index.



def find_min_variance_portfolio(portfolios: pd.DataFrame):
    """
    Return the portfolio with the lowest risk (minimum variance portfolio).
    """
    return portfolios.loc[portfolios["Risk"].idxmin()]