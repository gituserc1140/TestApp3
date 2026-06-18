# TestApp3

A Streamlit app powered by Cohere API to generate blog posts.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/gituserc1140/TestApp3.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set the required environment variables:
   ```bash
   export COHERE_API_KEY="your_api_key_here"
   ```
   Optional environment variables:
   ```bash
   export COHERE_API_URL="https://api.cohere.ai/generate"
   export COHERE_MODEL="command-xlarge-nightly"
   export API_TIMEOUT=10
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage
Enter a topic in the input field and click "Generate Blog" to create a blog post.

### Environment Variables
- `COHERE_API_KEY`: Your Cohere API key (required).
- `COHERE_API_URL`: Cohere API endpoint (default: `https://api.cohere.ai/generate`).
- `COHERE_MODEL`: Model to use (default: `command-xlarge-nightly`).
- `API_TIMEOUT`: API request timeout in seconds (default: `10`).