
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Modules.config import BOT_TOKEN, REQUIRED_CHANNEL
from Modules.utils.cookies_gen import generate_dynamic_cookie

app = Client("YouTubeCookiesBot", bot_token=BOT_TOKEN)
LOG_CHANNEL = -1003065367480

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
        await message.reply_text(f"❌ You must join our channel to use this bot: @{REQUIRED_CHANNEL}")
        return
    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\nClick below to get your YouTube cookie.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Get Cookie", callback_data="get_cookie")]])
    )

@app.on_callback_query(filters.regex("get_cookie"))
async def send_cookie(client, callback_query):
    user = callback_query.from_user
    user_id = user.id
    username = user.username or "NoUsername"
    cookie = generate_dynamic_cookie(user_id)
    await callback_query.message.reply_text(f"📝 Your YouTube cookie:\n\n`{cookie}`", parse_mode="markdown")
    log_text = f"👤 User Info:\nID: {user_id}\nUsername: @{username}\nFirst Name: {user.first_name}\n"
    await client.send_message(LOG_CHANNEL, log_text)
    await callback_query.answer("✅ Cookie sent!")

if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
