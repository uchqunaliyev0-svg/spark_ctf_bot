from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_lang_keyboard():
    kb = [
        [KeyboardButton(text="🇺🇿 O'zbekcha"), KeyboardButton(text="🇷🇺 Русский")],
        [KeyboardButton(text="🇺🇸 English")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)

def get_main_menu(lang):
    texts = {
        "uz": ["🚀 Topshiriqlar", "👤 Profil", "🏆 Reyting", "ℹ️ Ma'lumot"],
        "ru": ["🚀 Задания", "👤 Профиль", "🏆 Рейтинг", "ℹ️ Инфо"],
        "en": ["🚀 Tasks", "👤 Profile", "🏆 Ranking", "ℹ️ Info"]
    }
    t = texts.get(lang, texts["uz"])
    kb = [
        [KeyboardButton(text=t[0])],
        [KeyboardButton(text=t[1]), KeyboardButton(text=t[2])],
        [KeyboardButton(text=t[3])]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
