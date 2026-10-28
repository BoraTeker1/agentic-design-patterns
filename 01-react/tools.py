import os
from dotenv import load_dotenv
from tavily import TavilyClient
from datetime import date

load_dotenv()

def get_current_date():
    today = date.today()
    return today


def calculate(expression):
    try:
        first_val, compute, second_value = expression.split()
        first_val = float(first_val)
        second_value = float(second_value)

    except ValueError:
        return "Invalid Input. Use format '10 + 5'"

    if compute == '+':
        return first_val + second_value
        
    elif compute == '-':
        return first_val - second_value
       

    elif compute == '*':
        return first_val * second_value
       

    elif compute =='/':
        if float(second_value) == 0:
            return "Can not divide by 0"
        return first_val / second_value

    else:
        print("unsupported operator")


def web_search(query):
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY is missing")

    tavily_client = TavilyClient(api_key=api_key)
    response = tavily_client.search(query)
    
    res = []
    for item in response['results'][:3]:
        new_dict = {}
        new_dict['title'] = item['title']
        new_dict['url'] = item['url']
        new_dict['content'] = item['content']
        res.append(new_dict)
    

    return res









if __name__ == "__main__":
    print(web_search("Who is Lionel Messi?"))