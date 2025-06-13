import os 
import dotenv
import json 
import requests
from datetime import datetime
import yfinance as yf

# Load environment variables
dotenv.load_dotenv()
api_key = os.getenv("PERPLEXITY_API_KEY")

if not api_key:
    print("Error: PERPLEXITY_API_KEY not found in environment variables")
    print("Please add your API key to the .env file")
    exit(1)

# API endpoint
url = "https://api.perplexity.ai/chat/completions"

# Function implementations
def get_weather_data(location):
    """Get weather data for a location using OpenWeatherMap API"""
    try:
        # In a real implementation, you would use an actual weather API
        # This is a mock implementation
        weather_data = {
            "location": location,
            "temperature": "72°F",
            "conditions": "Partly Cloudy",
            "humidity": "65%",
            "wind": "8 mph",
            "forecast": "Clear skies expected for the next 3 days"
        }
        return weather_data
    except Exception as e:
        return {"error": f"Failed to get weather data: {str(e)}"}

def get_stock_data(ticker):
    """Get stock data using yfinance"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        
        stock_data = {
            "ticker": ticker,
            "current_price": f"${current_price:.2f}",
            "company_name": info.get('longName', 'N/A'),
            "market_cap": f"${info.get('marketCap', 0):,.2f}",
            "pe_ratio": info.get('trailingPE', 'N/A'),
            "dividend_yield": f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else 'N/A'
        }
        return stock_data
    except Exception as e:
        return {"error": f"Failed to get stock data: {str(e)}"}

def get_news_data(topic, count=5):
    """Get news data for a topic"""
    try:
        # In a real implementation, you would use a news API
        # This is a mock implementation
        news_data = {
            "topic": topic,
            "articles": [
                {
                    "title": f"Latest news about {topic}",
                    "source": "News Source",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "summary": f"This is a sample news article about {topic}"
                } for _ in range(count)
            ]
        }
        return news_data
    except Exception as e:
        return {"error": f"Failed to get news data: {str(e)}"}

def get_company_data(company_name):
    """Get company information"""
    try:
        # In a real implementation, you would use a company information API
        # This is a mock implementation
        company_data = {
            "name": company_name,
            "industry": "Technology",
            "founded": "2000",
            "headquarters": "San Francisco, CA",
            "description": f"{company_name} is a leading technology company.",
            "key_products": ["Product 1", "Product 2", "Product 3"]
        }
        return company_data
    except Exception as e:
        return {"error": f"Failed to get company data: {str(e)}"}

# Define the functions that can be called
functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather and forecast for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state/country, e.g. San Francisco, CA or London, UK"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "get_stock_price",
        "description": "Get the current stock price and information for a ticker symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol, e.g. AAPL"
                }
            },
            "required": ["ticker"]
        }
    },
    {
        "name": "get_news",
        "description": "Get the latest news for a specific topic or company",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic or company name to search news for"
                },
                "count": {
                    "type": "integer",
                    "description": "Number of news articles to return (default: 5)",
                    "default": 5
                }
            },
            "required": ["topic"]
        }
    },
    {
        "name": "get_company_info",
        "description": "Get detailed information about a company",
        "parameters": {
            "type": "object",
            "properties": {
                "company_name": {
                    "type": "string",
                    "description": "The name of the company to get information about"
                }
            },
            "required": ["company_name"]
        }
    }
]

def get_user_query():
    print("\nAvailable Functions:")
    print("1. Get Weather")
    print("2. Get Stock Price")
    print("3. Get News")
    print("4. Get Company Information")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == "1":
        location = input("Enter location (e.g., New York, NY): ")
        return f"What's the weather like in {location}?"
    elif choice == "2":
        ticker = input("Enter stock ticker symbol (e.g., AAPL): ").upper()
        return f"What is the current price and information for {ticker} stock?"
    elif choice == "3":
        topic = input("Enter topic or company name for news: ")
        count = input("Enter number of news articles (default: 5): ")
        count = int(count) if count.isdigit() else 5
        return f"Get me {count} latest news articles about {topic}"
    elif choice == "4":
        company = input("Enter company name: ")
        return f"Tell me about {company} company"
    elif choice == "5":
        return "exit"
    else:
        print("Invalid choice. Please try again.")
        return get_user_query()

def process_query(user_query):
    if user_query == "exit":
        return False
        
    # Example conversation with function calling
    messages = [
        {
            "role": "system",
            "content": """You are a helpful assistant that can provide information about weather, stocks, news, and companies. 
            Use the appropriate function based on the user's query. For weather queries, use get_weather. 
            For stock queries, use get_stock_price. For news queries, use get_news. 
            For company information, use get_company_info."""
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    # Prepare the request payload
    payload = {
        "model": "sonar-pro",
        "messages": messages,
        "functions": functions,
        "temperature": 0.7,
        "max_tokens": 1024
    }

    # Headers with API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Make the request
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        # Process the response
        result = response.json()
        
        print("\nAPI Response:")
        print("=" * 50)
        
        # Check if the model wants to call a function
        if 'choices' in result and len(result['choices']) > 0:
            message = result['choices'][0]['message']
            if 'function_call' in message:
                function_call = message['function_call']
                print("\nFunction Call Requested:")
                print("-" * 30)
                print(f"Function: {function_call['name']}")
                arguments = json.loads(function_call['arguments'])
                print(f"Arguments: {json.dumps(arguments, indent=2)}")
                
                # Execute the appropriate function
                function_name = function_call['name']
                if function_name == 'get_weather':
                    result = get_weather_data(arguments['location'])
                elif function_name == 'get_stock_price':
                    result = get_stock_data(arguments['ticker'])
                elif function_name == 'get_news':
                    result = get_news_data(arguments['topic'], arguments.get('count', 5))
                elif function_name == 'get_company_info':
                    result = get_company_data(arguments['company_name'])
                
                # Add the function result to the conversation
                messages.append(message)
                messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": json.dumps(result)
                })
                
                # Make another API call with the function result
                payload["messages"] = messages
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                result = response.json()
                
                if 'choices' in result and len(result['choices']) > 0:
                    final_message = result['choices'][0]['message']
                    print("\nFinal Response:")
                    print("-" * 30)
                    print(final_message['content'])
            else:
                print("\nAssistant's Response:")
                print("-" * 30)
                print(message['content'])
                
            # Print citations if available
            if 'citations' in result and result['citations']:
                print("\nCitations:")
                print("-" * 30)
                for citation in result['citations']:
                    print(f"- {citation}")
        else:
            print("\nNo message content found in the response")
            
    except requests.exceptions.RequestException as e:
        print(f"\nError making API request: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response text: {e.response.text}")
    except json.JSONDecodeError as e:
        print(f"\nError decoding JSON response: {str(e)}")
        print(f"Raw response: {response.text}")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
    
    return True

if __name__ == "__main__":
    print("Welcome to the Information Assistant!")
    print("You can get information about weather, stocks, news, and companies.")
    
    while True:
        user_query = get_user_query()
        if not process_query(user_query):
            print("\nThank you for using the Information Assistant!")
            break 