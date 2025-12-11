import streamlit as st
import pandas as pd
import altair as alt
import google.generativeai as genai
from pathlib import Path

st.set_page_config(page_title="Data Science Dashboard + AI", layout="wide")
st.title("Data Science Dashboard + AI Assistant")

# Authentication
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to proceed.")
    st.stop()

DATA_DIR = Path("data")
METADATA_CSV = DATA_DIR / "datasets_metadata.csv"

@st.cache_data
def load_metadata():
    return pd.read_csv(METADATA_CSV)

if not METADATA_CSV.exists():
    st.warning(f"Missing `{METADATA_CSV}` file.")
    st.stop()

metadata = load_metadata()

with st.sidebar:
    st.header("Dataset Options")
    dataset_name = st.selectbox("Choose dataset", metadata["name"].tolist())

selected = metadata[metadata["name"] == dataset_name]

st.subheader(f"Dataset: {dataset_name}")
st.dataframe(selected)

# charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Rows per Dataset")
    chart = alt.Chart(metadata).mark_bar().encode(x="name", y="rows")
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.subheader("Columns per Dataset")
    chart = alt.Chart(metadata).mark_bar().encode(x="name", y="columns")
    st.altair_chart(chart, use_container_width=True)

# AI Assistant
st.markdown("---")
st.subheader("Data Science AI Assistant")

try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Missing GEMINI_API_KEY in secrets.toml")
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
    st.error(f"Failed to fetch Gemini models: {e}")
    st.stop()

if not model_names:
    st.error("No valid Gemini models available.")
    st.stop()

with st.sidebar:
    st.header("AI Settings")
    model_name = st.selectbox("Gemini Model", model_names, index=0)
    temperature = st.slider("Temperature", 0.0, 2.0, 1.0, step=0.1)

# Load selected model
try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"Model load error: {e}")
    st.stop()

# Chat History
if "ds_ai_chat" not in st.session_state:
    st.session_state.ds_ai_chat = []

for msg in st.session_state.ds_ai_chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Ask the Data Science AI...")

if prompt:
    st.session_state.ds_ai_chat.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    dataset_preview = selected.to_string(index=False)

    full_prompt = f"""
You are an experienced data scientist. Provide clear, concise, technically accurate guidance.

DATASET PREVIEW:
{dataset_preview}

QUESTION:
{prompt}
"""

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                response = model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature
                    )
                )
                reply = response.text
            except Exception as e:
                reply = f"AI Error: {e}"

        st.markdown(reply)
        st.session_state.ds_ai_chat.append({"role": "assistant", "content": reply})
