import streamlit as st
import pandas as pd
import numpy as np

# Page Setup
st.set_page_config(
    page_title="Login / Register",
    page_icon="<3",
    layout="centered"
)

# Initialise session state
if "users" not in st.session_state:
    st.session_state.users = {}  # simple in-memory dictionary

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# Title
st.title("Heyyyy Welcome")

# If already logged in skip login
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()

#Tabs
tab_login, tab_register = st.tabs(["Login", "Register"])

#LOGIN TAB
with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        users = st.session_state.users

        if login_username in users and users[login_username] == login_password:
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success(f"Welcome back, {login_username}! 🎉")

            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("Invalid username or password.")


#REGISTER TAB
with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif new_username in st.session_state.users:
            st.error("Username already exists. Choose another one.")
        else:
            st.session_state.users[new_username] = new_password
            st.success("Account created! You can now log in from the Login tab.")
            st.info("Go to the Login tab to sign in.")

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