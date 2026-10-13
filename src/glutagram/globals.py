from aioe621 import Auth
from aioe621.client import Client
from aiogram import Bot

from glutagram.config import secrets, config

bot = Bot(secrets.telegram_bot_token.get_secret_value())
e621 = Client(
    user_agent=config.e621_user_agent,
    auth=(
        Auth(username=secrets.e621_auth_username, api_key=secrets.e621_auth_api_key.get_secret_value())
        if secrets.e621_auth_username else None
    ),
)
