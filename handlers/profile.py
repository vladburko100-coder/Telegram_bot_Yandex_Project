from aiogram import F, Router, types
from keyboards.keyboards import come_back, profile_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from functions.db import get_user_total, get_top_players
from tabulate import tabulate

router = Router()


class States(StatesGroup):
    get_back = State()


@router.callback_query(F.data == 'cancel_profile')
@router.callback_query(F.data == 'profile')
async def get_profile(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        f'Профиль\n\n@{callback.from_user.username}\nУгаданных мест: {get_user_total(callback.from_user.id)}',
        reply_markup=profile_keyboard()
    )


@router.callback_query(F.data == 'top_5')
async def top_players(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = get_top_players()
    tir_list = ''
    for i, (user, total) in enumerate(data, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📌"
        tir_list += f"{medal} <b>{i}.</b>  <i>{user}</i> — <b>{total}</b> 🎯\n"
    await callback.message.edit_text(
        f'Топ игроков\n\n{tir_list}',
        reply_markup=come_back(),
        parse_mode='HTML'
    )
    await state.set_state(States.get_back)
