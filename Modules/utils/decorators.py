"""
decorators.py
-------------
Common decorators for YouTubeCookiesBot.
"""

from functools import wraps
from pyrogram.types import Message
from Modules.config import REQUIRED_CHANNEL
from Modules.utils.database import add_log
from pyrogram.errors import UserNotParticipant

def must_join(func):
    """
    Decorator to check if the user has joined the REQUIRED_CHANNEL.
    """
    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        try:
            member = await client.get_chat_member(REQUIRED_CHANNEL, message.from_user.id)
            if member.status not in ("member", "administrator", "creator"):
                await message.reply_text(f"❌ You must join @{REQUIRED_CHANNEL} to use this bot!")
                return
        except UserNotParticipant:
            await message.reply_text(f"❌ You must join @{REQUIRED_CHANNEL} to use this bot!")
            return
        # log user action
        await add_log(f"User {message.from_user.id} used command {message.text}")
        return await func(client, message, *args, **kwargs)
    return wrapper
