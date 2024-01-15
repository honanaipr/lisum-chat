from aiogram import Bot
from aiogram.enums import ParseMode
from .config import config

bot = Bot(config.bot.token, parse_mode=ParseMode.HTML)
