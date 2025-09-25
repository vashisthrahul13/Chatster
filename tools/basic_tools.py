from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool,Tool
import requests
from langchain_google_community import GoogleSearchAPIWrapper
from dotenv import load_dotenv
import os


# # Go one step back to the base folder
base_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "..",'..'))

# Construct the .env path
env_path = os.path.join(base_dir, ".env")

load_dotenv(env_path)
# search_tool = DuckDuckGoSearchRun(region ='us-en')
search_tool_wrapper = GoogleSearchAPIWrapper()

search_tool = Tool(
    name="google_search",
    description="Search Google for recent results.",
    func=search_tool_wrapper.run,
)

@tool
def calculator(first_num:float,second_num:float,operation:str) -> str:
    """
    Perform a basic arithmetic operation on two numbers
    Supported operations : add, sub, mul, div
    """

    try:
        if operation =='add':
            result = first_num + second_num
        elif operation =='sub':
            result = first_num - second_num
        elif operation =='mul':
            result = first_num * second_num
        elif operation =='div':
            if second_num ==0:
                return {'error':'Division by zero not allowed'}
            result = first_num / second_num
        else:
            return {'error':f"unsupported operation '{operation}'"}
        
        return {'first_num':first_num, 'second_num':second_num, 'operation':operation, 'result':result}
    
    except Exception as e:
        return {'error':str(e)}
    

@tool
def get_stock_price(symbol:str) -> dict:
    """
    Fetch latest stock price for a given symbol (eg. 'AAPL','TSLA')
    using Alpha Vantage with API key in the url
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    r = requests.get(url)
    return r.json()
