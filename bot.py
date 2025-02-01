import os

from typing import Annotated, Union
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


class Action(BaseModel):
    action_type: str
    action: Union[ClickAction, KeyBoardAction]


client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

KEYMAP = {
    k: v
    for k, v in Keys.__dict__.items()
    if not k.startswith("__") and k != "ZENKAKU_HANKAKU"
}


class Bot:
    def __init__(self, prompt: str) -> None:
        self.prompt = prompt
        self.history = [
            {
                "role": "system",
                "content": f"You are a helpful assistant. Your job is to help the user with '{prompt}'. The user will give you the current HTML of the webpage and you will respond with an action to carry out to achieve the goal of the user. After that the user will again give the HTML of the webpage and the loop continues till the task is completed, at which case return none. For keys that are not printable characters, use this keymap for reference and follow it strictly: {KEYMAP}",
            },
        ]

    def get_action(self, html: str) -> Action | None:
        self.history.append(
            {
                "role": "user",
                "content": f"The current HTML of the webpage is\n\n{html}\n\nWhen outputting the query selector ensure that it is present in the html corpus supplied to you. That element will be interacted with on the webpage\n\nRespond with: " + """
{
'action_type': 'click' | 'keypress',
'action': {
    'query_selector': '',
    'key_to_press': ''
} | {
    'query_selector': '', // this is for clicking
}
}""",
            }
        )
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            n=1,
            messages=self.history,  # type: ignore
            response_format={"type": "json_object"},  # type: ignore
        )
        self.history.append(
            {
                "role": "assistant",
                "content": f"Action: {response.choices[0].message.content}",
            }
        )
        print("AI decision: ", response.choices[0].message.content)
        return Action.model_validate_json(response.choices[0].message.content or "{}")