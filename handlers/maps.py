import sqlite3
from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import start_keyboard
from functions.yandex_api import search_cords, static_maps
from functions.db import add_total

router = Router()


class States(StatesGroup):
    answer = State()


@router.callback_query(F.data == 'play')
async def static_map(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        'Начнем игру?',
        reply_markup=start_keyboard()
    )


@router.callback_query(F.data == 'starting')
async def handle_starting_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    thinking_msg = await callback.message.answer("Думаю над местом...")

    secret_cords = search_cords('59.732489,+30.474645')
    if secret_cords:
        await state.update_data(secret_cords=secret_cords)
        map_url = static_maps(secret_cords)

        await thinking_msg.delete()

        await callback.message.delete()
        await callback.message.answer_photo(
            photo=map_url,
            caption="Что это за место?"
        )
        await state.set_state(States.answer)


@router.message(States.answer)
async def handle_user_answer(message: types.Message, state: FSMContext):
    user_cords = message.text

    data = await state.get_data()
    secret_cords = data.get('secret_cords')

    user_cords = search_cords(user_cords)
    if user_cords:
        if user_cords == secret_cords:
            add_total(message.from_user.id)
            await message.answer('ВЕРНО!!')
        else:
            await message.answer('Неверно(((')
    else:
        await message.answer('место, которое вы загадали не найдено')
