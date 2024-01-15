from aiogram import Dispatcher
from .routers.main_router import main_router

dp = Dispatcher()

dp.include_router(main_router)
