import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")

# Authentication check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access this dashboard.")
    st.stop()

st.title(" Cybersecurity Dashboard<3")
st.write("Monitor phishing attacks, incident volume, and workflow problems.")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    days = st.slider("Days to simulate", 7, 90, 30)

# Fake incident data (replace with SQLite data later)
np.random.seed(1)
incidents = pd.DataFrame({
    "day": range(days),
    "phishing": np.random.randint(1, 20, days),
    "malware": np.random.randint(0, 10, days),
    "ddos": np.random.randint(0, 5, days)
})

col1, col2 = st.columns(2)

with col1:
    st.subheader("Phishing Trend")
    st.line_chart(incidents["phishing"])

with col2:
    st.subheader("Malware Detected")
    st.bar_chart(incidents["malware"])

with st.expander("Show Raw Incident Data"):
    st.dataframe(incidents)

# Key Insight
st.info(f"High phishing spikes detected on day {incidents['phishing'].idxmax()} — investigate user awareness or email filtering.")