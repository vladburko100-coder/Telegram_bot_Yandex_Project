from aiogram import Dispatcher
from handlers.start import router as start_router
from handlers.maps import router as static_router
from handlers.outside import router as outside_router
from handlers.weather.weather import router as weather_router
from handlers.cancel_menu import router as cancel_router


def register_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(static_router)
    dp.include_router(weather_router)
    dp.include_router(cancel_router)
    dp.include_router(outside_router)
