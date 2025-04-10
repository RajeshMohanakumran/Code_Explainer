import os
from dotenv import load_dotenv
import requests
import streamlit as st

# Load environment variables
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def query_model(input_text):
    prompt = (
        "Explain this code line-by-line in simple terms:\n\n"
        f"### Code:\n{input_text}\n\n"
        "### Line-by-Line Explanation:\n"
        "1. "  # This helps start the numbered list format
    )
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 300, "temperature": 0.3, "top_p": 0.9},
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
    return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.set_page_config(page_title="Code Explanation Assistant", layout="wide")
st.title("Code Explanation Assistant")
code_snippet = st.text_area("Paste your code snippet here:", height=200)

if st.button("Generate Explanation"):
    if code_snippet:
        with st.spinner("Generating explanation..."):
            explanation = query_model(code_snippet)
        st.subheader("Explanation:")
        st.write(explanation)
    else:
        st.warning("⚠️ Please provide a code snippet.")