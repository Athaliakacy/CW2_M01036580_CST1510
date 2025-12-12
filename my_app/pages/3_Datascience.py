import streamlit as st
import pandas as pd
import altair as alt
import google.generativeai as genai
from pathlib import Path

# PAGE SETUP
st.set_page_config(page_title="Data Science Dashboard + AI", layout="wide")
st.title(" Data Science Dashboard + AI Assistant")

# AUTH CHECK
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to proceed.")
    st.stop()

# LOAD METADATA CSV
DATA_DIR = Path("data")
METADATA_CSV = DATA_DIR / "datasets_metadata.csv"

if not METADATA_CSV.exists():
    st.error(" datasets_metadata.csv not found in /data folder")
    st.stop()

@st.cache_data
def load_metadata():
    """Load metadata reliably (tab-separated)."""
    try:
        return pd.read_csv(
            METADATA_CSV,
            sep="\t",
            header=0,
            names=["dataset_id", "name", "rows", "columns", "uploaded_by", "upload_date"]
        )
    except Exception:
        return pd.read_csv(
            METADATA_CSV,
            engine="python",
            sep=None,
            encoding="utf-16",
            on_bad_lines="skip"
        )

metadata = load_metadata()

st.subheader(" Loaded Dataset Metadata")
st.dataframe(metadata, use_container_width=True)


with st.sidebar:
    st.header("Dataset Options")
    dataset_name = st.selectbox("Choose dataset", metadata["name"].tolist())

selected = metadata[metadata["name"] == dataset_name]

st.subheader(f"Dataset Selected: {dataset_name}")
st.dataframe(selected, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Rows per Dataset")
    chart = alt.Chart(metadata).mark_bar().encode(
        x=alt.X("name", sort=None),
        y="rows"
    )
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.subheader(" Columns per Dataset")
    chart = alt.Chart(metadata).mark_bar().encode(
        x=alt.X("name", sort=None),
        y="columns"
    )
    st.altair_chart(chart, use_container_width=True)


st.markdown("---")
st.subheader(" Data Science AI Assistant")

# Load API key
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=gemini_api_key)
except:
    st.error(" Missing GEMINI_API_KEY in secrets.toml")
    st.stop()

# Load Gemini models
try:
    models = genai.list_models()
    model_names = [
        m.name for m in models
        if "generateContent" in getattr(m, "supported_generation_methods", [])
    ]
except Exception as e:
    st.error(f"Gemini API Error: {e}")
    st.stop()

if not model_names:
    st.error(" No valid Gemini models available.")
    st.stop()

with st.sidebar:
    st.header("AI Settings")
    model_name = st.selectbox("Gemini Model", model_names)
    temperature = st.slider("Temperature", 0.0, 2.0, 1.0)

# Load model
try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f" Error loading Gemini model: {e}")
    st.stop()


if "ds_ai_chat" not in st.session_state:
    st.session_state.ds_ai_chat = []

# Display previous messages
for msg in st.session_state.ds_ai_chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Ask the Data Science AI...")

if prompt:
    # Add user message
    st.session_state.ds_ai_chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    dataset_preview = selected.to_string(index=False)

    full_prompt = f"""
You are a highly skilled data scientist. Provide clear, accurate insights.

DATASET PREVIEW:
{dataset_preview}

QUESTION:
{prompt}
"""

    # Generate AI response
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
                reply = f" AI Error: {e}"

        st.markdown(reply)
        st.session_state.ds_ai_chat.append({"role": "assistant", "content": reply})
