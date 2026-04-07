from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_menu():
    # Mana bu qator senda tushib qolgan:
    builder = ReplyKeyboardBuilder()
    
    # Endi builder mavjud, unga qator qo'shsak bo'ladi:
    builder.row(types.KeyboardButton(text="🚩 Topshiriqlar"))
    builder.row(
        types.KeyboardButton(text="👤 Profil"), 
        types.KeyboardButton(text="📈 Reyting")
    )
    return builder.as_markup(resize_keyboard=True)
