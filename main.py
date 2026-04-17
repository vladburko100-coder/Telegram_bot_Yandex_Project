import asyncio
import os
from aiogram import Bot, Dispatcher
from handlers import register_routers
from dotenv import load_dotenv
from functions.db import create_database

load_dotenv()

TOKEN = os.getenv("TOKEN_BOT")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    register_routers(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    create_database()
    asyncio.run(main())
