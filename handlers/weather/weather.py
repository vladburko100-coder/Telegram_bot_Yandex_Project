from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from functions.yandex_api import search_cords
from functions.weather_api import weather_point_now, weather_point_forecast
from keyboards.keyboards import get_back_keyboard, get_type_keyboard, get_weather_keyboard

router = Router()


class WeatherStates(StatesGroup):
    waiting_for_location = State()
    waiting_for_forecast_type = State()


@router.message(F.text == 'Погода')
async def weather(message: types.Message, state: FSMContext):
    await state.set_state(WeatherStates.waiting_for_forecast_type)
    await message.answer('Выберите режим:', reply_markup=get_type_keyboard())


@router.callback_query(WeatherStates.waiting_for_forecast_type, F.data == 'current')
async def current_weather(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        '<b>Введите адрес для текущей погоды:</b>',
        reply_markup=get_back_keyboard(),
        parse_mode='HTML'
    )
    await state.set_state(WeatherStates.waiting_for_location)
    await state.update_data(forecast_type='current')
    await callback.answer()


@router.callback_query(WeatherStates.waiting_for_forecast_type, F.data == 'forecast')
async def current_weather(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        '<b>Выберите период прогноза погоды:</b>',
        reply_markup=get_weather_keyboard(),
        parse_mode='HTML'
    )
    await callback.answer()


@router.callback_query(F.data == 'forecast_7')
async def forecast_7_days(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        '<b>Введите адрес для прогноза через 7 дней:</b>',
        parse_mode='HTML',
        reply_markup=get_back_keyboard()
    )
    await state.set_state(WeatherStates.waiting_for_location)
    await state.update_data(forecast_type='forecast_7')
    await callback.answer()


@router.callback_query(F.data == 'forecast_30')
async def forecast_7_days(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        '<b>Введите адрес для прогноза через 30 дней:</b>',
        parse_mode='HTML',
        reply_markup=get_back_keyboard()
    )
    await state.set_state(WeatherStates.waiting_for_location)
    await state.update_data(forecast_type='forecast_30')
    await callback.answer()


@router.message(WeatherStates.waiting_for_location)
async def get_weather(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        forecast_type = data.get('forecast_type')
        location = message.text
        cords, location = search_cords(location)
        if forecast_type == "current":
            data = weather_point_now(cords)
        elif forecast_type == 'forecast_7':
            data = weather_point_forecast(cords, 8)
        elif forecast_type == 'forecast_30':
            data = weather_point_forecast(cords, 30)
        await message.answer(f'<b>Погода в {location} на {data.get('дата')}:</b>\n\n'
                             f'<i>Температура:</i> <b>{data.get('температура')}℃</b>\n'
                             f'<i>Давление:</i> <b>{data.get('давление')}мм</b>\n'
                             f'<i>Скорость ветра:</i> <b>{data.get('скорость')}м/с</b>\n'
                             f'<i>Влажность:</i> <b>{data.get('влажность')}%</b>\n', parse_mode='HTML',
                             reply_markup=get_back_keyboard()
                             )
    except IndexError:
        await message.answer('Адрес не найден...\nПопробуйте снова!')


@router.callback_query(F.data == 'cancel')
async def cancel_weather(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        '<b>Поиск погоды отменен</b>\n\nВыберите действие:',
        parse_mode='HTML',
        reply_markup=get_type_keyboard()
    )
    await state.set_state(WeatherStates.waiting_for_forecast_type)
    await callback.answer()
