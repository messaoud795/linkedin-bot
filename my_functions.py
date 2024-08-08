import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.ui import Select


# click on pagination
def click_paginations(counter, driver):
    try:
        if counter > 1:
            next_btn = driver.find_element_by_class_name(
                "jobs-search-pagination__button--next"
            )
            next_btn.click()
    except:
        print("pagination button is not found")


# find an element iteration
def find_element_by_name(driver, name):
    element_tag = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, name))
    )
    return element_tag


# find elements by css selector
def find_element_by_xpath(driver, xpatch):
    element_tag = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, xpatch))
    )
    return element_tag


def find_elements_by_css(driver, css):
    element_tag = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, css))
    )
    return element_tag


def find_element_by_css(driver, css):
    element_tag = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css))
    )
    return element_tag


def scroll_listings(driver):
    listings = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-list__title"))
    )
    # scroll down in results body to load all of them
    touch_action = TouchActions(driver)
    touch_action.scroll_from_element(listings[0], 0, 5000).perform()
    time.sleep(2)


def scroll_offer_forward(driver):
    offer = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".jobs-search__job-details--wrapper")
        )
    )
    # scroll down in results body to load all of them
    touch_action = TouchActions(driver)
    touch_action.scroll_from_element(offer[0], 0, 2000).perform()
    time.sleep(2)


def scroll_offer_backward(driver):
    offer = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".jobs-search__job-details--wrapper")
        )
    )
    touch_action = TouchActions(driver)
    touch_action.scroll_from_element(offer[0], 0, -2000).perform()
    time.sleep(2)


def close_application(driver):
    try:
        driver.find_element_by_xpath("/html/body/div[3]/div/div/button").click()
        discard_button = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".artdeco-modal__confirm-dialog-btn")
            )
        )[1]
        discard_button.click()
    except:
        print("error closing application modal")

    print("Complex application, skipped.")


# get the number of results
def listings_size(driver):
    try:
        # total_results =  driver.find_elements_by_class_name("jobs-search-results-list__text")[1].text.replace('results', '')
        total_results = find_element_by_css(
            driver, ".jobs-search-results-list__subtit" "le"
        ).text.replace("results", "")
        results = int(total_results.replace(",", ""))
        print(f"total results : {results}")

        return results
    except Exception:
        return Exception


def get_easy_apply_next_btn(driver):
    modal_el = driver.find_element_by_class_name("jobs-easy-apply-modal")
    footer = modal_el.find_element_by_tag_name("footer")
    submit_button = footer.find_elements_by_tag_name("button")[-1]
    return submit_button


def answer_input_question(input_el, text):
    input_el.clear()
    input_el.send_keys(text)


def answer_select_question(select_el, text):
    select = Select(select_el)
    select.select_by_visible_text(text)


years_3_experience_skills = [
    "html",
    "html5",
    "css",
    "css3" "node",
    "node.js",
    "mongo",
    "mongodb",
    "javascript",
    "react",
    "information",
    "it",
    "software",
    "development",
    "sass",
    "scss",
    "visual studio",
    "reactjs",
    "typescript",
    "linux",
    "front",
    "back",
    "frontend",
    "backend",
    "web",
    "nosql",
    "engineering",
    "vs code",
]
years_2_experience_skills = ["python", "sql", "aws", "redis"]
years_1_experience_skills = ["react native", "mobile"]


def answer_checkbox_question(fieldset_el, answer_value):
    input_elements = fieldset_el.find_elements_by_tag_name("input")
    for input in input_elements:
        label_el = input.get_attribute("value")
        if label_el == answer_value:
            input.click()
            return


def skill_check(label, skills):
    check = False
    for skill in skills:
        if skill in label:
            check = True
    return check


def answer_questions(driver):
    try:
        modal_el = driver.find_element_by_class_name("jobs-easy-apply-modal")

        try:
            inputs = modal_el.find_elements_by_tag_name("input")

            for input in inputs:
                label_el = input.find_element(By.XPATH, "preceding-sibling::label")
                label = label_el.text.lower()
                years3 = skill_check(label, years_3_experience_skills)
                years2 = skill_check(label, years_2_experience_skills)
                years1 = skill_check(label, years_1_experience_skills)
                if years3:
                    answer_input_question(input, "3")
                elif years2:
                    answer_input_question(input, "2")
                elif years1:
                    answer_input_question(input, "1")
                elif "portfolio" in label:
                    answer_input_question(
                        input, "https://portfolio-nabil-messaoud.netlify.app/"
                    )
                else:
                    answer_input_question(input, "0")

        except Exception:
            print("error locating inputs")

        try:
            selects = modal_el.find_elements_by_tag_name("select")
            for select in selects:
                label_el = select.find_element(By.XPATH, "preceding-sibling::label")
                label = label_el.text.lower()

                if "english" in label:
                    answer_select_question(select, "Professional")
                elif "french" in label:
                    answer_select_question(select, "Professional")
                elif "français" in label:
                    answer_select_question(select, "Professionel")
                elif "anglais" in label:
                    answer_select_question(select, "Professionel")
                elif "deutsch" in label:
                    answer_select_question(select, "Gut")
                elif "deutsch" in label:
                    answer_select_question(select, "Verhandlungssicher")
                elif "german" in label:
                    answer_select_question(select, "Conversational")
                elif "live" in label:
                    answer_select_question(select, "No")
                elif "authori" in label:
                    answer_select_question(select, "No")
                elif "relocat" in label:
                    answer_select_question(select, "Yes")
                else:
                    answer_select_question(select, "None")

        except Exception:
            print("error locating selects")

        try:
            fieldsets = modal_el.find_elements_by_class_name(
                "fb-text-selectable__option"
            )
            for fieldset in fieldsets:
                label_el = fieldset.find_element_by_tag_name("legend")
                label = label_el.text.lower()
                yes_answers_questions = [
                    "relocat",
                    "remote",
                    "hybrid",
                    "on-site",
                    "visa",
                ]
                yes_answers_ckeck = skill_check(label, yes_answers_questions)
                no_answers_questions = ["live", "authori"]
                no_answers_check = skill_check(label, no_answers_questions)

                if yes_answers_ckeck:
                    answer_checkbox_question(fieldset, "Yes")
                elif no_answers_check:
                    answer_checkbox_question(fieldset, "No")
                else:
                    answer_checkbox_question(fieldset, "No")

        except Exception:
            print("error locating checkboxes")

    except Exception:
        print("error answering questions")


def close_bot_detection_modal(driver):
    try:
        modal_el = driver.find_element_by_class_name("artdeco-modal")
        btns = modal_el.find_elements_by_tag_name("button")
        if btns[-1].text == "Continue applying":
            btns[-1].click()
    except Exception:
        print("error closing  bot detector modal")


def save_cookies(driver):
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb")).get(
        "https://www.linkedin.com/jobs/"
    )


def load_cookies(driver):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
