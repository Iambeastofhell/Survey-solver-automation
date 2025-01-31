from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://selenium.dev/')
browser.get_full_page_screenshot_as_file('screenshot.png')