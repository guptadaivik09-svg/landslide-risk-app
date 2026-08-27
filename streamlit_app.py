import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(
    page_title="LandGuard NER",
    page_icon="⛰️",
    layout="wide"
)

# ---------------- SAMPLE DATA ----------------

locations = {
    "Mawphlang": (25.48, 91.75),
    "Shillong Bypass": (25.58, 91.88),
    "Sohra Road": (25.27, 91.73),
    "Nongpoh": (25.90, 91.88),
    "Mawsynram": (25.30, 91.58)
}

location_data = {
    "Mawphlang": {
        "rainfall": 280,
        "soil": 78,
        "slope": 62,
        "movement": 42,
        "population": 3200,
        "road": "Important district road",
        "hospital": 1,
        "school": 3
    },
    "Shillong Bypass": {
        "rainfall": 210,
        "soil": 65,
        "slope": 48,
        "movement": 25,
        "population": 8500,
        "road": "Major highway",
        "hospital": 2,
        "school": 5
    },
    "Sohra Road": {
        "rainfall": 360,
        "soil": 84,
        "slope": 70,
        "movement": 55,
        "population": 1900,
        "road": "Tourist and local road",
        "hospital": 0,
        "school": 2
    },
    "Nongpoh": {
        "rainfall": 150,
        "soil": 45,
        "slope": 30,
        "movement": 8,
        "population": 2100,
        "road": "Local road",
        "hospital": 1,
        "school": 2
    },
    "Mawsynram": {
        "rainfall": 250,
        "soil": 70,
        "slope": 55,
        "movement": 18,
        "population": 2800,
        "road": "Hill road",
        "hospital": 0,
        "school": 2
    }
}

# ---------------- FUNCTIONS ----------------

def calculate_risk(rainfall, soil, slope, movement):
    rainfall_score = min((rainfall / 400) * 100, 100)
    soil_score = soil
    slope_score = min((slope / 70) * 100, 100)
    movement_score = min((movement / 60) * 100, 100)

    score = (
        rainfall_score * 0.35
        + soil_score * 0.20
        + slope_score * 0.25
        + movement_score * 0.20
    )

    return round(min(score, 100), 1)


def risk_category(score):
    if score <= 25:
        return "LOW", "green"
    elif score <= 50:
        return "MODERATE", "yellow"
    elif score <= 75:
        return "HIGH", "orange"
    return "CRITICAL", "red"


def priority_score(risk, population, road, hospital, school):
    road_value = {
        "Major highway": 25,
        "Important district road": 20,
        "Tourist and local road": 15,
        "Hill road": 12,
        "Local road": 8
    }

    exposure = min(population / 100, 40)
    infrastructure = (
        road_value.get(road, 10)
        + hospital * 8
        + school * 3
    )

    score = risk * 0.55 + exposure + infrastructure
    return round(min(score, 100), 1)


# ---------------- HEADER ----------------

st.title("⛰️ LandGuard NER")
st.subheader("AI-Based Landslide Early Warning & Response System")

st.write(
    "A decision-support prototype that converts landslide risk into "
    "prioritized disaster-response action."
)

st.info(
    "Demo flow: Predict → Verify → Prioritize → Alert → Respond"
)

# ---------------- SIDEBAR ----------------

st.sidebar.header("Monitoring Control")

selected_location = st.sidebar.selectbox(
    "Select monitoring location",
    list(location_data.keys())
)

data = location_data[selected_location]

st.sidebar.write("Current demo conditions")

rainfall = st.sidebar.slider(
    "Rainfall in last 24 hours (mm)",
    0, 500, data["rainfall"]
)

soil = st.sidebar.slider(
    "Soil moisture (%)",
    0, 100, data["soil"]
)

slope = st.sidebar.slider(
    "Slope steepness (degrees)",
    0, 90, data["slope"]
)

movement = st.sidebar.slider(
    "Ground movement (mm)",
    0, 100, data["movement"]
)

risk = calculate_risk(rainfall, soil, slope, movement)
category, map_color = risk_category(risk)

priority = priority_score(
    risk,
    data["population"],
    data["road"],
    data["hospital"],
    data["school"]
)

if priority >= 75:
    priority_level = "P1 - Immediate Action"
