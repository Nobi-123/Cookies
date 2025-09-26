from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Modules.config import BOT_TOKEN, REQUIRED_CHANNEL
from Modules.utils.cookies_gen import generate_dynamic_cookie
import os

app = Client("YouTubeCookiesBot", bot_token=BOT_TOKEN)
LOG_CHANNEL = -1003065367480  # your logging channel ID

async def check_must_join(client, user_id):
    try:
        member = await client.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"

    if not await check_must_join(client, user_id):
        await message.reply_text(
            f"❌ You must join our channel to use this bot: @{REQUIRED_CHANNEL}"
        )
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
    username = user.username or "NoUsername"

    # Generate cookie string
    cookie_str = generate_dynamic_cookie(user_id)

    # Save cookie to a temporary file
    file_name = f"{user_id}_cookie.txt"
    output_file = os.path.join("/tmp", file_name)  # Heroku allows writing to /tmp
    with open(output_file, "w") as f:
        f.write(cookie_str)

    # Send the cookie file to the user
    await client.send_document(
        chat_id=user_id,
        document=output_file,
        caption="📝 Here is your YouTube cookies file."
    )

    # Log user info to LOG_CHANNEL
    log_text = (
        f"👤 User Info:\n"
        f"ID: {user_id}\nUsername: @{username}\nFirst Name: {user.first_name}\n"
    )
    await client.send_message(LOG_CHANNEL, log_text)

    # Acknowledge callback
    await callback_query.answer("✅ Cookie file sent!")

if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
