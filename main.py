from selenium import webdriver
from selenium.common.exceptions import *
import math
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from my_functions import *
import logging
import time
from selenium import webdriver
from jobs import REACT_JOBS
from config import get_driver, sign_in
from search_constants import languagesToexclude


def bot(url, application_sent):
    try:
        # send applications
        driver.get(url)
        results_number = listings_size(driver)
        time.sleep(2)
        scroll_listings(driver)
        # get the number of pagination of the all offers
        global paginations
        try:
            paginations = driver.find_elements_by_css_selector(
                ".artdeco-pagination__indicator--number"
            )
        except:
            print("pagination not found")
        jobs_clicked = 0

        pages_number = math.ceil(results_number / 25)
        for i in range(pages_number):
            click_paginations(i, driver)
            results_number = listings_size(driver)
            listings = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".job-card-list__title")
                )
            )
            print(f"length of jobs offer{len(listings)}")
            jobsSubtitle = driver.find_elements_by_class_name(
                "job-card-list__entity-lockup"
            )

            for j in range(len(listings)):
                try:
                    listings[j].click()
                    jobs_clicked += 1
                    print(f"jobs_clicked{jobs_clicked}")
                    progress = math.floor((jobs_clicked / results_number) * 100)
                    print(f"progress : {progress}%")
                    # check if the listing offer title has one of the words mentionned
                    jobTitle = listings[j].text.lower()
                    jobSubtitle = jobsSubtitle[j].text.lower()
                    test2 = [False]
                    test1 = [
                        True for language in languagesToexclude if language in jobTitle
                    ]
                    test3 = [True for word in jobTitle.split() if word in "java"]

                    countriesToExclude = ["gitential"]

                    test2 = [
                        True for country in countriesToExclude if country in jobSubtitle
                    ]

                    if len(test1) > 0 or test2 == [True] or len(test3) > 0:
                        continue
                    time.sleep(1)

                except Exception as Argument:
                    print("error when clicking on the job offer")
                    logging.exception("Error during bot execution")

                # exclude any jobs that requires work auto or presence in the country

                try:
                    scroll_offer_forward(driver)
                    match_section_text = driver.find_element_by_class_name(
                        "job-details-how-you-match-card__header"
                    ).text
                    location_text = "Your location does not match country requirements"
                    work_permit_text = "This job requires a work authorization"
                    if (
                        location_text in match_section_text
                        or work_permit_text in match_section_text
                    ):
                        continue
                    scroll_offer_backward(driver)

                except:
                    print("error checking job match")

                # Try to locate the apply button, if can't locate then skip the job.
                try:
                    time.sleep(2)
                    apply_button = WebDriverWait(driver, 13).until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, "jobs-apply-button")
                        )
                    )

                    if apply_button.text == "Easy Apply":
                        apply_button.click()
                    time.sleep(1)
                    print("application button clicked")

                    close_bot_detection_modal(driver)

                    submitClick = 0
                    time.sleep(5)
                    submit_button = get_easy_apply_next_btn(driver)
                    my_number = "94304891"

                    while (
                        submit_button.text != "Submit application" and submitClick < 10
                    ):
                        try:
                            try:
                                if submitClick < 1:
                                    modal_el = driver.find_element_by_class_name(
                                        "jobs-easy-apply-modal"
                                    )
                                    inputs_el = modal_el.find_elements_by_tag_name(
                                        "input"
                                    )
                                    inputs_number = len(inputs_el)
                                    if inputs_number < 2:
                                        input_el = modal_el.find_element_by_tag_name(
                                            "input"
                                        )
                                        input_el.send_keys(my_number)
                                    elif inputs_number == 3:
                                        answer_input_question(inputs_el[0], "Nabil")
                                        answer_input_question(inputs_el[1], "Messaoud")
                                        select_country_el = (
                                            modal_el.find_element_by_tag_name("select")
                                        )
                                        answer_select_question(
                                            select_country_el, "Tunisia (+216)"
                                        )
                                        answer_input_question(inputs_el[2], my_number)

                                else:
                                    answer_questions(driver)
                            except:
                                print("error finding input label")

                            submit_button.click()
                            submitClick += 1
                            time.sleep(1)
                            submit_button = get_easy_apply_next_btn(driver)
                        except:
                            print("error clicking next")
                            close_application(driver)

                    submit_button.click()
                    if submit_button.text == "Submit application":
                        application_sent += 1
                        print(f"applications sent : {application_sent}")
                    else:
                        close_application(driver)
                        continue

                    # Once application completed, close the pop-up window.
                    time.sleep(2)
                    try:
                        close_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, ".artdeco-modal__dismiss")
                            )
                        )
                        close_button.click()
                    except:
                        print("No close button found, skipped.")
                    # close success toaster
                    try:
                        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                        time.sleep(2)
                    except:
                        print("No close button of toaster found, skipped.")
                        time.sleep(2)

                    # If already applied to job or job is no longer accepting applications, then skip.
                except:
                    print("No application button, skipped.")
                    time.sleep(1)
                    continue

            if results_number == jobs_clicked:
                print(f"Job is done for this url {url}")
                return application_sent

    except Exception:
        logging.exception("Error during bot execution")
        return


if __name__ == "__main__":
    print("linkedIn app is running")
    # Sign in
    driver = get_driver()
    try:
        sign_in(driver)
    except:
        print("i am already logged in")

    application_sent = 0

    for url in REACT_JOBS:
        bot(url, application_sent)
