import requests
from pathlib import Path
from utils.generic import save_file
from selenium.webdriver.remote.webdriver import WebDriver


def download_file(
    driver: WebDriver,
    base_url: str,
    params: dict,
) -> None:
    """
    Downloads a transaction file from the Fundaztic website.

    Args:
        driver (WebDriver): Selenium WebDriver instance.
        base_url (str): The base URL for the transaction download endpoint.
        params (dict): Parameters to be sent with the GET request.

    Returns:
        None
    """

    # Create a session and set cookies to remain logged in.
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie["name"], cookie["value"])

    response = session.get(base_url, params=params)

    save_file(
        file_path=Path(__name__).resolve().parent
        / "files"
        / "received_distribution.xls",
        write_content=response.content,
    )
