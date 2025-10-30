import pandas as pd
import streamlit as st
import plotly.express as px

# 🧵 Page setup
st.set_page_config(page_title="Thread & Trend Dashboard", page_icon="🧵", layout="wide")
st.title("🧵 Thread & Trend | Customer Retention Dashboard")

# 📂 File upload
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Read the Excel sheet
    df = pd.read_excel(uploaded_file, sheet_name="Sheet1")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.dropna(subset=["Date"], inplace=True)

    st.success("✅ Data loaded successfully!")
    st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")
    st.dataframe(df.head())

    # --- KPIs ---
    total_revenue = df["Revenue"].sum()
    total_ad_spend = df["Ad Spend"].sum()
    total_conversions = df["Conversions"].sum()
    roi = (total_revenue - total_ad_spend) / total_ad_spend * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("📢 Total Ad Spend", f"${total_ad_spend:,.0f}")
    col3.metric("🛍️ Conversions", f"{total_conversions:,}")
    col4.metric("📈 ROI", f"{roi:.2f}%")

    st.markdown("---")

    # --- Channel Performance ---
    st.subheader("📊 Channel Performance")
    channel_perf = df.groupby("Channel")[["Revenue", "Ad Spend", "Conversions"]].sum().sort_values("Revenue", ascending=False)
    channel_perf["ROI (%)"] = (channel_perf["Revenue"] - channel_perf["Ad Spend"]) / channel_perf["Ad Spend"] * 100
    st.dataframe(channel_perf)

    fig_channel = px.bar(channel_perf, x=channel_perf.index, y="Revenue", color="Revenue",
                         title="Revenue by Channel", text_auto=True)
    st.plotly_chart(fig_channel, use_container_width=True)

    # --- Seasonal Trends ---
    st.subheader("🍂 Seasonal Buying Trends")
    season_perf = df.groupby("Season")[["Revenue", "Conversions"]].mean()
    fig_season = px.bar(season_perf, x=season_perf.index, y="Revenue", color="Revenue",
                        title="Average Revenue by Season", text_auto=True)
    st.plotly_chart(fig_season, use_container_width=True)

    # --- Customer Type Insights ---
    st.subheader("🧍 Customer Type Insights")
    cust_perf = df.groupby("Customer Type")[["Revenue", "Conversions", "Ad Spend"]].mean()
    fig_cust = px.bar(cust_perf, x=cust_perf.index, y="Revenue", color="Revenue",
                      title="Average Revenue by Customer Type", text_auto=True)
    st.plotly_chart(fig_cust, use_container_width=True)

    # --- Time of Day ---
    st.subheader("⏰ Time of Day Performance")
    time_perf = df.groupby("Time of Day")[["Revenue", "Conversions"]].mean()
    fig_time = px.bar(time_perf, x=time_perf.index, y="Revenue", color="Revenue",
                      title="Average Revenue by Time of Day", text_auto=True)
    st.plotly_chart(fig_time, use_container_width=True)

    # --- Summary ---
    st.markdown("### 📈 Summary Highlights")
    st.markdown(f"""
    - 🏆 **Top Channel:** {channel_perf['Revenue'].idxmax()}  
    - 🌤 **Best Season:** {season_perf['Revenue'].idxmax()}  
    - 👥 **Best Customer Type:** {cust_perf['Revenue'].idxmax()}  
    - ⏱ **Best Time of Day:** {time_perf['Revenue'].idxmax()}  
    - 💹 **Overall ROI:** {roi:.2f}%
    """)

else:
    st.info("👆 Please upload your Excel file to start analysis.")