elif priority >= 50:
    priority_level = "P2 - High Priority"
elif priority >= 30:
    priority_level = "P3 - Monitor Closely"
else:
    priority_level = "P4 - Routine Monitoring"

# ---------------- TABS ----------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Command Dashboard",
    "🤖 Risk Prediction",
    "🚨 Response Priority",
    "📸 Field Verification",
    "🛟 Emergency Response"
])

# ---------------- TAB 1 ----------------

with tab1:
    st.header("District Command Center")
    st.write(f"Currently monitoring: **{selected_location}, East Khasi Hills**")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Critical Zones", "2")
    col2.metric("High-Risk Zones", "4")
    col3.metric("Open Reports", "7")
    col4.metric("Roads at Risk", "3")

    st.divider()

    st.subheader(f"Current Status: {selected_location}")

    if category == "LOW":
        st.success(f"🟢 {category} RISK")
    elif category == "MODERATE":
        st.warning(f"🟡 {category} RISK")
    elif category == "HIGH":
        st.warning(f"🟠 {category} RISK")
    else:
        st.error(f"🔴 {category} RISK")

    col1, col2, col3 = st.columns(3)

    col1.metric("Landslide Risk", f"{risk}/100")
    col2.metric("Response Priority", priority_level)
    col3.metric("Population Exposed", f"{data['population']:,}")

    st.subheader("Why is this location being monitored?")

    reasons = []

    if rainfall >= 250:
        reasons.append("High rainfall detected")

    if soil >= 70:
        reasons.append("Soil moisture is high")

    if slope >= 50:
        reasons.append("Steep slope detected")

    if movement >= 30:
        reasons.append("Ground movement reported")

    if reasons:
        for reason in reasons:
            st.write(f"⚠️ {reason}")
    else:
        st.write("✅ No major warning indicator detected.")

# ---------------- TAB 2 ----------------

with tab2:
    st.header("AI Risk Prediction")

    st.write(
        "The prototype combines rainfall, soil moisture, slope, "
        "and ground movement to calculate a risk score."
    )

    factor_table = pd.DataFrame({
        "Input Factor": [
            "Rainfall",
            "Soil Moisture",
            "Slope",
            "Ground Movement"
        ],
        "Current Value": [
            f"{rainfall} mm",
            f"{soil}%",
            f"{slope} degrees",
            f"{movement} mm"
        ],
        "Effect": [
            "Very High" if rainfall > 250 else "Moderate",
            "High" if soil > 70 else "Moderate",
            "High" if slope > 50 else "Moderate",
            "Very High" if movement > 30 else "Low"
        ]
    })

    st.dataframe(factor_table, use_container_width=True)

    st.subheader("Risk Indicator Chart")

    chart_data = pd.DataFrame({
        "Factor": [
            "Rainfall",
            "Soil Moisture",
            "Slope",
            "Ground Movement"
        ],
        "Score": [
            min(rainfall / 4, 100),
            soil,
            min(slope / 0.7, 100),
            min(movement / 0.6, 100)
        ]
    })

    st.bar_chart(chart_data.set_index("Factor"))

    st.metric("AI Risk Score", f"{risk}/100")

    st.caption(
        "This is a demonstration scoring model. A production system "
        "would be trained using historical and real-time data."
    )

# ---------------- TAB 3 ----------------

