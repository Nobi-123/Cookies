"""
cookies_gen.py
--------------
Generate YouTube cookies and return them as a BytesIO file for Telegram.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile
from io import BytesIO

# --- Setup Selenium Chrome options ---
options = options()
prefs = {'exit_type': 'Normal'}
options.add_experimental_option("prefs", {'profile': prefs})
options.add_argument("--headless=new")  # Headless mode for Heroku/VPS
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-infobars")
options.add_argument("--autoplay-policy=no-user-gesture-required")
options.add_experimental_option("excludeSwitches", ['enable-automation'])
options.add_argument(f"user-data-dir={tempfile.mkdtemp()}")  # unique temp profile
options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) "
                     "AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")

# --- Initialize WebDriver ---
driver = webdriver.Chrome(options=options)

def save_cookies_to_netscape(cookies):
    """
    Save cookies to Netscape format string
    """
    output = "# Netscape HTTP Cookie File\n# Generated automatically by @TNCnetwork!\n\n"
    output += "# domain\t include_subdomains\t path\t secure\t expiration_date\t name\t value\n"
    for cookie in cookies:
        expiry = cookie.get('expiry') or cookie.get('expires') or 0
        output += f"{cookie['domain']}\t"
        output += "TRUE\t"
        output += f"{cookie['path']}\t"
        output += "TRUE\t" if cookie.get('secure') else "FALSE\t"
        output += f"{int(expiry)}\t"
        output += f"{cookie['name']}\t{cookie['value']}\n"
    return output

def generate_dynamic_cookie():
    """
    Generate cookies and return as BytesIO for Telegram
    """
    cookies = driver.get_cookies()
    cookie_str = save_cookies_to_netscape(cookies)

    # Convert to BytesIO
    cookie_file = BytesIO()
    cookie_file.name = "cookies.txt"
    cookie_file.write(cookie_str.encode())
    cookie_file.seek(0)
    return cookie_file

def quit_driver():
    driver.quit()
