import os
import time
import logging
from selenium import webdriver
from locators import login
from constants import Captcha
from captcha.ocr import solve_captcha


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    driver = webdriver.Chrome()
    driver.get("https://p2p.fundaztic.com/visitor/to-login")

    email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]

    login.resolve_email_input(driver, email)
    login.resolve_password_input(driver, password)

    # Saves the captcha image from the browser in the project directory.
    login.save_captcha_image(driver, Captcha.raw_image_file)

    result = solve_captcha(Captcha.raw_image_file)
    logging.info(f"Captcha solved: {result}")

    login.resolve_verification_input(driver, result)

    login.click_submit_button(driver)

    time.sleep(7)
    driver.quit()
