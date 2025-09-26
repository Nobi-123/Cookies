"""
helpers.py
----------
Utility functions for YouTubeCookiesBot.
"""

import random
import string
from Modules.utils.database import add_user, add_cookie

async def save_user_and_cookie(user_id: int, username: str, cookie: str):
    """
    Save user info and their generated cookie in the database.
    """
    await add_user(user_id, username)
    await add_cookie(user_id, cookie)

def generate_random_cookie_token(length: int = 16) -> str:
    """
    Generate a random token to append to cookies for uniqueness.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
