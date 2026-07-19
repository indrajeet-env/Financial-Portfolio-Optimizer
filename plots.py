import matplotlib.pyplot as plt
import pandas as pd

def plot_efficient_frontier(
    portfolios: pd.DataFrame, # DataFrame containing all the generated portfolios.
    max_sharpe: pd.Series, # just one row
    min_variance: pd.Series,
):
  
  plt.figure(figsize=(10, 6)) # width, height
  scatter = plt.scatter(
    portfolios["Risk"], # x-axis
    portfolios["Return"], # y-axis
    c=portfolios["Sharpe"], # color of the points based on Sharpe ratio, higher Sharpe ratio will be Yellow, medium will be green, and lower will be purple
    cmap="viridis", # color palette
    alpha=0.5, # alpha controls transparency
    s=5, # s is the size of the points
  )
  plt.colorbar(scatter, label="Sharpe Ratio")
  plt.grid(True, linestyle="--", alpha=0.4)

  # Sort portfolios by increasing risk
  frontier = portfolios.sort_values("Risk")

  # Keep only portfolios that offer the highest return seen so far
  # This approximates the Efficient Frontier from the simulated portfolios.
  efficient_frontier = []
  max_return = -float("inf")

  for _, portfolio in frontier.iterrows():
      if portfolio["Return"] > max_return:
          efficient_frontier.append(portfolio)
          max_return = portfolio["Return"]

  efficient_frontier = pd.DataFrame(efficient_frontier)
  plt.scatter( # plot the maximum Sharpe ratio portfolio
    max_sharpe["Risk"],
    max_sharpe["Return"],
    color="red",
    marker="*",
    s=250,
    label="Maximum Sharpe Portfolio",
  )
  plt.scatter( # plot the minimum variance portfolio
      min_variance["Risk"],
      min_variance["Return"],
      color="green",
      marker="o",
      s=150,
      label="Minimum Variance Portfolio",
  )
  plt.plot(
      efficient_frontier["Risk"],
      efficient_frontier["Return"],
      color="darkorange",
      linewidth=2.5,
      label="Efficient Frontier",
      zorder=2,
  )
  
  plt.title("Modern Portfolio Theory - Efficient Frontier")
  plt.xlabel("Risk (Volatility)")
  plt.ylabel("Expected Annual Return")
  plt.legend()
  
  plt.tight_layout()
  
  plt.show()