from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from handlers.start import start_bot

router = Router()


@router.callback_query(F.data == 'cancel_menu')
async def cancel_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()

    await start_bot(callback.message, state)
    await callback.answer()
