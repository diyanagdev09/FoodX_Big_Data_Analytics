from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="FoodX | Big Data Analytics",
    page_icon="🍽️",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent

# The GitHub repository currently stores result CSVs in its root directory.
# The second location also supports the structured data/results layout.
def find_csv(filename: str) -> Path | None:
    candidates = [
        BASE_DIR / filename,
        BASE_DIR / "data" / "results" / filename,
    ]
    return next((path for path in candidates if path.is_file()), None)


@st.cache_data(show_spinner=False)
def load_csv(filename: str) -> pd.DataFrame:
    path = find_csv(filename)
    if path is None:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception as exc:
        st.warning(f"Could not read {filename}: {exc}")
        return pd.DataFrame()


restaurant = load_csv("restaurant_analysis.csv")
hourly = load_csv("hourly_demand.csv")
daily = load_csv("daily_demand.csv")
delivery = load_csv("delivery_analysis.csv")
segments = load_csv("customer_segments.csv")
recommendations = load_csv("recommendations.csv")

st.title("🍽️ FoodX")
st.caption("Food Delivery Demand, Customer Behaviour & Restaurant Recommendation Analytics")

required_restaurant_columns = {"Restaurant name", "total_orders", "delivered_orders"}
if restaurant.empty or not required_restaurant_columns.issubset(restaurant.columns):
    st.error(
        "Restaurant analysis data is missing or has an unexpected format. "
        "Keep restaurant_analysis.csv beside app.py or in data/results/."
    )
    st.stop()

# Ensure numeric columns are usable even if a CSV was exported as text.
for frame, columns in [
    (restaurant, ["total_orders", "delivered_orders", "average_order_value", "average_rating"]),
    (hourly, ["Order Hour", "total_orders"]),
    (daily, ["total_orders"]),
    (delivery, ["avg_kpt", "avg_rider_wait", "avg_distance"]),
    (segments, ["customer_count", "avg_orders", "avg_spending", "avg_order_value", "avg_discount"]),
    (recommendations, ["predicted_preference", "average_rating", "total_orders"]),
]:
    for column in columns:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")

# KPI row
c1, c2, c3 = st.columns(3)
c1.metric("Restaurants analysed", f"{len(restaurant):,}")
c2.metric("Orders in restaurant summary", f"{int(restaurant['total_orders'].fillna(0).sum()):,}")
c3.metric("Delivered orders in summary", f"{int(restaurant['delivered_orders'].fillna(0).sum()):,}")

st.divider()
st.subheader("Restaurant performance")
top_restaurants = restaurant.sort_values("total_orders", ascending=False)
color_column = "average_rating" if "average_rating" in top_restaurants.columns else None
st.plotly_chart(
    px.bar(
        top_restaurants,
        x="Restaurant name",
        y="total_orders",
        color=color_column,
        title="Orders by restaurant",
        labels={"total_orders": "Total orders", "average_rating": "Average rating"},
        template="plotly_dark",
    ),
    use_container_width=True,
)
st.dataframe(restaurant, use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.subheader("Demand by hour")
    if not hourly.empty and {"Order Hour", "total_orders"}.issubset(hourly.columns):
        hourly_sorted = hourly.sort_values("Order Hour")
        st.plotly_chart(
            px.line(hourly_sorted, x="Order Hour", y="total_orders", markers=True,
                    title="Orders across the day", template="plotly_dark"),
            use_container_width=True,
        )
    else:
        st.info("Hourly demand data is not available.")

with right:
    st.subheader("Demand by day")
    if not daily.empty and {"Order Day", "total_orders"}.issubset(daily.columns):
        st.plotly_chart(
            px.bar(daily, x="Order Day", y="total_orders", title="Orders by day of week",
                   template="plotly_dark"),
            use_container_width=True,
        )
    else:
        st.info("Daily demand data is not available.")

st.divider()
st.subheader("Delivery operations")
if not delivery.empty and {"Restaurant name", "avg_kpt", "avg_rider_wait"}.issubset(delivery.columns):
    st.plotly_chart(
        px.bar(
            delivery,
            x="Restaurant name",
            y=["avg_kpt", "avg_rider_wait"],
            barmode="group",
            title="Average kitchen preparation and rider wait time",
            labels={"value": "Minutes", "variable": "Metric"},
            template="plotly_dark",
        ),
        use_container_width=True,
    )
    st.dataframe(delivery, use_container_width=True, hide_index=True)
else:
    st.info("Delivery analysis data is not available or is missing required columns.")

left, right = st.columns(2)
with left:
    st.subheader("Customer segments (K-Means)")
    if not segments.empty and {"Customer Segment", "customer_count"}.issubset(segments.columns):
        st.plotly_chart(
            px.pie(segments, names="Customer Segment", values="customer_count", hole=0.45,
                   title="Customer distribution by segment", template="plotly_dark"),
            use_container_width=True,
        )
        st.dataframe(segments, use_container_width=True, hide_index=True)
    else:
        st.info("Customer segmentation data is not available.")

with right:
    st.subheader("ALS restaurant recommendations")
    if not recommendations.empty:
        show_columns = [
            column for column in
            ["Restaurant name", "predicted_preference", "average_rating", "total_orders"]
            if column in recommendations.columns
        ]
        st.dataframe(recommendations[show_columns], use_container_width=True, hide_index=True)
    else:
        st.info("Recommendation data is not available.")

st.divider()
st.caption(
    "Dashboard displays precomputed outputs exported by the PySpark notebook. "
    "Run the notebook to regenerate the analytical results and ML recommendations."
)
