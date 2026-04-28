import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import register_routers

load_dotenv()

TOKEN = os.getenv("TOKEN_BOT")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    register_routers(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
