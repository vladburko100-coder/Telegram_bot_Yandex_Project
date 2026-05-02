import asyncio
import os
import aioschedule
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
from handlers import register_routers
from handlers.reminder import scheduler

load_dotenv()

TOKEN = os.getenv("TOKEN_BOT")
PROXY_URL = os.getenv("PROXY_URL")


async def main():
    session = AiohttpSession(proxy=PROXY_URL)
    bot = Bot(token=TOKEN, session=session)
    dp = Dispatcher()

    scheduler_task = asyncio.create_task(scheduler(bot))
    register_routers(dp)

    await asyncio.gather(scheduler_task, dp.start_polling(bot))


if __name__ == '__main__':
    asyncio.run(main())
