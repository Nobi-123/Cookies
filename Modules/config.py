
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
DEFAULT_TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", "TNCnetwork")
LOG_CHANNEL = os.getenv("LOG_CHANNEL", "-1003065367480")
from Modules.utils.default_cookies import get_default_cookie
DEFAULT_COOKIE = get_default_cookie()
