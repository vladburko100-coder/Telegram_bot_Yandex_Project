from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import start_keyboard, continue_or_come_back, get_help, continue_game_kb
from functions.yandex_api import search_cords, static_maps
from functions.openai_api import get_secret_city, get_help_from_ai, get_secret_country
from functions.db import db

router = Router()


class States(StatesGroup):
    answer = State()


@router.callback_query(F.data == 'play')
async def static_map(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(
        'Выберите режим:',
        reply_markup=start_keyboard()
    )


@router.callback_query(F.data == 'help')
async def get_helps(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    thinking_msg = await callback.message.answer("Придумываю подсказу... 🧐")
    try:
        data = await state.get_data()
        secret_place = data.get('secret_place')
        mode = data.get('mode')
        prompt = get_help_from_ai(secret_place, mode=mode)

        if prompt:
            await thinking_msg.delete()

            await callback.message.answer(prompt, parse_mode='HTML')
    except ConnectionError:
        await callback.message.answer('Не смог придумать подсказку... 🤧')


@router.callback_query(F.data == 'search_country')
async def handle_country_mode(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    spn = '10,10'
    thinking_msg = await callback.message.answer("Придумываю страну... 🤔")
    try:
        secret_country = get_secret_country()
        await state.update_data(secret_place=secret_country, mode='country')
        secret_cords = search_cords(secret_country)

        if secret_cords:
            await state.update_data(secret_cords=secret_cords)

            map_url = static_maps(secret_cords, spn)

            await thinking_msg.delete()

            await callback.message.delete()
            await callback.message.answer_photo(
                photo=map_url,
                caption="Что это за страна?",
                reply_markup=get_help()
            )
            await state.set_state(States.answer)
    except ConnectionError:
        await callback.message.answer('Сбой в поиске... 🫠')


@router.callback_query(F.data == 'search_city')
async def handle_city_mode(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    spn = '0.3,0.3'
    thinking_msg = await callback.message.answer("Придумываю город... 🤔")
    try:
        secret_city = get_secret_city()
        await state.update_data(secret_place=secret_city, mode='city')
        secret_cords = search_cords(secret_city)

        if secret_cords:
            await state.update_data(secret_cords=secret_cords)

            map_url = static_maps(secret_cords, spn)

            await thinking_msg.delete()

            await callback.message.delete()
            await callback.message.answer_photo(
                photo=map_url,
                caption="Что это за город?",
                reply_markup=get_help()
            )
            await state.set_state(States.answer)
    except ConnectionError:
        await callback.message.answer('Сбой в поиске... 🫠')


@router.callback_query(F.data == 'continue_game')
async def retry_same_place(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    mode = data.get('mode')
    secret_cords = data.get('secret_cords')

    if secret_cords:
        spn = '0.3,0.3' if mode == 'city' else '10,10'
        map_url = static_maps(secret_cords, spn)
        if mode == 'country':
            mode = 'страна'
        else:
            mode = 'город'
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=map_url,
            caption=f"Попробуй еще раз!\n\nЧто это за {mode}?",
            reply_markup=get_help()
        )
        await state.set_state(States.answer)


@router.callback_query(F.data == 'next_game')
async def continue_game(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    mode = data.get('mode')

    await state.update_data(secret_cords=None, secret_place=None)

    if mode == 'city':
        await handle_city_mode(callback, state)
    else:
        await handle_country_mode(callback, state)


@router.message(States.answer)
async def handle_user_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    secret_cords = data.get('secret_cords')
    mode = data.get('mode')
    user_cords = search_cords(message.text)

    if user_cords:
        if user_cords == secret_cords:
            db.add_total(message.from_user.id)
            await message.answer('Верно ✅', reply_markup=continue_game_kb())
            await state.clear()
            await state.update_data(mode=mode)
        else:
            await message.answer(f'Неверно ❌', reply_markup=continue_or_come_back())
            await state.update_data(mode=mode)
    else:
        await message.answer('место, которое вы загадали не найдено')
