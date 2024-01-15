from lisum_chat.bot import bot
from lisum_chat.dispatcher import dp
import asyncio
import logging
import sys


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
