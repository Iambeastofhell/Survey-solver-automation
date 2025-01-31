import os

from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

from selenium.webdriver.common.keys import Keys

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

KEYMAP = {k:v for k,v in Keys.__dict__.items() if not k.startswith("__") and k != 'ZENKAKU_HANKAKU'}

class Bot:
    def __init__(self, prompt: str) -> None:
        self.prompt = prompt
        self.history = [
            {
                "role": "system",
                "content": f"You are a helpful assistant. Your job is to help the user with '{prompt}'. The user will give you the current HTML of the webpage and you will respond with an action to carry out to achieve the goal of the user. After that the user will again give the HTML of the webpage and the loop continues till the task is completed, at which case return none. For keys that are not printable characters, use this keymap for reference and follow it strictly: {KEYMAP}",
            },
        ]

    def get_action(self, html: str) -> ClickAction | KeyBoardAction | None:
        self.history.append(
            {
                "role": "user",
                "content": f"The current HTML of the webpage is\n\n{html}",
            }
        )
        response = client.beta.chat.completions.parse(
            model="gemini-1.5-flash",
            n=1,
            messages=self.history, #type: ignore
            response_format=ClickAction | KeyBoardAction,  # type: ignore
        )
        self.history.append(
            {
                "role": "assistant",
                "content": f"Action: {response.choices[0].message.parsed}",
            }
        )
        print("AI decision: ", response.choices[0].message.parsed)
        return response.choices[0].message.parsed

