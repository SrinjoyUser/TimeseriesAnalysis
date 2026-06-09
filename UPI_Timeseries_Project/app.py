import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="UPI Spending Analytics", layout="wide")
st.title("💸 UPI Macro-Economic Spending Dashboard")
st.markdown("Analyzing Indian Consumer Behavior: Discretionary vs. Essential Spending (2016 - 2026)")

# --- LOAD PICKLED DATA ---
@st.cache_data
def load_data():
    wallet_share = pd.read_pickle('wallet_share.pkl')
    spending_index = pd.read_pickle('spending_index.pkl')
    heatmap_data = pd.read_pickle('heatmap_data.pkl')
    forecast_data = pd.read_pickle('forecast_data.pkl')
    return wallet_share, spending_index, heatmap_data, forecast_data

df_wallet, df_index, df_heat, df_forecast = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")
available_years = sorted(list(set([month[:4] for month in df_index.index])))
selected_year = st.sidebar.selectbox("Zoom in on Year:", ["All Time"] + available_years)

if selected_year != "All Time":
    df_wallet = df_wallet[df_wallet.index.str.startswith(selected_year)]
    df_index = df_index[df_index.index.str.startswith(selected_year)]

# --- NEW: EXECUTIVE KPI CARDS ---
st.header("⚡ Key Performance Indicators (Latest Month)")

# Get the last two months of data to calculate Month-over-Month (MoM) growth
current_month = df_index.iloc[-1]
prev_month = df_index.iloc[-2]

# Math for the % change arrows
disc_growth = ((current_month['Discretionary'] - prev_month['Discretionary']) / prev_month['Discretionary']) * 100
ess_growth = ((current_month['Essential'] - prev_month['Essential']) / prev_month['Essential']) * 100
index_growth = ((current_month['Spending_Index'] - prev_month['Spending_Index']) / prev_month['Spending_Index']) * 100

col1, col2, col3 = st.columns(3)
col1.metric(label="Discretionary Spend (Wants)", value=f"₹{current_month['Discretionary']:,.0f}", delta=f"{disc_growth:.1f}% MoM")
col2.metric(label="Essential Spend (Needs)", value=f"₹{current_month['Essential']:,.0f}", delta=f"{ess_growth:.1f}% MoM", delta_color="inverse") # Inverse because higher essential spend is often inflation/stress
col3.metric(label="Spending Index Ratio", value=f"{current_month['Spending_Index']:.2f}", delta=f"{index_growth:.1f}% MoM")
st.markdown("---")

# --- SECTION 1: THE SPENDING INDEX ---
st.header("📉 The Discretionary vs. Essential Spending Index")

# Build the interactive Line Chart
fig_index = go.Figure()

# Plot the Historical Data (Solid Line)
fig_index.add_trace(go.Scatter(
    x=df_index.index, y=df_index['Spending_Index'],
    mode='lines+markers', name='Historical Index',
    line=dict(color='royalblue', width=3)
))

# Plot the AI Forecast (Dotted Line) - THIS IS THE NEW PART!
fig_index.add_trace(go.Scatter(
    x=df_forecast.index, y=df_forecast['Predicted_Index'],
    mode='lines+markers', name='AI Forecast (Next 6 Months)',
    line=dict(color='orange', width=3, dash='dot') # Dotted orange line indicates the future
))

fig_index.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Equilibrium (Wants = Needs)")
fig_index.update_layout(xaxis_title="Month", yaxis_title="Index Ratio", hovermode="x unified")
st.plotly_chart(fig_index, use_container_width=True)

# --- SECTION 2: WALLET SHARE DYNAMICS ---
st.markdown("---")
st.header("📊 Sector-Wise Wallet Share")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    fig_area = px.area(df_wallet, x=df_wallet.index, y=df_wallet.columns,
                       labels={'value': 'Wallet Share (%)', 'index': 'Month', 'variable': 'Sector'},
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_area, use_container_width=True)

with col_chart2:
    selected_month = st.selectbox("Select a Month for Pie Chart:", df_wallet.index)
    month_data = df_wallet.loc[selected_month]
    fig_pie = px.pie(values=month_data.values, names=month_data.index, hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# --- NEW: DAY-OF-WEEK HEATMAP ---
st.markdown("---")
st.header("🔥 Day-of-Week Sector Heatmap")
st.markdown("Identifies exactly *when* consumers are spending money to optimize targeted credit card offers.")

# Transpose the dataframe so Days are on the Y-axis and Sectors are on the X-axis
fig_heat = px.imshow(
    df_heat.T, 
    color_continuous_scale="Blues",
    aspect="auto",
    labels=dict(x="Day of the Week", y="Business Sector", color="Total Spend (INR)")
)
st.plotly_chart(fig_heat, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("🚀 Built for Fintech Risk & Rewards Modeling | Data mathematically anchored to true NPCI 2016-2026 volumes.")