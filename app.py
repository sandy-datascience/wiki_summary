import streamlit as st
import requests

# Replace with your ACTUAL FastAPI Render URL
BACKEND_URL = "https://wiki-summary.onrender.com"  # ← CHANGE THIS

st.title("📚 Wikipedia Summarizer")

query = st.text_input("Enter a topic:")
sentences = st.slider("Number of sentences", 3, 20, 10)

if st.button("Get Summary") and query:
    try:
        response = requests.post(
            f"{BACKEND_URL}/summarize",
            params={"query": query, "sentences": sentences}
        )

        if response.status_code == 200:
            st.success("✅ Summary generated!")
            st.write(response.json()["summary"])
        else:
            st.error(f"❌ Error: {response.json()}")

    except Exception as e:
        st.error(f"❌ Connection error: {str(e)}")
