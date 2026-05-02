from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⏪', callback_data='cancel')]
    ])


def get_back_mode():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⏪', callback_data='play')]
    ])


def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Играть 👾', callback_data='play')],
        [InlineKeyboardButton(text='Профиль 🙎🏻‍♂️', callback_data='profile')]
    ])


def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Страны', callback_data='search_country')],
        [InlineKeyboardButton(text='Города', callback_data='search_city')],
        [InlineKeyboardButton(text='⏪', callback_data='cancel')]
    ])


def profile_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔝', callback_data='top_5'),
         InlineKeyboardButton(text='⏪', callback_data='cancel')]
    ])


def come_back():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⏪', callback_data='cancel_profile')]
    ])


def continue_or_come_back():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Повторить 🔄', callback_data='continue_game')],
        [InlineKeyboardButton(text='Следующее ➡', callback_data='next_game')],
        [InlineKeyboardButton(text='⏪', callback_data='cancel')]
    ])


def continue_game_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Следующее ➡', callback_data='next_game')],
        [InlineKeyboardButton(text='⏪', callback_data='cancel')]
    ])


def get_help():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Помощь', callback_data='help')],
        [InlineKeyboardButton(text='Сдаться', callback_data='give_up')]
    ])
