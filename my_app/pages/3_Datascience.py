import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Data Science Dashboard", layout="wide")

# Auth check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access this dashboard.")
    st.stop()

st.title("Data Science Dashboard<3")
st.write("Analyze datasets, missing values, and distribution patterns.")

# Sidebar: choose dataset size
with st.sidebar:
    st.header("Dataset Options")
    rows = st.slider("Number of rows", 50, 1000, 300)

# Fake dataset (replace with CSV from SQLite later)
data = pd.DataFrame({
    "age": np.random.normal(35, 10, rows).astype(int),
    "salary": np.random.normal(60000, 15000, rows).astype(int),
    "missing": np.random.choice([0, None], rows, p=[0.7, 0.3])
})

col1, col2 = st.columns(2)

with col1:
    st.subheader("Age Distribution")
    chart = alt.Chart(data).mark_bar().encode(
    alt.X("age:Q", bin=True),
    alt.Y("count()")
)

st.altair_chart(chart, use_container_width=True)
with col2:
    st.subheader("Salary Distribution")
    st.line_chart(data["salary"])

st.subheader("Missing Data Summary")
missing_rate = data.isnull().mean() * 100
st.dataframe(missing_rate)

st.info("Recommendation: Fill or remove missing values in the 'missing' column to improve data quality.")