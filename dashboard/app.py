import streamlit as st
import pandas as pd
import os

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Mumbai Real Estate Intelligence",
    page_icon="🏠",
    layout="wide"
)

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------
BASE_DIR = os.path.dirname(__file__)

df = pd.read_csv("C:/Mumbai_Real_Estate_Intelligence/data/cleaned/mumbai_housing_price_cleaned.csv")

df["Area"] = "Andheri"

df.loc[df["Area_Bandra"] == 1, "Area"] = "Bandra"
df.loc[df["Area_Borivali"] == 1, "Area"] = "Borivali"
df.loc[df["Area_Colaba"] == 1, "Area"] = "Colaba"
df.loc[df["Area_Powai"] == 1, "Area"] = "Powai"

# ---------------------------------------------------
# Title
# ---------------------------------------------------
st.title("🏠 Mumbai Real Estate Intelligence Dashboard")

st.markdown(
"""
### AI-Powered Property Price Prediction & Business Analytics

An end-to-end Data Science project that predicts Mumbai property prices
using **XGBoost**, explains predictions using **SHAP**, and provides
interactive business intelligence dashboards.
"""
)

st.divider()

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏡 Properties",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "📍 Areas Covered",
        df["Area"].nunique()
    )

with col3:
    avg_price = df["Total_Price_Local"].mean()/10000000

    st.metric(
        "💰 Avg Property Price",
        f"₹{avg_price:.2f} Cr"
    )

with col4:
    st.metric(
        "🤖 ML Model",
        "XGBoost"
    )

st.divider()

# ---------------------------------------------------
# About the Project
# ---------------------------------------------------

st.subheader("📌 Project Highlights")

left, right = st.columns(2)

with left:

    st.success("✔ Property Price Prediction")

    st.success("✔ SHAP Explainability")

    st.success("✔ Investment Score Calculator")

with right:

    st.success("✔ Area Comparison Dashboard")

    st.success("✔ Feature Importance Analysis")

    st.success("✔ Business Insights Dashboard")

st.divider()

# ---------------------------------------------------
# Dataset Overview
# ---------------------------------------------------

st.subheader("📊 Dataset Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Average Size",
        f"{df['Size_sqm'].mean():.1f} sqm"
    )

with c2:
    st.metric(
        "Average Bedrooms",
        f"{df['Bedrooms'].mean():.1f}"
    )

with c3:
    expensive_area = (
        df.groupby("Area")["Total_Price_Local"]
        .mean()
        .idxmax()
    )

    st.metric(
        "Most Expensive Area",
        expensive_area
    )

st.divider()

# ---------------------------------------------------
# Navigation Guide
# ---------------------------------------------------

st.subheader("🧭 Dashboard Navigation")

st.info("""
### 📈 Price Prediction
Predict the selling price of a property using the trained XGBoost model.

### 📊 Area Comparison
Compare average prices, property sizes, and bedroom distributions between different areas.

### 🔥 Feature Importance
Understand which features contribute the most to property prices.

### 💰 Investment Score
Evaluate how attractive an area is for real estate investment.

### 📈 Business Insights
Explore key metrics and insights from the Mumbai housing market.
""")

st.divider()

st.caption(
    "Developed using Python • XGBoost • SHAP • Streamlit • Plotly"
)