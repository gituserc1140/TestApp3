import streamlit as st
import requests
import os
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
COHERE_API_KEY = st.secrets.get("COHERE_API_KEY", os.getenv("COHERE_API_KEY"))
COHERE_API_URL = os.getenv("COHERE_API_URL", "https://api.cohere.ai/generate")
COHERE_MODEL = os.getenv("COHERE_MODEL", "command-xlarge-nightly")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", 10))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 500))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))

# Validate required environment variables
if not COHERE_API_KEY or not COHERE_API_URL:
    st.error("Required environment variables (COHERE_API_KEY, COHERE_API_URL) are not set.")
    st.stop()

def fetch_blog_content(prompt, max_retries=3, backoff_factor=1):
    """
    Fetches blog content from the Cohere API based on the provided prompt.

    Args:
        prompt (str): The topic or prompt for generating the blog content.

    Returns:
        str: The generated blog content or an error message if the request fails.
    """
    url = COHERE_API_URL
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": COHERE_MODEL,
        "prompt": prompt,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
    }
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=API_TIMEOUT)
            response.raise_for_status()
            response_data = response.json()
            if "generations" in response_data and response_data["generations"]:
                return response_data["generations"][0]["text"]
            else:
                logging.error("Invalid API response structure.")
                return "Failed to fetch content. Please try again later."
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                logging.warning(f"API request failed (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {backoff_factor * (2 ** attempt)} seconds.")
                time.sleep(backoff_factor * (2 ** attempt))
            else:
                logging.error(f"API request failed after {max_retries} attempts: {e}")
                return "Failed to fetch content. Please try again later."
        except ValueError as e:
            logging.error(f"Failed to parse API response as JSON: {e}")
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