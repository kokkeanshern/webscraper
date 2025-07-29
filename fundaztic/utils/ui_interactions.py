import base64
from utils.generic import save_file
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


def send_key(driver: WebDriver, key: str, element_type: By, element_id: str):
    element: WebElement = driver.find_element(element_type, element_id)
    element.send_keys(key)


def click_element(driver: WebDriver, element_type: By, element_id: str):
    element: WebElement = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((element_type, element_id))
    )
    element.click()


def save_image(
    driver: WebDriver, img_file_name: str, element_type: By, element_id: str
):
    """
    Saves the captcha image from the browser to a file.
    Args:
       driver: Selenium WebDriver instance.
       img_file_name (str): The file path where the captcha image will be saved.
    Returns:
       None
    """
    captcha_img = driver.find_element(element_type, element_id)

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
    save_file(file_path=img_file_name, write_content=base64.b64decode(img_data))
