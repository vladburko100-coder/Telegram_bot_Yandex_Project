from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from handlers.start import start_bot

router = Router()


@router.callback_query(F.data == 'cancel')
async def cancel_begin(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.clear()
    await start_bot(callback.message, state)