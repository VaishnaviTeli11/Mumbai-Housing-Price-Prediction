import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import os

PRIMARY = "#2563EB"      # Blue
SECONDARY = "#14B8A6"    # Teal
ACCENT = "#F59E0B"       # Orange

# Page Config

st.title("Price Prediction")

# CSS

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.main-title{
    font-size:40px;
    font-weight:bold;
    color:#00B4D8;
}

</style>
""", unsafe_allow_html=True)

# Paths

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

csv_path = os.path.join(
    BASE_DIR,
    "data",
    "cleaned",
    "mumbai_housing_price_cleaned.csv"
)

model_path = os.path.join(
    BASE_DIR,
    "models",
    "final_xgboost_model.pkl"
)

# Load Dataset


try:
    df = pd.read_csv(csv_path)
except Exception as e:
    st.error(f"Could not load dataset.\n\n{e}")
    st.stop()

# Load Model

try:
    with open(model_path, "rb") as file:
        model = pickle.load(file)
except Exception as e:
    st.error(f"Could not load model.\n\n{e}")
    st.stop()

# Title

st.markdown(
    '<p class="main-title"> Mumbai House Price Prediction</p>',
    unsafe_allow_html=True
)

st.write("Predict the market value of a residential property using the trained XGBoost model.")

# Sidebar Inputs

st.sidebar.header("Property Details")

area = st.sidebar.selectbox(
    "Area",
    [
        "Andheri",
        "Bandra",
        "Borivali",
        "Colaba",
        "Powai"
    ]
)

current_year = int(df["Year"].max())

year = st.sidebar.slider(
    "Year",
    min_value=int(df["Year"].min()),
    max_value=2050,
    value=current_year,
    step=1,
    help="Future predictions are estimated using the trained XGBoost model."
)

size = st.sidebar.number_input(
    "Size (sqm)",
    min_value=20,
    max_value=500,
    value=100
)

bedrooms = st.sidebar.number_input(
    "Bedrooms",
    min_value=1,
    max_value=10,
    value=2
)

price_per_sqm = st.sidebar.number_input(
    "Price per sqm",
    min_value=50000,
    max_value=1000000,
    value=250000,
    step=5000
)

predict = st.sidebar.button(
    "🏠 Predict Property Price",
    use_container_width=True
)

# Prediction

if predict:

    input_df = pd.DataFrame({
        "Year":[year],
        "Price_per_sqm_Local":[price_per_sqm],
        "Size_sqm":[size],
        "Bedrooms":[bedrooms],
        "Area_Bandra":[1 if area=="Bandra" else 0],
        "Area_Borivali":[1 if area=="Borivali" else 0],
        "Area_Colaba":[1 if area=="Colaba" else 0],
        "Area_Powai":[1 if area=="Powai" else 0]
    })

    input_df = input_df[
        [
            "Year",
            "Price_per_sqm_Local",
            "Size_sqm",
            "Bedrooms",
            "Area_Bandra",
            "Area_Borivali",
            "Area_Colaba",
            "Area_Powai"
        ]
    ]

    prediction = float(model.predict(input_df)[0])

    # Prediction Result
 
    st.divider()

    st.subheader("Prediction Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Predicted Price", f"₹ {prediction:,.0f}")

    with col2:
        st.metric("Size", f"{size} sqm")

    with col3:
        st.metric("Bedrooms", bedrooms)

# Property Summary

    st.divider()

    st.subheader("📋 Property Summary")

    summary = pd.DataFrame({
        "Feature":[
            "Area",
            "Construction Year",
            "Size (sqm)",
            "Bedrooms",
            "Price per sqm",
            "Predicted Price"
        ],

        "Value":[
            area,
            year,
            size,
            bedrooms,
            f"₹ {price_per_sqm:,.0f}",
            f"₹ {prediction/1e7:.2f} Cr"
        ]
    })

    st.dataframe(summary, use_container_width=True, hide_index=True)

# Investment Score

    score = 50

    # Area score

    if area == "Colaba":
        score += 25

    elif area == "Bandra":
        score += 22

    elif area == "Powai":
        score += 18

    elif area == "Andheri":
        score += 15

    else:
        score += 12

    # Property size

    if size >= 150:
        score += 10

    elif size >= 100:
        score += 7

    elif size >= 70:
        score += 5

    # Bedrooms

    if bedrooms >= 3:
        score += 5

    # Future property

    if year > 2025:
        score += 3

    score = min(score,100)

    st.divider()

    st.subheader("📈 Investment Score")

    st.progress(score/100)

    score_col1, score_col2 = st.columns([1,2])

    with score_col1:
        st.metric("Investment Score", f"{score}/100")

    with score_col2:
        if score >= 90:
            st.success("★★★★★ Excellent Investment")

        elif score >= 80:
            st.success("★★★★☆ Very Good Investment")

        elif score >= 70:
            st.info("★★★★ Good Investment")

        elif score >= 60:
            st.warning("★★★ Average Investment")

        else:
            st.error("★★ Below Average Investment")

# Market Comparison

    st.divider()

    st.subheader("Market Comparison")

    avg_price = df["Total_Price_Local"].mean()

    difference = prediction - avg_price

    pct = (difference / avg_price) * 100

    # Convert to Crores
    avg_price_cr = avg_price / 1e7
    prediction_cr = prediction / 1e7
    difference_cr = difference / 1e7

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Dataset Average", f"₹ {avg_price_cr:.2f} Cr")

    with c2:
        st.metric("Difference", f"₹ {difference_cr:+.2f} Cr")

    with c3:
        st.metric("% Difference", f"{pct:.2f}%")

# Price Visualization

    st.divider()
    st.subheader("Price Comparison")

    comparison_df = pd.DataFrame({
        "Category": [
            "Predicted Price",
            "Dataset Average"
        ],
        "Price": [
            prediction,
            avg_price
        ]
    })

    fig = px.bar(
    comparison_df,
    x="Category",
    y="Price",
    color="Category",
    text="Price",
    color_discrete_sequence=[PRIMARY, ACCENT]
    )

    fig.update_traces(
        texttemplate="₹ %{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        showlegend=False,
        height=420,
        xaxis_title="",
        yaxis_title="Price (₹)",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

# Future Price Projection

    st.divider()

    st.subheader("Estimated Future Property Value")

    future_years = list(range(max(year, 2025), 2051))

    growth_rate = 0.06   # 6% yearly appreciation

    future_prices = []

    for y in future_years:

        years_passed = y - max(year, 2025)

        future_price = prediction * ((1 + growth_rate) ** years_passed)

        future_prices.append(future_price)

    future_df = pd.DataFrame({
        "Year": future_years,
        "Estimated Price": future_prices
    })

    
    fig = px.line(
    future_df,
    x="Year",
    y="Estimated Price",
    markers=True
    )

    fig.update_traces(
        line=dict(color=SECONDARY, width=4),
        marker=dict(size=9)
    )

    fig.update_layout(
        height=430,
        template="plotly_white",
        xaxis_title="Year",
        yaxis_title="Predicted Price (₹)"
    )

    st.plotly_chart(fig, use_container_width=True)
# AI Investment Recommendation

    st.divider()

    st.subheader("🤖 AI Investment Insight")

    if score >= 90:
        st.success("""
    This property is an **excellent investment opportunity**.

    ✔ Premium locality

    ✔ High appreciation potential

    ✔ Strong resale value

    ✔ Suitable for long-term investment
    """)

    elif score >= 75:
        st.info("""
    This property has **strong investment potential**.

    ✔ Good location

    ✔ Good resale prospects

    ✔ Recommended for medium to long-term investment.
    """)

    elif score >= 60:
        st.warning("""
    This property offers **average investment potential**.

    Consider comparing similar properties before making a purchase.
    """)

    else:
        st.error("""
    Investment potential appears below average.

    Further market research is recommended before purchasing.
    """)

# Price Per Square Meter

    st.divider()

    st.subheader("Price Per Square Meter")

    st.metric("Price / sqm", f"₹ {prediction/size:,.0f}")

# Download Prediction Report

    st.divider()

    st.subheader("Download Prediction Report")

    report = pd.DataFrame({

        "Feature":[
            "Area",
            "Construction Year",
            "Property Size",
            "Bedrooms",
            "Predicted Price",
            "Investment Score"
        ],

        "Value":[
            area,
            year,
            size,
            bedrooms,
            prediction,
            score
        ]

    })

    csv = report.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Report",
        data=csv,
        file_name="property_prediction_report.csv",
        mime="text/csv"
    )

# Disclaimer

    st.divider()

    st.caption(
    """
    Predictions are generated using the trained Machine Learning model and
    should be treated as estimates rather than exact market values.
    """
    )