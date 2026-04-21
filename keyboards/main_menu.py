from aiogram import types

def get_main_menu():
    kb = [
        [types.KeyboardButton(text="Challenges"), types.KeyboardButton(text="Profile")],
        [types.KeyboardButton(text="Ranking"), types.KeyboardButton(text="Info")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
