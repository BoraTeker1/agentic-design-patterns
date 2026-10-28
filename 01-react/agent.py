
import json
from tools import calculate, get_current_date, web_search
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
MAX_STEPS = 10
MODEL = "gpt-4o-mini"

tools = [
    {
        "type": "function",
        "name": "calculate",
        "description": "Perform arithmetic calculations. Use this tool for addition, subtraction, multiplication, and division.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A mathematical expression in the format '10 + 5'. Use spaces between operands and operator."
                }
            },
            "required": ["expression"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_current_date",
        "description": "Get the current date. Use this tool when answering questions that require today's date.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "web_search",
        "description": "Search the internet for external or up-to-date information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to send to the web search engine."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        },
        "strict": True
    }
]

#tools_without_date = []
#for tool in tools:
    #if tool["name"] != "get_current_date":
        #tools_without_date.append(tool)

#tools = tools_without_date


def run_agent(question):
    response = client.responses.create(
        model=MODEL,
        input=question,
        tools=tools
    )

    for step in range(1, MAX_STEPS + 2):
        tool_calls = []

        for item in response.output:
            if item.type == "function_call":
                tool_calls.append(item)

        if not tool_calls:
            print("\nFinal Answer:")
            print(response.output_text)
            return response.output_text

        if step > MAX_STEPS:
            print("\nMaximum steps reached")
            return None

        print(f"\n--- Step {step} ---")

        tool_outputs = []

        for item in tool_calls:
            print(f"Tool requested: {item.name}")
            print(f"Arguments: {item.arguments}")

            try:
                arguments = json.loads(item.arguments)

                if item.name == "calculate":
                    result = calculate(arguments["expression"])

                elif item.name == "get_current_date":
                    result = get_current_date()

                elif item.name == "web_search":
                    result = web_search(arguments["query"])

                else:
                    raise ValueError(f"Unknown tool: {item.name}")

                output = json.dumps(
                    {"ok": True, "data": result},
                    default=str
                )

            except Exception as e:
                output = json.dumps({
                    "ok": False,
                    "error": str(e)
                })

            print(f"Tool result: {output[:500]}")

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": output
            })

        response = client.responses.create(
            model=MODEL,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=tools
        )


if __name__ == "__main__":
    run_agent(
        "How many days until the next US federal holiday, and which one is it?"
    )
