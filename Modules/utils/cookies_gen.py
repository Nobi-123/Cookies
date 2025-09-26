from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

def generate_dynamic_cookie(user_id: int) -> str:
    """
    Generates YouTube cookies using headless Chrome and returns them as a string.
    """

    # Setup Chrome options for Heroku
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    )

    # Use ChromeDriver installed by buildpack
    driver_path = os.getenv("GOOGLE_CHROME_BIN", "/usr/bin/google-chrome")
    chrome_driver_path = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")

    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

    # Open YouTube (user must have logged in manually in advance)
    driver.get("https://www.youtube.com")
    time.sleep(5)  # wait for page & cookies to load

    cookies = driver.get_cookies()
    driver.quit()

    # Format cookies as a single string
    cookie_str = ""
    for cookie in cookies:
        cookie_str += f"{cookie['name']}={cookie['value']}; "

    return cookie_str.strip()
