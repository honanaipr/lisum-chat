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

from .routers.main_router import main_router

dp.include_router(main_router)

bot = Bot(config.bot.token, parse_mode=ParseMode.HTML)
