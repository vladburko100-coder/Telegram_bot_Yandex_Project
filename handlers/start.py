from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.menu import main_menu_kb

router = Router()


@router.message(Command('start'))
async def start_bot(message: types.Message, state: FSMContext):
    await state.clear()

    welcome_text = (
        f"Привет, я API бот!"
    )
    await message.answer(
        welcome_text,
        reply_markup=main_menu_kb()
    )