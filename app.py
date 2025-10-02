import streamlit as st
import requests
import os

# Get backend URL from environment or use local for development
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')

st.title("📚 Wikipedia Summarizer")

query = st.text_input("Enter a topic:")
sentences = st.slider("Number of sentences", 3, 20, 10)

if st.button("Get Summary"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/summarize",
            params={"query": query, "sentences": sentences}
        )

        if response.status_code == 200:
            st.success("✅ Summary generated!")
            st.write(response.json()["summary"])
        else:
            st.error("❌ Error generating summary")

    except Exception as e:
        st.error(f"❌ Connection error: {str(e)}")
