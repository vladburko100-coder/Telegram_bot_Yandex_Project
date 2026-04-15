from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards.menu import main_menu_kb
from functions.yandex_api import search_cords, static_maps
from keyboards.keyboards import get_back_keyboard

router = Router()


class MapStates(StatesGroup):
    waiting_for_address = State()


@router.message(F.text == 'Карты')
async def static_map(message: types.Message, state: FSMContext):
    await state.set_state(MapStates.waiting_for_address)
    await message.answer(
        'Введи топоним, а я покажу его на карте',
        reply_markup=main_menu_kb()
    )


@router.message(MapStates.waiting_for_address)
async def get_address(message: types.Message, state: FSMContext):
    try:
        cords, address = search_cords(message.text)
        map_url = static_maps(cords)
        await message.answer_photo(
            photo=map_url, caption=f"<i>{address}</i>\n\n"
                                   f"<i>Координаты: </i>{cords[0]}, {cords[1]}", parse_mode='HTML',reply_markup=types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [types.InlineKeyboardButton(text='Ссылка на объект', url=map_url)],
                        [InlineKeyboardButton(text='Вернуться', callback_data='cancel_menu')]
                    ]
                )
            )
    except IndexError:
        await message.answer('Объект не найден...\nПопробуйте снова!')