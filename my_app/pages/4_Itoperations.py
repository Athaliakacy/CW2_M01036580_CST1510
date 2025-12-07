import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="IT Ops Dashboard", layout="wide")

# Auth check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access this dashboard.")
    st.stop()

st.title(" IT Operations Dashboard<3")
st.write("Track support tickets and identify workflow bottlenecks.")

# Sidebar
with st.sidebar:
    st.header("Ticket Config")
    n_tickets = st.slider("Number of tickets", 20, 200, 50)

# Fake ticket data (replace with real SQLite table later)
tickets = pd.DataFrame({
    "priority": np.random.choice(["Low", "Medium", "High"], n_tickets),
    "resolution_time": np.random.randint(10, 120, n_tickets),
})

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ticket Priorities")
    st.bar_chart(tickets["priority"].value_counts())

with col2:
    st.subheader("Resolution Time Distribution")
    st.line_chart(tickets["resolution_time"])

with st.expander("Show Ticket Table"):
    st.dataframe(tickets)

# Insight
avg_resolution = tickets["resolution_time"].mean()
st.info(f"Average resolution time: **{avg_resolution:.1f} mins**. Consider adding more staff during peak periods.")