from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from data import fetch_stock_data, calculate_daily_returns
from optimizer import (
    calculate_statistics,
    generate_random_portfolios,
    find_max_sharpe_portfolio,
    find_min_variance_portfolio,
)


app = FastAPI(title="Financial Portfolio Optimizer API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PortfolioRequest(BaseModel):
    symbols: list[str]
    period: str = "2y"
    num_portfolios: int = 10000


@app.get("/")
def root():
    return {
        "message": "Financial Portfolio Optimizer API is running"
    }


@app.post("/optimize")
def optimize(request: PortfolioRequest):
    prices = fetch_stock_data(
        request.symbols,
        request.period,
    )

    returns = calculate_daily_returns(prices)

    annual_mean_returns, covariance_matrix = calculate_statistics(
        returns
    )

    portfolios = generate_random_portfolios(
        request.num_portfolios,
        annual_mean_returns,
        covariance_matrix,
    )

    max_sharpe = find_max_sharpe_portfolio(portfolios)
    min_variance = find_min_variance_portfolio(portfolios)
    chart_data = portfolios[
      ["Risk", "Return", "Sharpe"]
    ].to_dict(orient="records")

    return {
        "max_sharpe": max_sharpe.to_dict(),
        "min_variance": min_variance.to_dict(),
        "chart_data": chart_data,
    }