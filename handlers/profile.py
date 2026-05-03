from aiogram import F, Router, types
from keyboards.keyboards import come_back, profile_keyboard
from aiogram.fsm.context import FSMContext
from functions.db import db

router = Router()


@router.callback_query(F.data == 'cancel_profile')
@router.callback_query(F.data == 'profile')
async def get_profile(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    user_id = callback.from_user.id
    await callback.message.edit_text(
        f'<b>Профиль</b> @{callback.from_user.username}\n\n'
        f'<b>Ранг:</b> {db.get_rang_user(user_id)}\n'
        f'<b>ELO: </b>{db.get_points(user_id)}\n'
        f'<b>Угаданных мест:</b> {db.get_user_total(user_id)}\n'
        f'              <b>Первый заход:</b> {db.get_date(user_id)}\n',
        reply_markup=profile_keyboard(),
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'top_5')
async def top_players(callback: types.CallbackQuery):
    await callback.answer()
    data = db.get_top_players(5)
    tir_list = ''
    for i, (user, total, rang, points) in enumerate(data, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📌"
        tir_list += f"{medal} <i>{user}</i> — {points} ELO 🎯\n"
    await callback.message.edit_text(
        f'Топ игроков\n\n{tir_list}',
        reply_markup=come_back(),
        parse_mode='HTML'
    )
