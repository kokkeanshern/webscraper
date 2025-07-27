import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from constants import Captcha, Links, FundazticLocators
from captcha.ocr import solve_captcha
from utils.interactions import send_key, click_element, save_image

# ToDo: Ensure setup works on Linux machines (infra will use Linux).
# ToDo: Add retry logic for failed submissions.

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Initialize the WebDriver and navigate to the login page.
    driver = webdriver.Chrome()
    driver.get(Links.fundaztic_login)

    # Saves the captcha image from the browser in the project directory.
    save_image(
        driver,
        Captcha.raw_image_file,
        By.CSS_SELECTOR,
        FundazticLocators.login_page__captcha_puzzle,
    )

    result = solve_captcha(Captcha.raw_image_file)
    logging.info(f"Captcha solved: {result}")

    # Fill in the login form with email, password, and captcha value
    send_key(
        driver,
        os.environ["FUNDAZTIC_EMAIL"],
        By.ID,
        FundazticLocators.login_page__email_input,
    )
    send_key(
        driver,
        os.environ["FUNDAZTIC_PASSWORD"],
        By.NAME,
        FundazticLocators.login_page__password_input,
    )
    send_key(driver, result, By.NAME, FundazticLocators.login_page__captcha_input)
    click_element(driver, By.CLASS_NAME, FundazticLocators.login_page__submit_button)

    time.sleep(7)
    driver.quit()
