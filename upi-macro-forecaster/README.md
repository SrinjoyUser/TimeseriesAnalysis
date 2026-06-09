# 💸 UPI Macro-Economic Spending Forecaster

## 🌐 Live Dashboard
**Try the interactive web app here:** [https://timeseriesanalysis-upi-spending-pattern-forecaster.streamlit.app/]

## Overview
This project is a full-stack data science application that analyzes Indian consumer behavior through the lens of UPI (Unified Payments Interface) transactions. By mapping 10 years of historical data into a custom **Discretionary vs. Essential Spending Index**, this tool identifies macroeconomic shocks (like the 2020 lockdowns), festive spending spikes, and day-of-week consumer habits. 

Furthermore, it utilizes Machine Learning to forecast future spending trends.

## 🚀 Key Features
* **Automated Data Engineering:** Dynamically cleans and merges fragmented NPCI transaction data, utilizing power transformations to correct sampling bias and duplicate drops.
* **The Spending Index:** A mathematical ratio comparing "Wants" (Dining, Entertainment) vs "Needs" (Groceries, Healthcare) over time.
* **Predictive AI Forecasting:** Uses a Holt-Winters Exponential Smoothing model to predict consumer spending behavior 6 months into the future.
* **Interactive Dashboard:** Built with Streamlit and Plotly for real-time data exploration, heatmaps, and MoM KPI tracking.

## 🛠️ Tech Stack
* **Data Engineering:** Python, Pandas, NumPy, Glob
* **Machine Learning:** Statsmodels (Holt-Winters)
* **Visualization & UI:** Streamlit, Plotly Express, Plotly Graph Objects

## ⚙️ How to Run Locally
1. Clone this repository.
2. Install the required packages: `pip install pandas numpy streamlit plotly statsmodels`
3. Run the dashboard: `streamlit run app.py`