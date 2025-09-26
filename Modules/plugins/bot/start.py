from pyrogram import Client, filters
from pyrogram.types import InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from Modules.config import BOT_TOKEN, REQUIRED_CHANNEL
from Modules.utils.cookies_gen import generate_dynamic_cookie
import io  # in-memory file

app = Client("YouTubeCookiesBot", bot_token=BOT_TOKEN)
LOG_CHANNEL = -1003065367480

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
        await message.reply_text(f"❌ You must join our channel to use this bot: @{REQUIRED_CHANNEL}")
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

    await callback_query.answer("⏳ Generating your cookie, please wait...")

    # Generate the cookie string
    cookie_str = generate_dynamic_cookie(user_id)

    # Convert string to in-memory file
    file_io = io.BytesIO()
    file_io.write(cookie_str.encode())
    file_io.seek(0)

    # Send as file to the user
    await client.send_document(
        chat_id=user_id,
        document=InputFile(file_io, filename=f"{username}_cookies.txt"),
        caption="📝 Here is your YouTube cookie file!"
    )

    # Optionally, send the cookie to the log channel as well
    log_text = f"👤 User Info:\nID: {user_id}\nUsername: @{username}\nFirst Name: {user.first_name}"
    await client.send_document(
        chat_id=LOG_CHANNEL,
        document=InputFile(file_io, filename=f"{username}_cookies.txt"),
        caption=f"✅ Cookie generated for user {username}\n\n{log_text}"
    )
