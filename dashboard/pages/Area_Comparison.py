import streamlit as st
import pandas as pd
import plotly.express as px

PRIMARY = "#2563EB"      # Blue
SECONDARY = "#14B8A6"    # Teal
ACCENT = "#F59E0B"       # Orange
BACKGROUND = "#F8FAFC"
FONT = "sans serif"

df = pd.read_csv("data/cleaned/mumbai_housing_price_cleaned.csv")

st.title("Area Comparison")

areas = ["Andheri","Bandra", "Borivali", "Colaba", "Powai"]

area1 = st.selectbox("Select First Area", areas)

area2 = st.selectbox("Select Second Area", areas, index=1)

def get_area_data(area):

    if area == "Andheri":
        return df[
            (df["Area_Bandra"] == 0) &
            (df["Area_Borivali"] == 0) &
            (df["Area_Colaba"] == 0) &
            (df["Area_Powai"] == 0)
        ]

    return df[df[f"Area_{area}"] == 1]


area1_df = get_area_data(area1)
area2_df = get_area_data(area2)

comparison = pd.DataFrame({
    "Area":[area1, area2],
    "Average Price":[
        area1_df["Total_Price_Local"].mean(),
        area2_df["Total_Price_Local"].mean()],
    "Average Price Per Sqm":[
        area1_df["Price_per_sqm_Local"].mean(),
        area2_df["Price_per_sqm_Local"].mean()]
})

# Create Crore column
comparison["Average Price (Cr)"] = comparison["Average Price"] / 10000000

# KPI Cards

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label=f"🏠 {area1}", value=f"₹{comparison.loc[0,'Average Price (Cr)']:.2f} Cr")

with col2:
    st.metric(
        label=f"🏠 {area2}", value=f"₹{comparison.loc[1,'Average Price (Cr)']:.2f} Cr")

st.divider()


# Average Property Price
st.subheader("Average Property Price")
fig = px.bar(
    comparison,
    x="Area",
    y="Average Price (Cr)",
    color="Area",
    text="Average Price (Cr)",
    color_discrete_sequence=[PRIMARY, SECONDARY]
)

fig.update_traces(
    texttemplate="₹%{text:.2f} Cr",
    textposition="outside"
)

fig.update_layout(
    height=450,
    xaxis_title="",
    yaxis_title="Average Price (Crores ₹)",
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=15),
    margin=dict(t=40, l=30, r=30, b=30)
)

st.plotly_chart(fig, use_container_width=True)

# Price per Sqm

st.subheader("Average Price per Sq.m")

fig = px.bar(
    comparison,
    x="Area",
    y="Average Price Per Sqm",
    color="Area",
    text="Average Price Per Sqm",
    color_discrete_sequence=[ACCENT, SECONDARY])

fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")

fig.update_layout(
    height=450,
    xaxis_title="",
    yaxis_title="Price per Sq.m (₹)",
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=15),
    margin=dict(t=40, l=30, r=30, b=30)
)

st.plotly_chart(fig, use_container_width=True)

# Price Distribution

price_df = pd.concat([area1_df.assign(Area=area1), area2_df.assign(Area=area2)])

st.subheader("Property Price Distribution")

fig = px.box(
    price_df,
    x="Area",
    y="Total_Price_Local",
    color="Area",
    color_discrete_sequence=[PRIMARY, SECONDARY],
    points="outliers"
)

fig.update_layout(
    height=500,
    xaxis_title="",
    yaxis_title="Property Price (₹)",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=15)
)

st.plotly_chart(fig, use_container_width=True)

# Summary Table

comparison_display = comparison.copy()

comparison_display["Average Price"] = comparison_display["Average Price"].apply(
    lambda x: f"₹{x/10000000:.2f} Cr")

comparison_display["Average Price Per Sqm"] = comparison_display["Average Price Per Sqm"].apply(
    lambda x: f"₹{x:,.0f}")

comparison_display = comparison_display.drop(columns=["Average Price (Cr)"])

st.subheader("Comparison Summary")

st.dataframe(comparison_display, use_container_width=True, hide_index=True)
