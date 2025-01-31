from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("https://w3schools.com")

# Use JavaScript to select elements like jQuery
elements = driver.execute_script("return document.querySelectorAll('.ga-nav');")
print("wd", elements)