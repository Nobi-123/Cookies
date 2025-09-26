"""
database.py
-----------
Async MongoDB helper functions for YouTubeCookiesBot.
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from Modules.config import DEBUG

# -------------------------
# MongoDB Connection
# -------------------------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "YouTubeCookiesBot")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# -------------------------
# Collections
# -------------------------
users_collection = db.get_collection("users")          # store user info
cookies_collection = db.get_collection("cookies")      # store generated cookies
logs_collection = db.get_collection("logs")            # store bot logs

# -------------------------
# Async helper functions
# -------------------------

async def add_user(user_id: int, username: str = None):
    """Add a user to the database if not exists."""
    user = await users_collection.find_one({"user_id": user_id})
    if not user:
        await users_collection.insert_one({
            "user_id": user_id,
            "username": username,
        })
        if DEBUG:
            print(f"[DB] Added user {user_id} ({username})")

async def add_cookie(user_id: int, cookie: str):
    """Save generated cookie linked to a user."""
    await cookies_collection.insert_one({
        "user_id": user_id,
        "cookie": cookie,
    })
    if DEBUG:
        print(f"[DB] Saved cookie for user {user_id}")

async def add_log(message: str):
    """Save bot log message."""
    await logs_collection.insert_one({
        "message": message,
    })
    if DEBUG:
        print(f"[DB] Log: {message}")

async def get_user_cookies(user_id: int):
    """Retrieve all cookies for a given user."""
    cursor = cookies_collection.find({"user_id": user_id})
    return [doc async for doc in cursor]

async def get_all_users():
    """Retrieve all users."""
    cursor = users_collection.find()
    return [doc async for doc in cursor]
