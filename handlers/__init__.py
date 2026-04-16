from aiogram import Dispatcher
from handlers.start import router as start_router
from handlers.maps import router as static_router
from handlers.profile import router as profile_router
from handlers.cancel import router as cancel_router


def register_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(static_router)
    dp.include_router(profile_router)
    dp.include_router(cancel_router)
