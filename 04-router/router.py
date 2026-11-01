from dotenv import load_dotenv
from openai import OpenAI
from models import Router

import json
import os


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
MODEL = "gpt-4o-mini"


#I am asking llm to make the routing desicion. 

def route(goal: str) -> Router:
    response = client.responses.parse(
        model=MODEL,
            input=
            [
                {
                    "role": "system",
                    "content": 
                    f'''
                    Your job is to classify the incoming request.
                    there are only 4 valid routing categories:
                    

1-coding
Use this category if the user asks about programming, debugging,
or code-related problems.

2-research
Use this category if the user asks for research, comparisons,
or information gathering.

3-support
Use this category if the user explicitly needs customer support,
such as billing, refunds, subscriptions, account access, or orders.
Do not assume a request is support simply because the user asks for help.

4-unclear
Use this category if there is insufficient information to determine
which specialist should handle the request.
If multiple categories are plausible and the user's intent is
not clear, choose unclear instead of guessing.

'''

                },
                {
                    "role": "user",
                    "content": goal
                    
                },
            ],
            text_format=Router
    )

    if response.output_parsed is None:
        raise ValueError("No parsed routing decision returned")

    
    return response.output_parsed



if __name__ == "__main__":
    result = route("I want to check my refund status")
    print(result)

    if result.confidence < 0.7 or result.category == "unclear":
        print("I need help with my application")