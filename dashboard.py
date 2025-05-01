import streamlit as st
import pandas as pd
import plotly.express as px

# Load datasets
game_df = pd.read_csv("game_summary.csv")
studio_df = pd.read_csv("studio_summary.csv")
region_device_df = pd.read_csv("region_device_summary.csv")
game_type_df = pd.read_csv("game_type_summary.csv")

st.set_page_config(page_title="Game Engagement Dashboard", layout="wide")
st.title("🎮 Game Engagement Dashboard")

# --- KPI Cards ---
col1, col2, col3, col4 = st.columns(4)

top_game = game_df.loc[game_df['duration_minutes'].idxmax()]
top_retention_game = game_df.loc[game_df['avg_retention'].idxmax()]
top_studio = studio_df.loc[studio_df['duration_minutes'].idxmax()]
top_monetized_game = game_df.loc[game_df['in_game_currency_spent'].idxmax()]

col1.metric("Top Engaged Game", top_game['game_name'], f"{int(top_game['duration_minutes'])} mins")
col2.metric("Best Retention Game", top_retention_game['game_name'], f"{top_retention_game['avg_retention']*100:.1f}%")
col3.metric("Top Performing Studio", top_studio['studio_id'], f"{int(top_studio['duration_minutes'])} mins")
col4.metric("Top Monetized Game", top_monetized_game['game_name'], f"${top_monetized_game['in_game_currency_spent']}")

# --- Game Engagement Visualization ---
st.subheader("📊 Game Engagement Overview")
fig1 = px.scatter(
    game_df,
    x="duration_minutes",
    y="avg_retention",
    size="in_game_currency_spent",
    color="game_type",
    hover_name="game_name",
    title="Engagement vs Retention by Game"
)
st.plotly_chart(fig1, use_container_width=True)

# --- Studio Performance ---
st.subheader("🏢 Studio Performance")
fig2 = px.bar(
    studio_df,
    x="studio_id",
    y=["duration_minutes", "in_game_currency_spent"],
    barmode="group",
    title="Total Session Duration & Currency Spent by Studio"
)
st.plotly_chart(fig2, use_container_width=True)

# --- Region and Device Engagement ---
st.subheader("🌍 Engagement by Region & Device")
fig3 = px.density_heatmap(
    region_device_df,
    x="device_type",
    y="region",
    z="duration_minutes",
    color_continuous_scale="Viridis",
    title="Session Duration Heatmap"
)
st.plotly_chart(fig3, use_container_width=True)

# --- Game Type Comparison ---
st.subheader("⚖️ Game Type Comparison")
fig4 = px.box(
    game_df,
    x="game_type",
    y="duration_minutes",
    points="all",
    title="Session Duration Distribution by Game Type"
)
st.plotly_chart(fig4, use_container_width=True)

fig5 = px.box(
    game_df,
    x="game_type",
    y="avg_retention",
    points="all",
    title="Retention Distribution by Game Type"
)
st.plotly_chart(fig5, use_container_width=True)

fig6 = px.box(
    game_df,
    x="game_type",
    y="in_game_currency_spent",
    points="all",
    title="Currency Spent by Game Type"
)
st.plotly_chart(fig6, use_container_width=True)

st.caption("Built for publisher-level insight into game performance, engagement, and investment strategy.")
