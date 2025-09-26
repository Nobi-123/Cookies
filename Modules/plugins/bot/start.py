# Modules/plugins/bot/start.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Modules.config import BOT_TOKEN, REQUIRED_CHANNEL, LOG_CHANNEL
import io
from Modules.utils.cookies_gen import generate_dynamic_cookie, get_cookie_file_bytes
from pyrogram.types import InputFile

app = Client("YouTubeCookiesBot", bot_token=BOT_TOKEN)

async def check_must_join(client, user_id):
    try:
        member = await client.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_id = message.from_user.id
    if not await check_must_join(client, user_id):
        await message.reply_text(f"❌ You must join @{REQUIRED_CHANNEL} to use this bot.")
        return

    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\nClick below to get your YouTube cookie.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Get Cookie", callback_data="get_cookie")]]
        )
    )


@app.on_callback_query(filters.regex("get_cookie"))
async def send_cookie(client, callback_query):
    user = callback_query.from_user

    # Generate cookies dynamically
    cookie_text = generate_dynamic_cookie()
    cookie_file = get_cookie_file_bytes(cookie_text)

    # Send as file to user
    await client.send_document(
        chat_id=user.id,
        document=InputFile(cookie_file, filename="youtube_cookies.txt"),
        caption="✅ Here is your YouTube cookie file."
    )

    # Optionally log
    await client.send_message(LOG_CHANNEL,
        f"👤 Sent cookies to {user.first_name} (@{user.username or 'NoUsername'})"
    )

    await callback_query.answer("✅ Cookie file sent!")

