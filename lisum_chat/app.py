import os

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from redminelib import Redmine
from .config import config

dp = Dispatcher()

redmine = Redmine(config.redmine.url, key=config.redmine.key)

from . import redmine


@dp.message(F.text.as_("message_text"))
async def message_handler(message: types.Message, message_text: str) -> None:
    result_message = await message.answer("⏳✍")
    search_result = redmine.search(message_text).results[0].model_dump_json()
    await result_message.edit_text(search_result, parse_mode=None)


bot = Bot(config.bot.token, parse_mode=ParseMode.HTML)
