import os
import time
import logging
from jinja2 import Template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from captcha.ocr import solve_captcha
from utils.number_cruncher import aggregate_received_distribution
from utils.ui_interactions import send_key, click_element, save_image
from constants import Captcha, Links, FundazticLocators, FilePaths, FileNames
from utils.email_sender import Email
from utils.generic import delete_file


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    options = Options()
    options.add_argument("--window-size=1051,798")
    options.add_argument("--headless")
    prefs = {
        "download.default_directory": str(FilePaths.download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    driver.get(Links.fundaztic_login)

    time.sleep(10)

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
    click_element(
        driver, By.CSS_SELECTOR, "a.QueriesBnt[href^='javascript:export_eight']"
    )

    # For some reason, wait_and_rename_latest_download() has issues resulting in corrupted files.
    # Using an explicit wait as a workaround this for now.
    time.sleep(10)
    files = list(FilePaths.download_dir.glob("*"))
    if files:
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        new_path = FilePaths.download_dir / FileNames.received_distribution_xls
        if new_path.exists():
            new_path.unlink()
        latest_file.rename(new_path)

    result = aggregate_received_distribution()

    with open("templates/report_template.html") as f:
        template = Template(f.read())

    html_email = template.render(
        mtd_net_interest=result["mtd_net_interest"],
        mtd_principal=result["mtd_principal"],
        mtd_fees=result["mtd_fees"],
        prev_net_interest=result["prev_net_interest"],
        prev_principal=result["prev_principal"],
        prev_fees=result["prev_fees"],
        m1_net_interest=result["m1_net_interest"],
        m1_principal=result["m1_principal"],
        m1_fees=result["m1_fees"],
        m2_net_interest=result["m2_net_interest"],
        m2_principal=result["m2_principal"],
        m2_fees=result["m2_fees"],
        m3_net_interest=result["m3_net_interest"],
        m3_principal=result["m3_principal"],
        m3_fees=result["m3_fees"],
    )

    email = Email(
        subject="Fundaztic Daily Report",
        from_email=os.environ["SERVICE_EMAIL"],
        to_email=os.environ["RECEIPIENT_EMAIL"],
        body=html_email,
    )
    email.send_email("smtp.gmail.com")

    driver.quit()

    # Cleanup all downloaded files.
    delete_file()
