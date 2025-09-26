"""
inline.py
---------
Inline keyboard helper functions.
"""

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def must_join_keyboard(channel_username: str):
    """
    Return an inline keyboard prompting user to join required channel.
    """
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Join Channel ✅", url=f"https://t.me/{channel_username}")],
            [InlineKeyboardButton("Check Again 🔄", callback_data="check_join")]
        ]
    )

def log_button(log_channel_username: str):
    """
    Inline button linking to log channel (for admin/owner monitoring).
    """
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("View Logs 📊", url=f"https://t.me/{log_channel_username}")]
        ]
    )
