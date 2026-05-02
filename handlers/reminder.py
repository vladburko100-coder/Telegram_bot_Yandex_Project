import asyncio
import aioschedule
from aiogram import Bot


async def send_reminder(bot: Bot):
    from functions.db import db

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
    aioschedule.every(7).days.do(send_reminder, bot)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)