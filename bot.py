import os

from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ClickAction(BaseModel):
    query_selector: str


class KeyBoardAction(BaseModel):
    query_selector: str
    key_to_press: str



client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

def get_action(html: str) -> ClickAction | KeyBoardAction | None:
    response = client.beta.chat.completions.parse(
        model="gemini-1.5-flash",
        n=1,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Explain to me how AI works"
            }
        ],
        response_format=ClickAction | KeyBoardAction, # type: ignore
    )
    return response.choices[0].message.parsed