import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit configuration
st.set_page_config(page_title="AI Code Helper", page_icon="🤖", layout="wide")

st.title("🤖 AI Code Helper")
st.write("Your smart AI assistant for generating, explaining, and debugging code!")

# Tabs for different features
tab1, tab2 = st.tabs(["🧩 Generate Code", "🔍 Explain / Debug Code"])

# ---------------- TAB 1: Code Generation ----------------
with tab1:
    st.subheader("🧩 Generate Code")
    prompt = st.text_area("Describe what code you want to generate:")

    language = st.selectbox(
        "Select programming language:",
        ["Python", "JavaScript", "C++", "Java", "HTML", "Other"],
        key="lang_generate"
    )

    if st.button("🚀 Generate Code"):
        if not prompt.strip():
            st.warning("Please enter a description for the code.")
        else:
            with st.spinner("💡 Thinking..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": f"You are an expert {language} programmer."},
                        {"role": "user", "content": f"Write {language} code for: {prompt}"}
                    ]
                )
                code_output = response.choices[0].message.content
                st.code(code_output, language=language.lower())
                st.success("✅ Code generated successfully!")

# ---------------- TAB 2: Explain or Debug ----------------
with tab2:
    st.subheader("🔍 Explain or Debug Code")
    code_input = st.text_area("Paste your code here for explanation or debugging:")
    action = st.radio("Choose what you want to do:", ["Explain", "Debug"], key="action")

    if st.button("🧠 Process Code"):
        if not code_input.strip():
            st.warning("Please paste your code first.")
        else:
            with st.spinner("🧩 Analyzing your code..."):
                if action == "Explain":
                    user_request = f"Explain the following code step-by-step:\n{code_input}"
                else:
                    user_request = f"Debug the following code and explain the issues:\n{code_input}"

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a senior developer who explains clearly."},
                        {"role": "user", "content": user_request}
                    ]
                )

                explanation = response.choices[0].message.content
                st.write(explanation)
                st.success("✅ Done!")