with tab3:
    st.header("Response Priority Engine")

    st.write(
        "Two places may have similar landslide risk, but the location "
        "with more people and critical infrastructure should be handled first."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Risk Score", f"{risk}/100")
    col2.metric("Population Exposed", f"{data['population']:,}")
    col3.metric("Hospitals", data["hospital"])
    col4.metric("Schools", data["school"])

    st.subheader("Priority Result")

    if priority_level.startswith("P1"):
        st.error(f"🚨 {priority_level}")
    elif priority_level.startswith("P2"):
        st.warning(f"🟠 {priority_level}")
    else:
        st.info(f"📍 {priority_level}")

    st.write(f"Nearby road: **{data['road']}**")
    st.write(
        "The priority score considers hazard risk, exposed population, "
        "roads, hospitals, and schools."
    )

    comparison = pd.DataFrame({
        "Location": [
            selected_location,
            "Example low-exposure location"
        ],
        "Risk Score": [
            risk,
            91
        ],
        "Population": [
            data["population"],
            300
        ],
        "Priority": [
            priority_level,
            "P2 - High Priority"
        ]
    })

    st.subheader("Why Risk Alone Is Not Enough")
    st.dataframe(comparison, use_container_width=True)

# ---------------- TAB 4 ----------------

with tab4:
    st.header("Field Verification")

    st.write(
        "Citizens and field officers can report cracks, rockfall, "
        "blocked roads, or unusual slope movement."
    )

    with st.form("field_report"):
        name = st.text_input("Reporter name")
        report_location = st.selectbox(
            "Location",
            list(location_data.keys())
        )
        report_type = st.selectbox(
            "Report type",
            [
                "Ground crack",
                "Rockfall",
                "Blocked road",
                "Water seepage",
                "Slope movement"
            ]
        )
        description = st.text_area("Describe the observation")
        photo = st.file_uploader(
            "Upload field photo",
            type=["jpg", "jpeg", "png"]
        )

        submitted = st.form_submit_button("Submit Report")

        if submitted:
            st.success(
                "Report received successfully. "
                "It has been added for human verification."
            )

            st.write("AI-assisted verification status: **Pending review**")
            st.write("Human verification required before official action.")

    st.subheader("Sample Reports")

    reports = pd.DataFrame({
        "Location": [
            "Mawphlang",
            "Sohra Road",
            "Shillong Bypass"
        ],
        "Observation": [
            "Surface cracks",
            "Rockfall near road",
            "Water seepage"
        ],
        "AI Confidence": [
            "87%",
            "79%",
            "71%"
        ],
        "Status": [
            "Needs inspection",
            "Team assigned",
            "Under review"
        ]
    })

    st.dataframe(reports, use_container_width=True)

# ---------------- TAB 5 ----------------

with tab5:
    st.header("Emergency Response")

    st.write(
        "The response team can use the priority level to decide "
        "what action should happen first."
    )

    if priority_level.startswith("P1"):
        st.error("IMMEDIATE RESPONSE REQUIRED")

        st.checkbox("Alert district disaster management authority")
        st.checkbox("Inspect road and nearby slope")
        st.checkbox("Notify nearby settlements")
        st.checkbox("Prepare evacuation support")
        st.checkbox("Send response team")

    elif priority_level.startswith("P2"):
        st.warning("HIGH PRIORITY RESPONSE")

        st.checkbox("Increase monitoring")
        st.checkbox("Inspect vulnerable road")
        st.checkbox("Keep response team ready")
        st.checkbox("Contact local officer")

    else:
        st.success("ROUTINE MONITORING")

        st.checkbox("Continue regular monitoring")
        st.checkbox("Review weather forecast")
        st.checkbox("Keep field reporting active")

    st.subheader("Alert Preview")

    st.text_area(
        "Message that can be sent to authorities/community",
        value=(
            f"LANDGUARD NER ALERT\n"
            f"Location: {selected_location}\n"
            f"Risk: {category}\n"
            f"Risk Score: {risk}/100\n"
            f"Priority: {priority_level}\n"
            f"Action: Inspect vulnerable areas and follow local safety instructions."
        ),
        height=180
    )

    st.button("Simulate Send Alert")

# ---------------- MAP ----------------

st.divider()
st.header("🗺️ NER Risk Map")

st.write(
    "This map displays sample monitoring locations. "
    "The selected location is shown with its current risk category."
)

map_object = folium.Map(
    location=[25.55, 91.80],
    zoom_start=9
)

for place, coordinates in locations.items():
    if place == selected_location:
        marker_color = map_color
        marker_radius = 18
        popup = f"{place}: {category} risk"
    else:
        marker_color = "blue"
        marker_radius = 8
        popup = f"{place}: Sample monitoring point"

    folium.CircleMarker(
        location=coordinates,
        radius=marker_radius,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.8,
        popup=popup
    ).add_to(map_object)

st_folium(map_object, width=1100, height=500)

st.caption(
    "Prototype only: map points and risk values are sample data, "
    "not official warning information."
)

st.divider()
st.caption(
    f"LandGuard NER prototype | Updated: "
    f"{datetime.now().strftime('%d %B %Y, %I:%M %p')}"
)
