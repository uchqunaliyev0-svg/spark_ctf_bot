from aiogram import types
from locales import get_text

def get_main_menu(lang='en'):
    kb = [
        [types.KeyboardButton(text=get_text(lang, "btn_challenges")), types.KeyboardButton(text=get_text(lang, "btn_profile"))],
        [types.KeyboardButton(text=get_text(lang, "btn_ranking")), types.KeyboardButton(text=get_text(lang, "btn_info"))]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
