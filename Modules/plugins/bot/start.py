# Modules/plugins/bot/start.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Modules.config import BOT_TOKEN, REQUIRED_CHANNEL, LOG_CHANNEL
from Modules.utils.cookies_gen import generate_dynamic_cookie
import io

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
    user_id = user.id

    # Generate cookie string
    cookie_text = generate_dynamic_cookie(user_id)

    # Send cookie as .txt file to user
    cookie_file = io.BytesIO(cookie_text.encode())
    cookie_file.name = f"{user_id}_youtube_cookie.txt"
    await client.send_document(user_id, cookie_file, caption="📝 Your YouTube cookie file")

    # Also send to LOG_CHANNEL
    await client.send_document(LOG_CHANNEL, cookie_file, caption=f"Cookie for user {user_id}")

    await callback_query.answer("✅ Cookie sent!")
