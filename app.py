import streamlit as st
import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_blog_content(prompt):
    """
    Fetches blog content from the Cohere API based on the provided prompt.

    Args:
        prompt (str): The topic or prompt for generating the blog content.

    Returns:
        str: The generated blog content or an error message if the request fails.
    """
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set.")

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
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return response.json()["generations"][0]["text"]
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return "Failed to fetch content. Please try again later."

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