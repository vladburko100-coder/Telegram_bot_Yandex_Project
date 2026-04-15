from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_type_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Сейчас', callback_data='current')],
        [InlineKeyboardButton(text='Прогноз', callback_data='forecast')],
        [InlineKeyboardButton(text='Вернуться', callback_data='cancel_menu')]
    ])


def get_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вернуться', callback_data='cancel')]
    ])


def get_weather_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='7 дней', callback_data='forecast_7')],
        [InlineKeyboardButton(text='30 дней', callback_data='forecast_30')],
        [InlineKeyboardButton(text='Назад', callback_data='cancel')]
    ])
