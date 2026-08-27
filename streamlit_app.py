import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="NER Landslide Monitor",
    page_icon="⛰️",
    layout="wide"
)

st.title("⛰️ NER Landslide Early Warning System")
st.write("Prototype dashboard for monitoring landslide risk in the North Eastern Region.")

st.sidebar.header("Select Location")

district = st.sidebar.selectbox(
    "District",
    [
        "East Khasi Hills, Meghalaya",
        "Aizawl, Mizoram",
        "Gangtok, Sikkim",
        "Kohima, Nagaland",
        "Tawang, Arunachal Pradesh"
    ]
)

st.sidebar.header("Current Conditions")

rainfall = st.sidebar.slider("Rainfall in last 24 hours (mm)", 0, 500, 120)
slope = st.sidebar.slider("Slope angle (degrees)", 0, 90, 35)
soil_moisture = st.sidebar.slider("Soil moisture (%)", 0, 100, 55)
ground_movement = st.sidebar.slider("Ground movement (mm)", 0, 100, 10)

risk_score = (
    rainfall * 0.30
    + slope * 0.25
    + soil_moisture * 0.25
    + ground_movement * 0.20
)

risk_score = min(round(risk_score, 1), 100)

if risk_score < 35:
    risk_level = "LOW"
    message = "No immediate warning. Continue regular monitoring."
elif risk_score < 65:
    risk_level = "MEDIUM"
    message = "Caution advised. Increase monitoring and prepare local officials."
else:
    risk_level = "HIGH"
    message = "Early warning recommended. Inspect roads and alert nearby communities."

st.subheader(f"Risk Status: {district}")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Risk Score", f"{risk_score}/100")
col2.metric("Rainfall", f"{rainfall} mm")
col3.metric("Soil Moisture", f"{soil_moisture}%")
col4.metric("Ground Movement", f"{ground_movement} mm")

if risk_level == "LOW":
    st.success(f"🟢 {risk_level} RISK — {message}")
elif risk_level == "MEDIUM":
    st.warning(f"🟡 {risk_level} RISK — {message}")
else:
    st.error(f"🔴 {risk_level} RISK — {message}")

st.subheader("Risk Factors")

factor_data = pd.DataFrame({
    "Factor": ["Rainfall", "Slope", "Soil Moisture", "Ground Movement"],
    "Value": [rainfall, slope, soil_moisture, ground_movement]
})

st.bar_chart(factor_data.set_index("Factor"))

st.subheader("NER Risk Monitoring Map")

locations = {
    "East Khasi Hills, Meghalaya": (25.57, 91.88),
    "Aizawl, Mizoram": (23.73, 92.72),
    "Gangtok, Sikkim": (27.33, 88.61),
    "Kohima, Nagaland": (25.67, 94.11),
    "Tawang, Arunachal Pradesh": (27.59, 91.86)
}

latitude, longitude = locations[district]

map_object = folium.Map(
    location=[latitude, longitude],
    zoom_start=7
)

color = "green" if risk_level == "LOW" else "orange" if risk_level == "MEDIUM" else "red"

folium.CircleMarker(
    location=[latitude, longitude],
    radius=18,
    color=color,
    fill=True,
    fill_color=color,
    fill_opacity=0.7,
    popup=f"{district} - {risk_level} Risk"
).add_to(map_object)

st_folium(map_object, width=1000, height=450)

st.subheader("Citizen or Field Officer Report")

with st.form("report_form"):
    name = st.text_input("Your name")
    issue = st.selectbox(
        "Report type",
        ["Slope crack", "Road blocked", "Rockfall", "Heavy rainfall", "Ground movement"]
    )
    description = st.text_area("Describe the problem")
    photo = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Submit Report")

    if submitted:
        st.success("Report submitted successfully for review.")
