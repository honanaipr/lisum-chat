from lisum_chat.bot import bot
from lisum_chat.dispatcher import dp
from lisum_chat.database import engine
from lisum_chat.models import Base
import asyncio
import logging
import sys


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    Base.metadata.create_all(engine)
    asyncio.run(main())
