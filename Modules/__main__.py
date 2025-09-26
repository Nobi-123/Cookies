
from pyrogram import Client, filters
from Modules.utils.default_cookies import get_default_cookie
from Modules.plugins.bot import start
import os

API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

app = Client("YouTubeCookiesBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await start.handle_start(client, message)

@app.on_message(filters.command("getcookie"))
async def getcookie_command(client, message):
    cookie = get_default_cookie()
    await message.reply_text(f"Here is the default YouTube cookie:\n\n{cookie}")

if __name__ == "__main__":
    print("YouTubeCookiesBot is running...")
    app.run()
