import streamlit as st
import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_API_URL = os.getenv("COHERE_API_URL", "https://api.cohere.ai/generate")
COHERE_MODEL = os.getenv("COHERE_MODEL", "command-xlarge-nightly")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", 10))

def fetch_blog_content(prompt):
    """
    Fetches blog content from the Cohere API based on the provided prompt.

    Args:
        prompt (str): The topic or prompt for generating the blog content.

    Returns:
        str: The generated blog content or an error message if the request fails.
    """
    if not COHERE_API_KEY:
        st.error("COHERE_API_KEY environment variable is not set.")
        st.stop()

    url = COHERE_API_URL
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": COHERE_MODEL,
        "prompt": prompt,
        "max_tokens": 500,
        "temperature": 0.7,
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()["generations"][0]["text"]
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return "Failed to fetch content. Please try again later."

# Streamlit app
logging.info("Streamlit app started.")
st.title("Cohere Powered Blog")

# Input for blog topic
topic = st.text_input("Enter a topic for the blog:")

if st.button("Generate Blog"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    elif len(topic.strip()) < 5:
        st.warning("Topic must be at least 5 characters long.")
    else:
        logging.info(f"User entered topic: {topic}")
        with st.spinner("Generating blog..."):
            prompt = f"Write a blog post about {topic}."
            blog_content = fetch_blog_content(prompt)
            st.subheader("Generated Blog")
            st.write(blog_content)