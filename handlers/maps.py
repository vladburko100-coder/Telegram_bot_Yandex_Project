import sqlite3
from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import start_keyboard, continue_or_come_back, get_help
from functions.yandex_api import search_cords, static_maps
from functions.openai_api import get_secret_city, get_help_from_ai
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


@router.callback_query(F.data == 'help')
async def get_helps(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    thinking_msg = await callback.message.answer("Придумываю подсказу...")
    try:
        data = await state.get_data()
        secret_city = data.get('secret_city')
        prompt = get_help_from_ai(secret_city)
        if prompt:
            await thinking_msg.delete()

            await callback.message.answer(prompt)
    except ConnectionError:
        await callback.message.answer('Не смог придумать подсказку...')


@router.callback_query(F.data == 'starting')
async def handle_starting_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    thinking_msg = await callback.message.answer("Придумываю место...")
    try:
        secret_city = get_secret_city()
        await state.update_data(secret_city=secret_city)
        secret_cords = search_cords(secret_city)
        if secret_cords:
            await state.update_data(secret_cords=secret_cords)
            map_url = static_maps(secret_cords)

            await thinking_msg.delete()

            await callback.message.delete()
            await callback.message.answer_photo(
                photo=map_url,
                caption="Что это за место?",
                reply_markup=get_help()
            )
            await state.set_state(States.answer)
    except ConnectionError:
        await callback.message.answer('Сбой в поиске')


@router.message(States.answer)
async def handle_user_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    secret_cords = data.get('secret_cords')
    user_cords = search_cords(message.text)

    if user_cords:
        if user_cords == secret_cords:
            add_total(message.from_user.id)
            await message.answer('ВЕРНО!!', reply_markup=continue_or_come_back())
            await state.clear()
        else:
            await message.answer(f'Неверно(((\n{secret_cords}', reply_markup=continue_or_come_back())
    else:
        await message.answer('место, которое вы загадали не найдено')
