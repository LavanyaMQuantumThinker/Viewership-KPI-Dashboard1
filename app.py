print("Hello, VS Code!")

import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv(r"C:\Users\Lavanya\OneDrive\Desktop\Behindwoods\viewership_dashboard_data.csv")


st.title("📊 Viewership KPI Dashboard")
st.write("Analyze multi-platform video performance for Behindwoods")

# KPI Tilegit s
st.subheader("Key Performance Indicators")
st.metric("Total Views", f"{df['Views'].sum():,}")
st.metric("Average CTR (%)", f"{df['CTR (%)'].mean():.2f}")
st.metric("Average Watch Time (min)", f"{df['Avg Watch Time'].mean():.2f}")

# Line chart: Views over Time
st.subheader("📈 Views Over Time")
daily_views = df.groupby("Date")["Views"].sum().reset_index()
fig_line = px.line(daily_views, x="Date", y="Views", title="Total Daily Views")
st.plotly_chart(fig_line)

# Bar chart: Top 5 Videos
st.subheader("🏆 Top 5 Performing Videos")
top_videos = df.groupby("Video Title")["Views"].sum().sort_values(ascending=False).head(5).reset_index()
fig_bar = px.bar(top_videos, x="Video Title", y="Views", color="Views")
st.plotly_chart(fig_bar)

# Pie chart: Platform-wise Engagement
st.subheader("📊 Platform Engagement Distribution")
platform_engagement = df.groupby("Platform")["Views"].sum().reset_index()
fig_pie = px.pie(platform_engagement, names="Platform", values="Views", title="Views by Platform")
st.plotly_chart(fig_pie)