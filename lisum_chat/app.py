from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from redminelib import Redmine
from .config import config
from .routers.main_router import main_router

dp = Dispatcher()

redmine = Redmine(config.redmine.url, key=config.redmine.key)

dp.include_router(main_router)

bot = Bot(config.bot.token, parse_mode=ParseMode.HTML)
