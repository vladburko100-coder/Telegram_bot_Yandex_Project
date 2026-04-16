from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton


def get_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вернуться', callback_data='cancel')]
    ])


def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Играть', callback_data='play')],
        [InlineKeyboardButton(text='Профиль', callback_data='profile')]
    ])


def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да!', callback_data='starting'),
         InlineKeyboardButton(text='Вернуться', callback_data='cancel')]
    ])


def profile_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Топ 5', callback_data='top_5'),
         InlineKeyboardButton(text='Вернуться', callback_data='cancel')]
    ])


def come_back():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вернуться', callback_data='cancel_profile')]
    ])
