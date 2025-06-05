import os 
import dotenv
import requests
import json

# Load API key from .env file
dotenv.load_dotenv()
api_key = os.getenv("PERPLEXITY_API_KEY")

# API endpoint
url = "https://api.perplexity.ai/chat/completions"

"""Ian: Hi grandma, how are you?
Grandma: I'm fine, thank you. How are you?
Ian: I'm good, thank you. Give me a suggestion on what to do for lunch?
Grandma: I suggest you to have a salad for lunch.
Ian: That's a good idea. Thank you grandma.
"""

# Initialize conversation history
messages = [{"role": "system", "content": "You are a sweet and helpful grandma"}]

while True:
# adding user input question:
    user_input = input("Nikki: ")
    messages.append({"role": "user", "content": user_input})
    response = {
    "model": "sonar-pro",
    "messages": messages,
    "temperature": 0.5,
    "max_tokens": 1024
}

    # Headers with API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Make the request
    response = requests.post(url, json=response, headers=headers)
    grandma_response = response.json()
    print(f"\nGranny: {grandma_response['choices'][0]['message']['content']} \n")
    # Add grandma's response to the conversation history
    messages.append({"role": "assistant", "content": grandma_response['choices'][0]['message']['content']})
