import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="FoodX | Big Data Analytics", page_icon="🍽️", layout="wide")
BASE = Path(__file__).parent
RESULTS = BASE / "data" / "results"

@st.cache_data
def load_csv(name):
    path = RESULTS / name
    return pd.read_csv(path) if path.exists() else pd.DataFrame()

restaurant = load_csv("restaurant_analysis.csv")
hourly = load_csv("hourly_demand.csv")
daily = load_csv("daily_demand.csv")
delivery = load_csv("delivery_analysis.csv")
segments = load_csv("customer_segments.csv")
recommendations = load_csv("recommendations.csv")

st.title("🍽️ FoodX")
st.caption("Food Delivery Demand, Customer Behaviour & Restaurant Recommendation Analytics")

if restaurant.empty:
    st.error("Project result CSVs are missing. Keep the data/results folder in the project.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Restaurants analysed", len(restaurant))
c2.metric("Orders in restaurant summary", f"{int(restaurant['total_orders'].sum()):,}")
c3.metric("Delivered orders in summary", f"{int(restaurant['delivered_orders'].sum()):,}")

st.subheader("Restaurant performance")
top = restaurant.sort_values("total_orders", ascending=False)
st.plotly_chart(px.bar(top, x="Restaurant name", y="total_orders", color="average_rating",
                       title="Orders by restaurant", template="plotly_dark"), use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Demand by hour")
    if not hourly.empty:
        hourly = hourly.sort_values("Order Hour")
        st.plotly_chart(px.line(hourly, x="Order Hour", y="total_orders", markers=True,
                                template="plotly_dark"), use_container_width=True)
with right:
    st.subheader("Demand by day")
    if not daily.empty:
        st.plotly_chart(px.bar(daily, x="Order Day", y="total_orders",
                               template="plotly_dark"), use_container_width=True)

st.subheader("Delivery operations")
if not delivery.empty:
    st.plotly_chart(px.bar(delivery, x="Restaurant name", y=["avg_kpt", "avg_rider_wait"],
                           barmode="group", template="plotly_dark",
                           labels={"value": "Minutes", "variable": "Metric"}),
                    use_container_width=True)
    st.dataframe(delivery, use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.subheader("Customer segments (K-Means)")
    if not segments.empty:
        st.plotly_chart(px.pie(segments, names="Customer Segment", values="customer_count",
                               hole=0.45, template="plotly_dark"), use_container_width=True)
        st.dataframe(segments, use_container_width=True, hide_index=True)
with right:
    st.subheader("ALS restaurant recommendations")
    if not recommendations.empty:
        show_cols = [c for c in ["Restaurant name", "predicted_preference", "average_rating", "total_orders"]
                     if c in recommendations.columns]
        st.dataframe(recommendations[show_cols], use_container_width=True, hide_index=True)

st.caption("Dashboard reads the exported analytical CSVs. Run the Colab notebook to regenerate model outputs.")
