import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(
    page_title="NER Landslide Safety System",
    page_icon="⛰️",
    layout="wide"
)

# ---------- Sample data ----------
locations = {
    "East Khasi Hills, Meghalaya": (25.57, 91.88),
    "Aizawl, Mizoram": (23.73, 92.72),
    "Gangtok, Sikkim": (27.33, 88.61),
    "Kohima, Nagaland": (25.67, 94.11),
    "Tawang, Arunachal Pradesh": (27.59, 91.86),
}

sample_reports = pd.DataFrame({
    "Location": [
        "East Khasi Hills",
        "Aizawl",
        "Gangtok",
        "Kohima"
    ],
    "Report": [
        "Roadside cracks reported",
        "Heavy rainfall near hill road",
        "Small rockfall observed",
        "Waterlogged slope"
    ],
    "Priority": [
        "High",
        "Medium",
        "High",
        "Medium"
    ],
    "Status": [
        "Inspection required",
        "Monitoring",
        "Team assigned",
        "Monitoring"
    ]
})

# ---------- Header ----------
st.title("⛰️ NER Landslide Safety System")
st.caption("AI-based early warning and risk monitoring prototype for the North Eastern Region")

st.info(
    "This is a team demonstration prototype. It uses sample conditions "
    "to show how authorities could monitor risk and respond early."
)

# ---------- Sidebar ----------
st.sidebar.title("Control Panel")

district = st.sidebar.selectbox(
    "Choose monitoring area",
    list(locations.keys())
)

st.sidebar.subheader("Enter current conditions")

rainfall = st.sidebar.slider(
    "Rainfall in last 24 hours (mm)",
    0, 500, 120
)

slope = st.sidebar.slider(
    "Slope steepness (degrees)",
    0, 90, 35
)

soil_moisture = st.sidebar.slider(
    "Soil moisture (%)",
    0, 100, 55
)

movement = st.sidebar.slider(
    "Ground movement (mm)",
    0, 100, 10
)

# ---------- Risk calculation ----------
rainfall_score = min(rainfall / 300 * 100, 100)
slope_score = slope / 60 * 100
moisture_score = soil_moisture
movement_score = movement

risk_score = (
    rainfall_score * 0.35
    + slope_score * 0.25
    + moisture_score * 0.20
    + movement_score * 0.20
)

risk_score = round(min(risk_score, 100), 1)

if risk_score < 35:
    risk_level = "LOW"
    risk_color = "green"
    advice = "Continue normal monitoring."
elif risk_score < 65:
    risk_level = "MEDIUM"
    risk_color = "orange"
    advice = "Increase monitoring and inspect vulnerable roads."
else:
    risk_level = "HIGH"
    risk_color = "red"
    advice = "Issue early warning and prepare emergency response."

# ---------- Tabs ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "🧮 Risk Calculator",
    "🗺️ Risk Map",
    "📢 Field Reports",
    "ℹ️ About Project"
])

# ---------- Dashboard ----------
with tab1:
    st.header("Current Situation")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Selected Area", district.split(",")[0])
    col2.metric("Risk Score", f"{risk_score}/100")
    col3.metric("Rainfall", f"{rainfall} mm")
    col4.metric("Ground Movement", f"{movement} mm")

    if risk_level == "LOW":
        st.success(f"🟢 LOW RISK — {advice}")
    elif risk_level == "MEDIUM":
        st.warning(f"🟡 MEDIUM RISK — {advice}")
    else:
        st.error(f"🔴 HIGH RISK — {advice}")

    st.subheader("What is happening?")

    if rainfall > 250:
        st.write("⚠️ Heavy rainfall is increasing the possibility of slope failure.")
    else:
        st.write("🌦️ Rainfall is currently within the demo monitoring range.")

    if soil_moisture > 70:
        st.write("💧 Soil moisture is high, which may reduce slope stability.")
    else:
        st.write("✅ Soil moisture is being monitored.")

    if movement > 30:
        st.write("🚨 Ground movement is high. A field inspection is recommended.")
    else:
        st.write("✅ No major ground movement is detected in this demo.")

    st.subheader("Immediate Action")

    if risk_level == "HIGH":
        st.error(
            "1. Alert district officials\n"
            "2. Inspect nearby roads\n"
            "3. Notify nearby communities\n"
            "4. Prepare evacuation support"
        )
    elif risk_level == "MEDIUM":
        st.warning(
            "1. Increase monitoring\n"
            "2. Check rainfall again after a few hours\n"
            "3. Keep response teams ready"
        )
    else:
        st.success(
            "1. Continue routine monitoring\n"
            "2. Keep field reporting active"
        )

