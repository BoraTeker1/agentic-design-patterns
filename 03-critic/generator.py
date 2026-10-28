from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()

client = OpenAI()
MODEL = "gpt-4o-mini"

class Generate(BaseModel):
    result: str

tools = []



def generator(spec: str, previous_code: str = None, feedback: list[str] =  None) -> str:
    #if this is the first time execute it and check if it passes
    if previous_code is None and feedback is None:
        user_prompt = f"""
        Read the following specification carefully and generate python code. 
        {spec}
        """

    #if there has been previous executions you have to review them as well. 
    else:
        #revise the previous code
        user_prompt = f'''
        Original specification: 
        {spec}

        Previous code:
        {previous_code}

        Feedback from failed tests:
        {feedback}

        Revise the previous code to fix the issues while satisfying the original specification. 
        '''
        
    response = client.responses.parse(
        model=MODEL,
        input= [
            {
            "role": "system",
            "content": 
            (
            "You are a python code generator. "
            "Return only python source code in the result field "
            "without markdown formatting or explanations."
            )
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        text_format=Generate
    )

    if response.output_parsed is None:
        raise ValueError("The model did not return a parsed output.")

    return response.output_parsed.result


spec = """
Write a function called is_palindrome that takes a string and returns true if the 
string reads the same forwards and backwards, otherwise False. 
"""






if __name__ == "__main__":
    draft = generator(spec)
    print(draft)




