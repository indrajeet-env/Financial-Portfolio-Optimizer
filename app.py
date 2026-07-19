import streamlit as st
import requests
import pandas as pd
import plotly.express as px

import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

st.set_page_config(
    page_title="Financial Portfolio Optimizer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Financial Portfolio Optimizer")

st.markdown(
    "Optimize your investment portfolio using Modern Portfolio Theory."
)

st.sidebar.header("Portfolio Settings")

symbols = st.sidebar.text_input(
    "Stock Symbols (comma-separated)",
    value="AAPL,MSFT,NVDA,GOOGL",
)

period = st.sidebar.selectbox(
    "Investment Period",
    ["1y", "2y", "5y", "10y"],
    index=1,
)

num_portfolios = st.sidebar.number_input(
    "Number of Portfolios",
    min_value=100,
    max_value=100000,
    value=10000,
    step=100,
)

optimize = st.sidebar.button(
    "🚀 Optimize Portfolio",
    use_container_width=True,
)

if optimize: # If button is clicked, run the optimization
    with st.spinner("Running Monte Carlo Simulation..."): # st.spinner shows a loading spinner while the optimization is running

        payload = {
            "symbols": [
                symbol.strip().upper()
                for symbol in symbols.split(",")
                if symbol.strip()
            ],
            "period": period,
            "num_portfolios": int(num_portfolios),
        }

        try:
            response = requests.post(
                f"{API_URL}/optimize",
                json=payload,
                timeout=120,
            )

            response.raise_for_status()

            data = response.json()

            st.success("Portfolio optimized successfully!")

            max_sharpe = data["max_sharpe"]
            min_variance = data["min_variance"]

            st.subheader("📊 Portfolio Summary")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Expected Return",
                    f"{max_sharpe['Return']:.2%}",
                )

            with col2:
                st.metric(
                    "Portfolio Risk",
                    f"{max_sharpe['Risk']:.2%}",
                )

            with col3:
                st.metric(
                    "Sharpe Ratio",
                    f"{max_sharpe['Sharpe']:.2f}",
                )

            st.divider()

            left_col, right_col = st.columns([2, 1])

            with left_col:
                st.subheader("📋 Maximum Sharpe Portfolio")

                allocation = {
                    k: v
                    for k, v in max_sharpe.items()
                    if k not in ["Return", "Risk", "Sharpe"]
                }

                allocation_df = pd.DataFrame(
                    {
                        "Stock": allocation.keys(),
                        "Weight": allocation.values(),
                    }
                )

                allocation_df["Weight"] = allocation_df["Weight"] * 100
                allocation_df = allocation_df.sort_values("Weight", ascending=False)

                st.dataframe(
                    allocation_df,
                    use_container_width=True,
                    hide_index=True,
                )

            with right_col:
                st.subheader("🥧 Allocation")

                fig = px.pie(
                    allocation_df,
                    names="Stock",
                    values="Weight",
                    hole=0.45,
                )

                fig.update_layout(height=420)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

            csv = allocation_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇️ Download Allocation CSV",
                data=csv,
                file_name="portfolio_allocation.csv",
                mime="text/csv",
                use_container_width=True,
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")