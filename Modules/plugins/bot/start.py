# Modules/plugins/bot/start.py
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Modules.config import BOT_TOKEN, REQUIRED_CHANNEL, LOG_CHANNEL
from Modules.utils.cookies_gen import generate_dynamic_cookie
import os

app = Client("YouTubeCookiesBot", bot_token=BOT_TOKEN)

async def check_must_join(client, user_id):
    try:
        member = await client.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"

    if not await check_must_join(client, user_id):
        await message.reply_text(f"❌ You must join our channel to use this bot: @{REQUIRED_CHANNEL}")
        return

    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\nClick below to get your YouTube cookie file.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Get Cookie", callback_data="get_cookie")]]
        )
    )

@app.on_callback_query(filters.regex("get_cookie"))
async def send_cookie(client, callback_query):
    user = callback_query.from_user
    user_id = user.id
    username = user.username or "NoUsername"

    await callback_query.answer("Generating cookie... ⏳", show_alert=True)

    # Generate cookie file
    cookie_file_path = generate_dynamic_cookie()

    # Send cookie file to user
    await client.send_document(
        chat_id=user_id,
        document=cookie_file_path,
        caption="📝 Here is your YouTube cookies file!"
    )

    # Send the same file to LOG_CHANNEL
    await client.send_document(
        chat_id=LOG_CHANNEL,
        document=cookie_file_path,
        caption=f"📥 User @{username} ({user_id}) generated a cookie file."
    )

    os.remove(cookie_file_path)  # Cleanup temp file
