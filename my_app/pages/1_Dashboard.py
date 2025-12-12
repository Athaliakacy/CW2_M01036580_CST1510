import streamlit as st
import pandas as pd
import numpy as np

#Page Setup
st.set_page_config(
    page_title="Dashboard",
    page_icon=";)",
    layout="wide"
)

#Ensure session state exists
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: redirect if not logged in
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

#Dashboard
st.title(";) Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")

st.caption("This is demo content — replace this with your real dashboard.")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    n_points = st.slider("Number of data points", 10, 200, 50)

#Fake data
data = pd.DataFrame(
    np.random.randn(n_points, 3),
    columns=["A", "B", "C"]
)

# Layout 
col1, col2 = st.columns(2)

with col1:
    st.subheader("Line Chart")
    st.line_chart(data)

with col2:
    st.subheader("Bar Chart")
    st.bar_chart(data)

# Raw Data
with st.expander("Show Raw Data"):
    st.dataframe(data)

# Logout 
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Home.py")