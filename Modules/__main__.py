from Modules.plugins.bot import start  # start.py already has app and handlers
import os
from pyrogram import Client

API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

# The app is already created in start.py, so we just run it
if __name__ == "__main__":
    print("YouTubeCookiesBot is running...")
    start.app.run()
