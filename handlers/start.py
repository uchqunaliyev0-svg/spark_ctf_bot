from aiogram import Router, types, F
from aiogram.filters import Command
from database import get_user, add_user, count_users  # db o'rniga count_users keldi
from keyboards.main_menu import get_main_menu

router = Router()

# Admin ID (Sizniki)
ADMIN_ID = 1894004823

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    user = await get_user(message.from_id)
    if not user:
        # Yangi foydalanuvchini bazaga qo'shish (ism, univ, daraja so'rash qismini keyinroq murakkablashtiramiz)
        # Hozircha xato bermasligi uchun default qiymatlar bilan qo'shamiz
        await add_user(message.from_id, message.from_user.full_name, "Noma'lum", "Beginner")
        await message.answer(f"🔥 Salom {message.from_user.first_name}!\nSpark CTF-ga xush kelibsiz. Ro'yxatdan o'tdingiz!")
    
    await message.answer(
        "💻 **Asosiy menyu**\n\nQuyidagi tugmalardan birini tanlang:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@router.message(Command("stat"))
async def show_stat(message: types.Message):
    if message.from_id == ADMIN_ID:
        # count_users() funksiyasini chaqiramiz
        count = await count_users()
        await message.answer(f"📊 **Bot statistikasi:**\n\nJami foydalanuvchilar: `{count}` ta", parse_mode="Markdown")
    else:
        await message.answer("Siz admin emassiz! ❌")
