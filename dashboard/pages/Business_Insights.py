import streamlit as st
import pandas as pd
import plotly.express as px

PRIMARY = "#2563EB"
SECONDARY = "#14B8A6"
ACCENT = "#F59E0B"

df = pd.read_csv("data/cleaned/mumbai_housing_price_cleaned.csv")

st.title("Business Insights")

# Area-wise data

areas = {
    "Andheri":
    (
        (df["Area_Bandra"] == 0) &
        (df["Area_Borivali"] == 0) &
        (df["Area_Colaba"] == 0) &
        (df["Area_Powai"] == 0)
    ),
    "Bandra": df["Area_Bandra"] == 1,
    "Borivali": df["Area_Borivali"] == 1,
    "Colaba": df["Area_Colaba"] == 1,
    "Powai": df["Area_Powai"] == 1
}

summary = []

for area, condition in areas.items():

    temp = df[condition]

    summary.append({

        "Area": area,

        "Average Price": temp["Total_Price_Local"].mean(),

        "Average Price/Sqm": temp["Price_per_sqm_Local"].mean(),

        "Average Size (Sq.m)": temp["Size_sqm"].mean()

    })

summary = pd.DataFrame(summary)

summary["Average Price (Cr)"] = summary["Average Price"] / 10000000

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Avg Property Price", f"₹{df['Total_Price_Local'].mean()/10000000:.2f} Cr")

with col2:
    st.metric("Most Expensive", summary.loc[summary["Average Price"].idxmax(), "Area"])

with col3:
    st.metric("Most Affordable", summary.loc[summary["Average Price"].idxmin(), "Area"])

with col4:
    st.metric("Avg Price/Sqm", f"₹{df['Price_per_sqm_Local'].mean():,.0f}")

st.divider()

# Average Price Chart
st.subheader("🏠 Average Property Price by Area")

fig = px.bar(
    summary,
    x="Area",
    y="Average Price (Cr)",
    text="Average Price (Cr)",
    color="Area",
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig.update_traces(
    texttemplate="₹%{text:.2f} Cr",
    textposition="outside"
)

fig.update_layout(
    height=500,
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

# Price per Sqm
st.subheader("📈 Average Price per Sq.m")

fig = px.bar(
    summary,
    x="Area",
    y="Average Price/Sqm",
    text="Average Price/Sqm",
    color="Area",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig.update_traces(
    texttemplate="₹%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    height=500,
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

# Area Comparison Table

display = summary.copy()

display["Average Price"] = display["Average Price"].apply(
    lambda x: f"₹{x/10000000:.2f} Cr")

display["Average Price/Sqm"] = display["Average Price/Sqm"].apply(
    lambda x: f"₹{x:,.0f}")

display["Average Size (Sq.m)"] = display["Average Size (Sq.m)"].round(2)

display = display.drop(columns=["Average Price (Cr)"])

st.subheader("📋 Area Summary")

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True
)

st.divider()

# Business Recommendations
st.subheader("💼 Business Recommendations")

st.success(f"""
### Premium Market

**{summary.loc[summary['Average Price'].idxmax(),'Area']}** commands the highest average property price and is best suited for luxury residential developments.
""")

st.info(f"""
### Value Investment

**{summary.loc[summary['Average Price'].idxmin(),'Area']}** offers the lowest average property price, making it attractive for first-time buyers and long-term investors.
""")

best_value = summary.loc[summary["Average Price/Sqm"].idxmin(), "Area"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Avg Property Price", f"₹{df['Total_Price_Local'].mean()/10000000:.2f} Cr")

with col2:
    st.metric("Avg Property Size", f"{df['Size_sqm'].mean():.1f} sqm")

with col3:
    st.metric("Avg Price/Sqm", f"₹{df['Price_per_sqm_Local'].mean():,.0f}")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Premium Area", summary.loc[summary["Average Price"].idxmax(), "Area"])

with col5:
    st.metric("Budget Area", summary.loc[summary["Average Price"].idxmin(), "Area"])

with col6:
    st.metric("Total Properties", len(df))

st.warning(f"""
### 📈 Best Value per Square Meter

**{best_value}** has the lowest average price per square meter, providing the best value for buyers seeking maximum living space within their budget.
""")

st.divider()

# Key Findings

st.subheader("Key Findings")

st.markdown("""
- Premium locations command substantially higher property prices.

- Location has a greater influence on property value than the number of bedrooms.

- Price per square meter is the strongest driver of total property price.

- Larger properties generally command higher overall prices.

- Significant price variation across areas highlights the importance of location in real estate investment decisions.

- The XGBoost regression model achieved the highest prediction accuracy among the evaluated models, making it suitable for estimating future property prices.
""")