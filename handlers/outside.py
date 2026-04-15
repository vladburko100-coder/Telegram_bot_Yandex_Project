from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from keyboards.menu import main_menu_kb

router = Router()


@router.message()
async def handle_unknown(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.answer(
            'Сначала выберите режим!',
            reply_markup=main_menu_kb()
        )