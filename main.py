from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from bot import Bot, ClickAction, KeyBoardAction


prompt = input("Enter prompt")
website = input("Enter website")
bot = Bot(prompt)
chromedriver_path = "./chromedriver-linux64/chromedriver"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)
driver.get(website)
driver.execute_script("")
WebDriverWait(driver,5)
while True:
    page_html = driver.page_source
    action = bot.get_action(page_html)
    if action is None:
        break
    if isinstance(action,ClickAction):
        elements = driver.execute_script(f" return document.querySelectorAll('{action.query_selector}')")
        elements[0].click()
    elif isinstance(action,KeyBoardAction):
        elements = driver.execute_script(f" return document.querySelectorAll('{action.query_selector}')")
        elements[0].send_keys(action.key_to_press)
    