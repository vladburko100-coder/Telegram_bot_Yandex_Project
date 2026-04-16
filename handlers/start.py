from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import main_menu_kb
from functions.db import add_user

router = Router()


@router.message(Command('start'))
async def start_bot(message: types.Message, state: FSMContext):
    await state.clear()
    add_user(message.from_user.id, message.from_user.username)
    await message.answer(
        f"Привет, я Geoguessr бот!",
        reply_markup=main_menu_kb()
    )