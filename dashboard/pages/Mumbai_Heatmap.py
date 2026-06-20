import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# PAGE TITLE

st.title("Mumbai Real Estate Area Map")

st.markdown("""
Explore the major residential areas included in the dataset.
Click on any location to view key real estate statistics.
""")

# LOAD DATA

df = pd.read_csv("data/cleaned/mumbai_housing_price_cleaned.csv")

# MAP

mumbai_map = folium.Map(
    location=[19.0760, 72.8777],
    zoom_start=11,
    tiles="CartoDB positron"
)

# AREA DETAILS

areas = {
    "Andheri": {
        "coords":[19.1136,72.8697],
        "condition":
        (
            (df["Area_Bandra"]==0)&
            (df["Area_Borivali"]==0)&
            (df["Area_Colaba"]==0)&
            (df["Area_Powai"]==0)
        ),
        "color":"blue"
    },

    "Bandra":{
        "coords":[19.0596,72.8295],
        "condition":df["Area_Bandra"]==1,
        "color":"green"
    },

    "Borivali":{
        "coords":[19.2307,72.8567],
        "condition":df["Area_Borivali"]==1,
        "color":"orange"
    },

    "Colaba":{
        "coords":[18.9067,72.8147],
        "condition":df["Area_Colaba"]==1,
        "color":"red"
    },

    "Powai":{
        "coords":[19.1176,72.9060],
        "condition":df["Area_Powai"]==1,
        "color":"purple"
    }

}

# ADD MARKERS

for area, details in areas.items():

    temp = df[details["condition"]]

    avg_price = temp["Total_Price_Local"].mean()/10000000

    avg_size = temp["Size_sqm"].mean()

    avg_ppsqm = temp["Price_per_sqm_Local"].mean()

    properties = len(temp)

    popup = f"""
    <b>{area}</b><br><br>

    <b>Average Price:</b> ₹{avg_price:.2f} Cr<br>

    <b>Average Size:</b> {avg_size:.1f} sqm<br>

    <b>Price/Sqm:</b> ₹{avg_ppsqm:,.0f}<br>

    <b>Properties:</b> {properties}
    """

    folium.CircleMarker(

        location=details["coords"],

        radius=12,

        color=details["color"],

        fill=True,

        fill_color=details["color"],

        fill_opacity=0.8,

        popup=folium.Popup(
            popup,
            max_width=300
        ),

        tooltip=f"{area}"

    ).add_to(
        mumbai_map
    )

# DISPLAY MAP

st_folium(
    mumbai_map,
    width=None,
    height=600
)

st.info("""
**Tip:** Hover over a location to view its name and click on the marker to see
average property price, property size, price per square metre and number of listings.
""")