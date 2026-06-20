import streamlit as st
import pandas as pd
import plotly.express as px

# Theme

PRIMARY = "#2563EB"
SECONDARY = "#14B8A6"
ACCENT = "#F59E0B"

st.title("Investment Score Engine")

st.markdown("""
This score ranks Mumbai areas based on affordability, value for money,
average property size and market availability.

A **higher score indicates a more attractive investment opportunity.**
""")

# Load Data

df = pd.read_csv("data/cleaned/mumbai_housing_price_cleaned.csv")

# Area Filters
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

        "Average Size": temp["Size_sqm"].mean(),

        "Properties": len(temp)

    })

score_df = pd.DataFrame(summary)

# Normalization

score_df["Price Score"] = (
    1 - (
        (score_df["Average Price"] - score_df["Average Price"].min()) /
        (score_df["Average Price"].max() - score_df["Average Price"].min())
    )
) * 100

score_df["PPSQM Score"] = (
    1 - (
        (score_df["Average Price/Sqm"] - score_df["Average Price/Sqm"].min()) /
        (score_df["Average Price/Sqm"].max() - score_df["Average Price/Sqm"].min())
    )
) * 100

score_df["Size Score"] = (
    (score_df["Average Size"] - score_df["Average Size"].min()) /
    (score_df["Average Size"].max() - score_df["Average Size"].min())
) * 100

score_df["Listing Score"] = (
    (score_df["Properties"] - score_df["Properties"].min()) /
    (score_df["Properties"].max() - score_df["Properties"].min())
) * 100

# Final Investment Score

score_df["Investment Score"] = (

    score_df["Price Score"] * 0.35 +

    score_df["PPSQM Score"] * 0.35 +

    score_df["Size Score"] * 0.20 +

    score_df["Listing Score"] * 0.10

)

score_df["Investment Score"] = score_df["Investment Score"].round(1)

score_df = score_df.sort_values(by="Investment Score", ascending=False)

# KPI Cards

best = score_df.iloc[0]

worst = score_df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Best Investment", best["Area"])

with col2:
    st.metric("Investment Score", f"{best['Investment Score']:.1f}/100")

with col3:
    st.metric("Lowest Ranked", worst["Area"])

with col4:
    st.metric("Areas Analysed", len(score_df))

st.divider()

# Chart

st.subheader("📈 Area-wise Investment Score")

fig = px.bar(
    score_df,
    x="Area",
    y="Investment Score",
    color="Investment Score",
    text="Investment Score",
    color_continuous_scale="Viridis"
)

fig.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

fig.update_layout(
    height=500,
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False,
    coloraxis_showscale=False,
    xaxis_title="",
    yaxis_title="Investment Score",
    font=dict(size=15)
)

st.plotly_chart(fig, use_container_width=True)

# Rankings

display = score_df.copy()

display["Average Price"] = display["Average Price"].apply(
    lambda x: f"₹{x/10000000:.2f} Cr")

display["Average Price/Sqm"] = display["Average Price/Sqm"].apply(
    lambda x: f"₹{x:,.0f}")

display["Average Size"] = display["Average Size"].round(1)

display = display[
    [
        "Area",
        "Investment Score",
        "Average Price",
        "Average Price/Sqm",
        "Average Size",
        "Properties"
    ]
]

st.subheader("Investment Rankings")

st.dataframe(display, use_container_width=True, hide_index=True)

st.divider()

# Recommendation

st.subheader("Investment Recommendation")

st.success(
    f"""
### Recommended Area: **{best['Area']}**

This area achieved the highest investment score based on:

- Competitive property prices
- Attractive price per square meter
- Larger average property size
- Healthy number of available properties

Overall, it offers the strongest balance between affordability and long-term investment potential.
"""
)

st.info("""
### How is the score calculated?

- 35% → Lower average property price
- 35% → Lower price per square meter
- 20% → Larger average property size
- 10% → Higher market availability

Scores are normalized to a 0–100 scale to allow fair comparison across areas.
""")