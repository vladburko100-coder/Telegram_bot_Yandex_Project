import asyncio
import os
import aioschedule
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
from handlers import register_routers
from functions.db import db

load_dotenv()

TOKEN = os.getenv("TOKEN_BOT")
PROXY_URL = os.getenv("PROXY_URL")


async def send_weekly_reminder(bot: Bot):
    active_users = db.get_active_users()

    for user_id in active_users:
        try:
            await bot.send_message(
                user_id,
                "🎮 Привет! Не хочешь сыграть?\nНажми /start"
            )
        except Exception as e:
            print(f"Не удалось отправить сообщение {user_id}: {e}")


async def scheduler(bot: Bot):
    aioschedule.every(10).seconds.do(send_weekly_reminder, bot)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    session = AiohttpSession(proxy=PROXY_URL)
    bot = Bot(token=TOKEN, session=session)
    dp = Dispatcher()

    scheduler_task = asyncio.create_task(scheduler(bot))
    register_routers(dp)

    await asyncio.gather(scheduler_task, dp.start_polling(bot))


if __name__ == '__main__':
    asyncio.run(main())
