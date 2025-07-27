import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from constants import Captcha, Links, FundazticLocators, ApiParams
from captcha.ocr import solve_captcha
from utils.ui_interactions import send_key, click_element, save_image
from utils.api_interactions import download_file

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

    ocr_captcha_value = solve_captcha(Captcha.raw_image_file)
    logging.info(f"OCR Model Detected Captcha Value: {ocr_captcha_value}")

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
    # Submitting the captcha value via send_keys triggers the login submission - no need to click the "submit" button.
    send_key(
        driver, ocr_captcha_value, By.NAME, FundazticLocators.login_page__captcha_input
    )

    # Navigate to the Investments page and download the transaction file.
    click_element(driver, By.LINK_TEXT, "My Investments")
    click_element(driver, By.LINK_TEXT, "Received Distribution")
    _params = ApiParams(
        {
            "beginTime": None,
            "endTime": None,
            "loansignId": None,
        }
    )

    download_file(
        driver=driver, base_url=Links.fundaztic_transaction_download, params=_params
    )

    time.sleep(7)
    driver.quit()
