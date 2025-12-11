import streamlit as st
import google.generativeai as genai

# Streamlit Page Settings
st.set_page_config(page_title="Multi-Domain AI (Gemini)", page_icon=":)", layout="wide")
st.title("Multi-Domain AI Assistant — Powered by Gemini")
st.caption("Choose your domain: Cybersecurity, Data Science, or IT Operations")

#Check GEMINI_API_KEY
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("GEMINI_API_KEY is missing! Add it to Streamlit secrets.toml.")
    st.stop()

genai.configure(api_key=gemini_api_key)

# Fetch available models safely
try:
    available_models = genai.list_models()
    # Only include models that support text generation
    model_names = [
        m.name
        for m in available_models
        if "generateContent" in getattr(m, "supported_generation_methods", [])
    ]
except Exception as e:
    st.error(f"Failed to fetch available models: {e}")
    st.stop()

if not model_names:
    st.error("No valid Gemini models available for text generation.")
    st.stop()


DOMAIN_PROMPTS = {
    "Cybersecurity": """You are a cybersecurity expert assistant.
Analyze threats, logs, vulnerabilities, and provide technical cyber guidance.""",
    "Data Science": """You are a data science expert assistant.
Help with machine learning, statistics, data cleaning, and visualization.""",
    "IT Operations": """You are an IT operations expert assistant.
Troubleshoot infrastructure issues, optimize systems, and manage tickets."""
}

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Chat Settings")
    domain = st.selectbox("Choose Domain", list(DOMAIN_PROMPTS.keys()))
    model_name = st.selectbox("Gemini Model", model_names, index=0)
    temperature = st.slider("Temperature", 0.0, 2.0, 1.0, 0.1)
    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

#Load Selected Gemini Model
try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"Failed to load Gemini model '{model_name}': {e}")
    st.stop()

#Display Conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#  Chat Input 
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
                reply = f"Error generating response: {e}"

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
