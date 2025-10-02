import streamlit as st
import requests

# Use localhost for local development
BACKEND_URL = "http://localhost:8000"

st.title("📚 Wikipedia Summarizer")

query = st.text_input("Enter a topic:")
sentences = st.slider("Number of sentences", 3, 20, 10)

if st.button("Get Summary") and query:
    try:
        response = requests.post(
            f"{BACKEND_URL}/summarize",
            params={"query": query, "sentences": sentences},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            st.success("✅ Summary generated!")
            st.write(data["summary"])
        else:
            st.error(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        st.error(f"❌ Connection error: {str(e)}")