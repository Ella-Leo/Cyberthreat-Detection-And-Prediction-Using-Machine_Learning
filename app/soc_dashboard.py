
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# PAGE CONFIG
st.set_page_config(
    page_title="SOC Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# DARK CYBER THEME
st.markdown("""
<style>
body {
    background-color: #0A192F;
    color: white;
}
[data-testid="stAppViewContainer"] {
    background-color: #0A192F;
}
[data-testid="stSidebar"] {
    background-color: #112240;
}
.metric-box {
    background-color: #112240;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# SAMPLE DATA (replace with real model output later)
np.random.seed(42)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
threats = [120, 145, 180, 220, 260, 310]

attack_types = ["DDoS", "Malware", "Phishing", "SQL Injection", "Brute Force", "Insider Threat"]
attack_counts = [350, 280, 190, 150, 125, 70]

severity_labels = ["Critical", "High", "Medium", "Low"]
severity_counts = [120, 450, 890, 1350]

# HEADER
st.title("🛡 SOC Cybersecurity Dashboard")
st.markdown("Real-time Threat Monitoring & AI Detection System")

# METRICS ROW
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Threats", "12,543", "+5%")
col2.metric("Active Threats", "243", "-2%")
col3.metric("Critical Alerts", "120", "+8%")
col4.metric("Model Accuracy", "98.5%", "+0.3%")

st.divider()

# THREAT TIMELINE
st.subheader("📈 Threat Timeline")

fig1 = px.line(
    x=months,
    y=threats,
    markers=True,
    labels={"x": "Month", "y": "Threats"},
    title="Threat Activity Over Time"
)
st.plotly_chart(fig1, use_container_width=True)

# SEVERITY DISTRIBUTION
st.subheader("⚠ Threat Severity Distribution")

fig2 = px.pie(
    names=severity_labels,
    values=severity_counts,
    title="Threat Severity Breakdown"
)
st.plotly_chart(fig2, use_container_width=True)

# RECENT ALERTS
st.subheader("🚨 Recent Alerts")

alerts = pd.DataFrame({
    "Time": ["10:23", "10:18", "09:55", "09:40", "09:12"],
    "Alert": [
        "Brute Force Detected",
        "DDoS Attack Attempt",
        "Malware Activity",
        "Suspicious Login",
        "SQL Injection Attempt"
    ]
})

st.dataframe(alerts, use_container_width=True)

# THREAT DISTRIBUTION
st.subheader("📊 Threat Distribution by Type")

fig3 = px.bar(
    x=attack_types,
    y=attack_counts,
    labels={"x": "Attack Type", "y": "Count"},
    title="Detected Cyber Threat Types"
)
st.plotly_chart(fig3, use_container_width=True)

# MODEL PERFORMANCE
st.subheader("🤖 Model Comparison")

models = ["Logistic Regression", "Decision Tree", "Random Forest", "SVM", "XGBoost"]
accuracy = [92, 94, 98, 96, 99]

fig4 = px.bar(
    x=models,
    y=accuracy,
    labels={"x": "Model", "y": "Accuracy (%)"},
    title="ML Model Performance Comparison"
)
st.plotly_chart(fig4, use_container_width=True)

# CONFUSION MATRIX
st.subheader("🧠 Confusion Matrix")

cm = np.array([[950, 50],
               [30, 970]])

fig5 = go.Figure(data=go.Heatmap(
    z=cm,
    x=["Predicted Normal", "Predicted Attack"],
    y=["Actual Normal", "Actual Attack"],
    colorscale="Reds"
))

fig5.update_layout(title="Confusion Matrix")
st.plotly_chart(fig5, use_container_width=True)

# FOOTER
st.markdown("---")
st.markdown("🔐 SOC Dashboard | Cybersecurity AI System | Module 10")
