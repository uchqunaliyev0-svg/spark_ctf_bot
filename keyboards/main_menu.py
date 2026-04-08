from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    kb = [
        [KeyboardButton(text="🚩 Tasks")],
        [KeyboardButton(text="👤 Profile"), KeyboardButton(text="🏆 Ranking")],
        [KeyboardButton(text="ℹ️ Info")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
