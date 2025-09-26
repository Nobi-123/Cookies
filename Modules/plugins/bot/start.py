# Modules/plugins/bot/start.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Modules.utils.cookies_gen import generate_dynamic_cookie
from Modules.config import BOT_TOKEN, REQUIRED_CHANNEL
from Modules.utils.database import add_user, add_log
import os

app = Client("YouTubeCookiesBot", bot_token=BOT_TOKEN)
LOG_CHANNEL = -1003065367480  # Replace with your actual log channel ID

async def check_must_join(client, user_id):
    """Check if user has joined the required channel."""
    try:
        member = await client.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

@app.on_message(filters.command("start") & filters.private)
async def handle_start(client, message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"

    if not await check_must_join(client, user_id):
        await message.reply_text(
            f"❌ You must join our channel to use this bot: @{REQUIRED_CHANNEL}"
        )
        return

    await add_user(user_id, username)
    await add_log(f"User {user_id} used /start")

    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\nClick below to get your YouTube cookie.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Get Cookie", callback_data="get_cookie")]]
        )
    )

@app.on_callback_query(filters.regex("get_cookie"))
async def handle_get_cookie(client, callback_query):
    user = callback_query.from_user
    user_id = user.id
    username = user.username or "NoUsername"

    # Generate dynamic cookie
    cookie = generate_dynamic_cookie(user_id)

    # Save cookie to a temporary file
    file_name = f"{user_id}_cookie.txt"
    file_path = os.path.join("/tmp", file_name)
    with open(file_path, "w") as f:
        f.write(cookie)

    # Send cookie file to user
    await callback_query.message.reply_document(
        document=file_path,
        caption="📝 Here is your YouTube cookie file!"
    )

    # Log to your admin/log channel
    log_text = f"👤 User Info:\nID: {user_id}\nUsername: @{username}\nFirst Name: {user.first_name}\nCookie file sent."
    await client.send_message(LOG_CHANNEL, log_text)

    await callback_query.answer("✅ Cookie sent!")

