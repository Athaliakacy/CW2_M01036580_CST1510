import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai


#  PAGE SETTINGS
st.set_page_config(page_title="Cybersecurity Dashboard + AI", layout="wide")
st.title("Cybersecurity Dashboard + Gemini AI Assistant")
st.caption("Monitor incidents and chat with an AI cybersecurity expert.")


# AUTH CHECK
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access this dashboard.")
    st.stop()


# CHECK GEMINI API KEY
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error(" GEMINI_API_KEY missing in secrets.toml!")
    st.stop()

genai.configure(api_key=gemini_api_key)


# FETCH GEMINI MODELS
try:
    available_models = genai.list_models()
    model_names = [
        m.name for m in available_models
        if "generateContent" in getattr(m, "supported_generation_methods", [])
    ]
except Exception as e:
    st.error(f"Failed to fetch available models: {e}")
    st.stop()

if not model_names:
    st.error("No valid Gemini models found that support text generation.")
    st.stop()


# CYBERSECURITY SYSTEM PROMPT
CYBER_PROMPT = """
You are a professional Cybersecurity Analyst AI.
Your job is to analyze logs, detect threats, provide incident insights,
improve SOC workflows, and generate security recommendations.
"""


# SIDEBAR SETTINGS
with st.sidebar:
    st.header("Settings")

    model_name = st.selectbox("Choose Gemini Model", model_names, index=0)
    temperature = st.slider("Temperature", 0.0, 2.0, 1.0, 0.1)

    days = st.slider("Days to simulate incidents", 7, 90, 30)

    if st.button("Reset AI Chat"):
        st.session_state.messages = []
        st.experimental_rerun()


# LOAD MODEL
try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"Failed to load model {model_name}: {e}")
    st.stop()


# LOAD REAL INCIDENT DATA
df = pd.read_csv("data/cyber_incidents.csv", sep="\t")  
st.write("Columns in CSV:", df.columns.tolist())  


incidents = pd.DataFrame({
    "day": range(len(df)),
    "phishing": (df["category"] == "Phishing").astype(int),
    "malware": (df["category"] == "Malware").astype(int),
    "ddos": (df["category"] == "DDoS").astype(int)
})


# DASHBOARD LAYOUT
col1, col2 = st.columns(2)

with col1:
    st.subheader(" Phishing Trend")
    st.line_chart(incidents[["phishing"]])

with col2:
    st.subheader(" Malware Detections")
    st.bar_chart(incidents[["malware"]])


with st.expander(" Show Raw Incident Data"):
    st.dataframe(incidents)


# Display quick insight
st.info(
    f"Highest phishing spike occurs on day {incidents['phishing'].idxmax()}. "
    f"Recommend reviewing email filtering & user awareness training."
)



# GEMINI AI CHAT SECTION
st.markdown("---")
st.header(" Cybersecurity AI Assistant")

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Chat input
prompt = st.chat_input("Ask the AI about incidents, threats, logs, or best practices...")

if prompt:
    # Add user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build full system prompt
    full_prompt = f"""
SYSTEM ROLE:
{CYBER_PROMPT}

SECURITY INCIDENT SUMMARY (REAL DATA):

Total phishing incidents: {incidents['phishing'].sum()}
Total malware incidents: {incidents['malware'].sum()}
Total DDoS incidents: {incidents['ddos'].sum()}

Recent Real Incidents:
{df.tail(5).to_string(index=False)}

USER QUESTION:
{prompt}
"""

    # Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("AI analyzing threats…"):
            try:
                response = model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(temperature=temperature)
                )
                reply = response.text
            except Exception as e:
                reply = f" Error generating response: {e}"

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
