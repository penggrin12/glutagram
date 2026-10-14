import sys

from aioe621 import Auth
from aioe621.client import Client
from aiogram import Bot

from glutagram.config import secrets, config

if "PLEASE_ENTER_YOUR_USERNAME_HERE" in config.e621_user_agent:
    sys.exit("Please provide a proper way to reach you in the user agent located in config.json.")

bot = Bot(secrets.telegram_bot_token.get_secret_value())
e621 = Client(
    user_agent=config.e621_user_agent,
    auth=(
        Auth(username=secrets.e621_auth_username, api_key=secrets.e621_auth_api_key.get_secret_value())
        if secrets.e621_auth_username else None
    ),
)
