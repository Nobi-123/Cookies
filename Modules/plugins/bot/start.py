import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from Modules.config import BOT_TOKEN, REQUIRED_CHANNEL
from Modules.utils.default_cookies import get_default_cookie

app = Client("YouTubeCookiesBot", bot_token=BOT_TOKEN)
LOG_CHANNEL = -1003065367480  # Replace with your actual log channel ID

async def check_must_join(client, user_id):
    """Check if the user has joined the required channel."""
    try:
        member = await client.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    first_name = message.from_user.first_name

    if not await check_must_join(client, user_id):
        await message.reply_text(
            f"❌ You must join our channel to use this bot: @{REQUIRED_CHANNEL}"
        )
        return

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Get Cookie", callback_data="get_cookie")]]
    )
    await message.reply_text(
        f"👋 Hello {first_name}!\nClick below to get your YouTube cookie.",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("get_cookie"))
async def send_cookie(client, callback_query):
    user = callback_query.from_user
    user_id = user.id
    username = user.username or "NoUsername"

    # Get default cookie
    cookie = get_default_cookie()

    # Save cookie to a temporary .txt file
    cookie_filename = f"{user_id}_youtube_cookie.txt"
    file_path = os.path.join("/tmp", cookie_filename)  # /tmp works on Heroku
    with open(file_path, "w") as f:
        f.write(cookie)

    # Send the cookie file to the user
    await callback_query.message.reply_document(
        document=InputFile(file_path),
        caption="📝 Here is your YouTube cookie file!"
    )

    # Log the action to LOG_CHANNEL
    log_text = (
        f"👤 User Info:\n"
        f"ID: {user_id}\n"
        f"Username: @{username}\n"
        f"First Name: {user.first_name}\n"
        f"Sent cookie file: {cookie_filename}"
    )
    await client.send_message(LOG_CHANNEL, log_text)

    # Acknowledge callback
    await callback_query.answer("✅ Cookie file sent!")

    # Delete temporary file
    os.remove(file_path)

if __name__ == "__main__":
    print("YouTubeCookiesBot is starting...")
    app.run()
