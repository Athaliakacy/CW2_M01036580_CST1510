import streamlit as st
import os
api_key = os.getenv("GEMINI_API_KEY")


# --- Debug message to ensure app loads ---
st.write(" App Loaded Successfully")

# --- Check Gemini API Key ---
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error(" GEMINI_API_KEY is missing! Add it to Streamlit secrets.toml.")
    st.stop()  # Stop execution if key is missing

# --- Import Gemini safely ---
try:
    import google.generativeai as genai
except Exception as e:
    st.error(f" Failed to import Gemini SDK: {e}")
    st.stop()

# --- Configure Gemini ---
try:
    genai.configure(api_key=gemini_api_key)
    st.write(" Gemini API configured")
except Exception as e:
    st.error(f" Failed to configure Gemini: {e}")
    st.stop()

# --- Gemini Model Options ---
MODEL_OPTIONS = {
    "Gemini 1.5 Flash": "gemini-1.5-flash",
    "Gemini 1.5 Pro": "gemini-1.5-pro"
}

# --- Domain Prompts ---
DOMAIN_PROMPTS = {
    "Cybersecurity": """You are a cybersecurity expert assistant.
Analyze threats, logs, vulnerabilities, and provide technical cyber guidance.""",
    "Data Science": """You are a data science expert assistant.
Help with machine learning, statistics, data cleaning, and visualization.""",
    "IT Operations": """You are an IT operations expert assistant.
Troubleshoot infrastructure issues, optimize systems, and manage tickets."""
}

# --- Streamlit Page Settings ---
st.set_page_config(page_title="Multi-Domain AI (Gemini)", page_icon=":)", layout="wide")
st.title("Multi-Domain AI Assistant — Powered by Gemini")
st.caption("Choose your domain: Cybersecurity, Data Science, or IT Operations")

# --- Session State for Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar Controls ---
with st.sidebar:
    st.subheader("Chat Settings")

    domain = st.selectbox("Choose Domain", ["Cybersecurity", "Data Science", "IT Operations"])

    model_choice = st.selectbox("Gemini Model", list(MODEL_OPTIONS.keys()), index=0)
    model_name = MODEL_OPTIONS[model_choice]

    temperature = st.slider("Temperature", 0.0, 2.0, 1.0, 0.1)

    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

# --- Load Gemini Model ---
try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f" Failed to load Gemini model '{model_name}': {e}")
    st.stop()

# --- Display Conversation ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Input ---
prompt = st.chat_input("Type your message...")

if prompt:
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build Gemini Input
    system_prompt = DOMAIN_PROMPTS[domain]
    full_prompt = f"""
SYSTEM ROLE:
{system_prompt}

USER:
{prompt}
"""

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
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