import streamlit as st

st.title("Landslide Risk Monitoring System")
st.write("Simple prototype for SIH")

with st.sidebar:
    rainfall = st.slider("Rainfall", 0, 500, 100)
    slope = st.slider("Slope", 0, 90, 30)
    moisture = st.slider("Soil Moisture", 0, 100, 40)

score = rainfall * 0.4 + slope * 1.5 + moisture * 0.6
st.metric("Risk Score", round(score, 1))

if score < 100:
    st.success("Low Risk")
elif score < 180:
    st.warning("Medium Risk")
else:
    st.error("High Risk")
