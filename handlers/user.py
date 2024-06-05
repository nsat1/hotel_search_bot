from datetime import datetime
from aiogram import Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from fluentogram import TranslatorRunner

from models.users import User
from db.base_repository import BaseRepository

users = BaseRepository(User)

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, i18n: TranslatorRunner):
    username = html.quote(message.from_user.full_name)
    user_id = message.from_user.id

    existing_user = await users.get(user_id)

    if not existing_user:
        new_user_data = {
            "id": user_id,
            "fullname": message.from_user.full_name,
            "username": message.from_user.username,
            "created_at": datetime.now(),
            "language_code": message.from_user.language_code
        }
        await users.create(**new_user_data)

    await message.answer(text=i18n.description(username=username))


@user_router.message(Command(commands=["help"]))
async def user_help(message: Message, i18n: TranslatorRunner):
    help_text = i18n.help()
    await message.answer(text=help_text)
