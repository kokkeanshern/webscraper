import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from constants import Captcha, Links, FundazticLocators, FilePaths
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from captcha.ocr import solve_captcha
from utils.generic import wait_and_rename_latest_download
from utils.ui_interactions import send_key, click_element, save_image

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    options = Options()
    options.add_argument("--window-size=1051,798")
    prefs = {
        "download.default_directory": str(FilePaths.download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
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
    send_key(
        driver, ocr_captcha_value, By.NAME, FundazticLocators.login_page__captcha_input
    )

    # Navigate to the Investments page and download the transaction file.
    click_element(driver, By.LINK_TEXT, "My Investments")
    click_element(driver, By.LINK_TEXT, "Received Distribution")

    driver.get(Links.fundaztic_transaction_download)

    # Wait and rename the downloaded file
    wait_and_rename_latest_download(
        FilePaths.download_dir, "fundaztic_transactions.xls"
    )

    driver.quit()
