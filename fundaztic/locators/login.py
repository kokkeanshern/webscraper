import base64
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# TODO:
# Add type hints to the functions.
# Consolidate function logic to reduce redundancy.


def resolve_email_input(driver, key):
    """
    Enters the email into the login form.
    Args:
       driver: Selenium WebDriver instance.
       key (str): The email to be entered.
    Returns:
       None
    """
    email_input = driver.find_element(By.ID, "username")
    email_input.send_keys(key)


def resolve_password_input(driver, key):
    """
    Enters the password into the login form.
    Args:
       driver: Selenium WebDriver instance.
       key (str): The password to be entered.
    Returns:
       None
    """
    password_input = driver.find_element(By.NAME, "pwd")
    password_input.send_keys(key)


def resolve_verification_input(driver, key):
    """
    "Silently" enters the captcha value to prevent refreshing the captcha challenge.
    Args:
       driver: Selenium WebDriver instance.
       key (str): The captcha value to be entered.
    Returns:
       None
    """
    driver.execute_script(
        "document.getElementsByName('captcha')[0].value = arguments[0];", key
    )


def save_captcha_image(driver, img_file):
    """
    Saves the captcha image from the browser to a file.
    Args:
       driver: Selenium WebDriver instance.
       img_file (str): The file path where the captcha image will be saved.
    Returns:
       None
    """
    captcha_img = driver.find_element(
        By.CSS_SELECTOR, "img[src*='/cic/code?name=user_login']"
    )

    img_data = driver.execute_script(
        """
                                    const img = arguments[0];
                                    const canvas = document.createElement('canvas');
                                    canvas.width = img.naturalWidth;
                                    canvas.height = img.naturalHeight;
                                    const ctx = canvas.getContext('2d');
                                    ctx.drawImage(img, 0, 0);
                                    return canvas.toDataURL('image/png').substring(22);  // remove data:image/png;base64,
                                    """,
        captcha_img,
    )

    with open(img_file, "wb") as f:
        f.write(base64.b64decode(img_data))


def click_submit_button(driver):
    """
    Clicks the submit button to log in.
    Args:
       driver: Selenium WebDriver instance.
    Returns:
       None
    """
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "loginBnt"))
    )
    login_button.click()
