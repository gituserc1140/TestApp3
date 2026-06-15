import streamlit as st
import requests
import os

# Function to fetch blog content using Cohere API
def fetch_blog_content(prompt):
    cohere_api_key = st.secrets["cohere_api_key"]
    url = "https://api.cohere.ai/generate"
    headers = {
        "Authorization": f"Bearer {cohere_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "command-xlarge-nightly",
        "prompt": prompt,
        "max_tokens": 500,
        "temperature": 0.7,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["generations"][0]["text"]
    else:
        return "Failed to fetch content."

# Streamlit app
st.title("Cohere Powered Blog")

# Input for blog topic
topic = st.text_input("Enter a topic for the blog:")

if st.button("Generate Blog"):
    if topic:
        with st.spinner("Generating blog..."):
            prompt = f"Write a blog post about {topic}."
            blog_content = fetch_blog_content(prompt)
            st.subheader("Generated Blog")
            st.write(blog_content)
    else:
        st.warning("Please enter a topic.")
