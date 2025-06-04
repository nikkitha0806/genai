import os 
import dotenv
import requests
import json

# Load API key from .env file
dotenv.load_dotenv()
api_key = os.getenv("PERPLEXITY_API_KEY")

# API endpoint
url = "https://api.perplexity.ai/chat/completions"

# adding user input question:
user_input = input("What Can I do for you?")

# Simple request
payload = {
    "model": "sonar-pro",
    "messages": [
        {"role": "system", "content": "You are a sweet and helpful assistant."},
        {"role": "user", "content": user_input}
    ],
    "temperature": 0.5,
    "max_tokens": 1024
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
    print(result['choices'][0]['message']['content'])
   # print("\nAPI Response:")
   # print(json.dumps(result, indent=2))
except:
    print("\nRaw Response:")
    print(response.text)