# ---------- Risk Calculator ----------
with tab2:
    st.header("How the Risk Score Is Calculated")

    st.write(
        "The prototype combines four warning factors. "
        "Higher values increase the risk score."
    )

    factor_data = pd.DataFrame({
        "Factor": [
            "Rainfall",
            "Slope",
            "Soil Moisture",
            "Ground Movement"
        ],
        "Current Value": [
            rainfall,
            slope,
            soil_moisture,
            movement
        ],
        "Importance": [
            "Very High",
            "High",
            "Medium",
            "Very High"
        ]
    })

    st.dataframe(factor_data, use_container_width=True)

    st.subheader("Risk Factor Chart")
    chart_data = pd.DataFrame({
        "Factor": ["Rainfall", "Slope", "Soil Moisture", "Movement"],
        "Score": [
            round(rainfall_score, 1),
            round(min(slope_score, 100), 1),
            round(moisture_score, 1),
            round(movement_score, 1)
        ]
    })

    st.bar_chart(chart_data.set_index("Factor"))

    st.subheader("Interpretation")
    st.write(f"Current risk category: **{risk_level}**")
    st.write(f"Suggested action: **{advice}**")

# ---------- Map ----------
with tab3:
    st.header("North Eastern Region Monitoring Map")

    selected_lat, selected_lon = locations[district]

    risk_map = folium.Map(
        location=[25.5, 91.8],
        zoom_start=6
    )

    for name, coordinates in locations.items():
        if name == district:
            marker_color = risk_color
            radius = 18
            popup_text = f"{name} - Selected area - {risk_level} risk"
        else:
            marker_color = "blue"
            radius = 8
            popup_text = f"{name} - Sample monitoring point"

        folium.CircleMarker(
            location=coordinates,
            radius=radius,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.75,
            popup=popup_text
        ).add_to(risk_map)

    st_folium(risk_map, width=1100, height=500)

    st.caption(
        "Green = low risk, orange = medium risk, red = high risk. "
        "Blue points represent other sample monitoring locations."
    )

# ---------- Reports ----------
with tab4:
    st.header("Citizen and Field Officer Reports")

    st.write(
        "Field officers or citizens can report cracks, rockfalls, "
        "blocked roads, or unusual ground movement."
    )

    with st.form("field_report"):
        reporter_name = st.text_input("Name")
        report_location = st.selectbox(
            "Report location",
            list(locations.keys())
        )
        report_type = st.selectbox(
            "Type of report",
            [
                "Slope crack",
                "Rockfall",
                "Blocked road",
                "Heavy rainfall",
                "Ground movement"
            ]
        )
        report_description = st.text_area(
            "Describe what you observed"
        )
        uploaded_photo = st.file_uploader(
            "Upload photo",
            type=["jpg", "jpeg", "png"]
        )

        submit_report = st.form_submit_button("Submit Report")

        if submit_report:
            st.success(
                "Report submitted successfully. "
                "The monitoring team can review it."
            )

    st.subheader("Existing Demo Reports")
    st.dataframe(sample_reports, use_container_width=True)

# ---------- About ----------
with tab5:
    st.header("About This Project")

    st.write(
        "The North Eastern Region frequently experiences landslides "
        "because of heavy rainfall, steep terrain, fragile slopes, "
        "and road cutting."
    )

    st.subheader("Main Goal")
    st.write(
        "To help authorities identify dangerous areas early, "
        "monitor changing conditions, and respond before a disaster becomes worse."
    )

    st.subheader("Planned Real-World Data")
    st.write(
        "The future version can use rainfall data, soil moisture sensors, "
        "satellite images, terrain information, historical landslide records, "
        "and field reports."
    )

    st.subheader("Prototype Team Roles")
    st.write(
        "• Data team: collect rainfall and landslide data\n"
        "• AI team: improve the risk prediction model\n"
        "• GIS team: improve the map\n"
        "• App team: manage the dashboard and reports\n"
        "• Presentation team: explain the solution and impact"
    )

    st.subheader("Important Note")
    st.warning(
        "This is a demonstration model and should not be used for real evacuation decisions."
    )

st.divider()
st.caption(
    f"Prototype last viewed: {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
)
