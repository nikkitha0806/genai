import os 
import dotenv
import requests
import json

# Load API key from .env file
dotenv.load_dotenv()
api_key = os.getenv("PERPLEXITY_API_KEY")

# API endpoint
url = "https://api.perplexity.ai/chat/completions"

# Simple request
payload = {
    "model": "sonar-pro",
    "messages": [
        {"role": "user", "content": "How many stars are there in our galaxy?"}
    ]
}

# Headers with API key
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Make the request
response = requests.post(url, json=payload, headers=headers)

# Print the response in a formatted way
try:
    result = response.json()
    print("\nAPI Response:")
    print(json.dumps(result, indent=2))
except:
    print("\nRaw Response:")
    print(response.text)