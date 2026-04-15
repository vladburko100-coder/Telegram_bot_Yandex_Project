import asyncio
from aiogram import Bot, Dispatcher
from handlers.register_routers import register_routers

TOKEN = '8708989854:AAErwQMCfkZ-mu6tRkBnVPR-Gm1DvQektWY'


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    register_routers(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
