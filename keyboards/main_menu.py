from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_lang_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_main_menu(lang):
    texts = {
        "uz": ["🚀 Topshiriqlar", "👤 Profil", "🏆 Reyting", "ℹ️ Ma'lumot"],
        "ru": ["🚀 Задания", "👤 Профиль", "🏆 Рейтинг", "ℹ️ Инфо"],
        "en": ["🚀 Tasks", "👤 Profile", "🏆 Ranking", "ℹ️ Info"]
    }
    t = texts[lang]
    buttons = [
        [InlineKeyboardButton(text=t[0], callback_data="tasks")],
        [InlineKeyboardButton(text=t[1], callback_data="profile"),
         InlineKeyboardButton(text=t[2], callback_data="ranking")],
        [InlineKeyboardButton(text=t[3], callback_data="about")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)o

