import os 
import openai
import dotenv
import requests

dotenv.load_dotenv()
api_key = os.getenv("PERPLEXITY_API_KEY")

# API endpoint
url = "https://api.perplexity.ai/chat/completions"

with open("code.py", "r") as file:
    code = file.read()
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
responses = {
    "model": "sonar-pro",
    "messages": [
        {"role": "system", "content": "You are a code review assistant. You are given a code and you need to review it and give feedback on it."},
        {"role": "user", "content": f"Review the following code: {code}"}
    ],
    "temperature": 0.5,
    "max_tokens": 1024
}

response = requests.post(url, json=responses, headers=headers)
result = response.json()
print(result)
print(result['choices'][0]['message']['content'])

