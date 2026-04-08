from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    buttons = [
        [InlineKeyboardButton(text="🚀 Topshiriqlar", callback_data="tasks")],
        [InlineKeyboardButton(text="👤 Profil", callback_data="profile"),
         InlineKeyboardButton(text="🏆 Reyting", callback_data="ranking")],
        [InlineKeyboardButton(text="ℹ️ Biz haqimizda", callback_data="about")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
