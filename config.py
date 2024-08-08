from selenium import webdriver
from dotenv import load_dotenv
import os
from my_functions import *
from selenium.webdriver.common.keys import Keys

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("w3c", False)
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        executable_path="C:\development\chromedriver", options=options
    )
    return driver


def sign_in(driver):
    driver.get("https://www.linkedin.com/login/")
    emailTag = find_element_by_name(driver, "session_key")
    emailTag.send_keys(EMAIL)
    passwordTag = find_element_by_name(driver, "session_password")
    passwordTag.send_keys(PASSWORD)
    passwordTag.send_keys(Keys.ENTER)
    time.sleep(30)
