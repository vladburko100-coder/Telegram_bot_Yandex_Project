from aiogram import F, Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from functions.yandex_api import search_cords
from functions.weather_api import weather_point

router = Router()


class WeatherStates(StatesGroup):
    waiting_for_location = State()
    waiting_for_forecast_type = State()


@router.message(F.text == 'Погода')
async def weather(message: types.Message, state: FSMContext):
    await state.set_state(WeatherStates.waiting_for_forecast_type)
    await message.answer('Выберите режим:', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Сейчас', callback_data='current')],
        [InlineKeyboardButton(text='Прогноз', callback_data='forecast')]
    ]))


@router.callback_query(WeatherStates.waiting_for_forecast_type, F.data == 'current')
async def current_weather(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        'Введите адрес для текущей погоды:',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='❌ Отмена', callback_data='cancel')]
        ])
    )
    await state.set_state(WeatherStates.waiting_for_location)
    await state.update_data(forecast_type='current')
    await callback.answer()


@router.message(WeatherStates.waiting_for_location)
async def get_weather(message: types.Message, state: FSMContext):
    data = await state.get_data()
    location = message.text
    forecast_type = data.get('forecast_type')
    cords, location = search_cords(location)

    data = weather_point(cords)
    await message.answer(f'<b>Погода в {location}:</b>\n\n'
                         f'<i>Температура:</i> <b>{data.get('температура')}℃</b>\n'
                         f'<i>Давление:</i> <b>{data.get('давление')}мм</b>\n'
                         f'<i>Скорость ветра:</i> <b>{data.get('скорость')}м/с</b>\n'
                         f'<i>Влажность:</i> <b>{data.get('влажность')}%</b>\n',parse_mode='HTML')