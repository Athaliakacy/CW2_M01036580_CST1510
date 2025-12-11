import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai

st.set_page_config(page_title="IT Ops Dashboard + AI", layout="wide")

# AUTH CHECK
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access this dashboard.")
    st.stop()

st.title("IT Operations Dashboard")
st.write("Track support tickets, bottlenecks, and ask the AI assistant for insights.")

with st.sidebar:
    st.header("Dashboard Settings")
    n_tickets = st.slider("Number of tickets", 20, 200, 50)

tickets = pd.DataFrame({
    "priority": np.random.choice(["Low", "Medium", "High"], n_tickets),
    "resolution_time": np.random.randint(10, 120, n_tickets),
})

# CHARTS 
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ticket Priorities")

    priority_counts = (
        tickets["priority"]
        .value_counts()
        .reset_index()
    )
    priority_counts.columns = ["priority", "count"]
    priority_counts = priority_counts.set_index("priority")

    st.bar_chart(priority_counts)

with col2:
    st.subheader("Resolution Time Distribution")
    st.line_chart(tickets["resolution_time"])

with st.expander("Show Ticket Table"):
    st.dataframe(tickets)

avg_resolution = tickets["resolution_time"].mean()
st.info(f"Average resolution time: {avg_resolution:.1f} mins.")

# AI ASSISTANT SECTION 

st.header("IT Operations AI Assistant — Powered by Gemini")

# CHECK GEMINI API KEY
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("GEMINI_API_KEY missing in secrets.toml.")
    st.stop()

genai.configure(api_key=gemini_api_key)

try:
    available_models = genai.list_models()
    model_names = [
        m.name
        for m in available_models
        if "generateContent" in getattr(m, "supported_generation_methods", [])
    ]
except Exception as e:
    st.error(f"Failed to fetch available models: {e}")
    st.stop()

if not model_names:
    st.error("No Gemini models support text generation.")
    st.stop()

IT_OPS_PROMPT = """You are an IT operations expert assistant.
Troubleshoot infrastructure issues, interpret logs, analyse ticket patterns,
identify workflow bottlenecks, and recommend operational improvements."""

# CHAT HISTORY 
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("AI Assistant Settings")
    model_name = st.selectbox("Gemini Model", model_names)
    temperature = st.slider("Temperature", 0.0, 2.0, 1.0)

    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

# LOAD SELECTED MODEL 
try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"Failed to load Gemini model '{model_name}': {e}")
    st.stop()

# DISPLAY CHAT HISTORY 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#  USER INPUT 
prompt = st.chat_input("Ask something about IT operations...")

if prompt:
    # Save + display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build final prompt
    full_prompt = f"""
SYSTEM ROLE:
{IT_OPS_PROMPT}

USER:
{prompt}

Extra IT Data:
Average Resolution Time: {avg_resolution:.1f} mins
Ticket Distribution: {priority_counts.to_dict()['count']}
"""

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature
                    )
                )
                reply = response.text
            except Exception as e:
                reply = f"Error generating response: {e}"

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
