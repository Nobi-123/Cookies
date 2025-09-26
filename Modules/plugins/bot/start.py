from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from io import BytesIO
from Modules.config import BOT_TOKEN, REQUIRED_CHANNEL, LOG_CHANNEL
from Modules.utils.cookies_gen import generate_dynamic_cookie

app = Client("YouTubeCookiesBot", bot_token=BOT_TOKEN)

async def check_must_join(client, user_id):
    try:
        member = await client.get_chat_member(REQUIRED_CHANNEL, user_id)
        if member.status in ["member", "creator", "administrator"]:
            return True
        return False
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

    # Generate cookie string dynamically
    cookie_text = generate_dynamic_cookie(user.id)

    # Convert to in-memory file
    cookie_file = BytesIO(cookie_text.encode("utf-8"))

    # Send cookie file to user
    await client.send_document(
        chat_id=user.id,
        document=cookie_file,
        file_name="cookies.txt",
        caption="✅ Here is your YouTube cookie file."
    )

    # Log the user action
    log_text = (
        f"👤 Sent cookies to:\n"
        f"ID: {user.id}\n"
        f"Username: @{user.username or 'NoUsername'}\n"
        f"First Name: {user.first_name}"
    )
    await client.send_message(LOG_CHANNEL, log_text)

    # Acknowledge callback
    await callback_query.answer("✅ Cookie file sent!")

if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
