from aiogram import Router, types, F
from aiogram.filters import Command
from database import get_user, add_user, count_users
from keyboards.main_menu import get_main_menu

router = Router()

# Admin ID (Sizniki)
ADMIN_ID = 1894004823

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    # Foydalanuvchi ID-sini olishning eng to'g'ri yo'li
    user_id = message.from_user.id
    user = await get_user(user_id)
    
    if not user:
        # Bazaga qo'shishda database.py dagi tartibda (id, ism, univ, lvl) beramiz
        full_name = message.from_user.full_name
        await add_user(user_id, full_name, "Cyber University", "Beginner")
        
        await message.answer(
            f"🚀 **Xush kelibsiz, {message.from_user.first_name}!**\n\n"
            "Siz Spark CTF tizimida muvaffaqiyatli ro'yxatdan o'tdingiz. "
            "Kiber-jang maydoniga tayyormisiz? 🔥",
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            f"Qaytganingiz bilan, **{message.from_user.first_name}**! 👋\n"
            "Sizni yana ko'rib turganimizdan xursandmiz.",
            parse_mode="Markdown"
        )
    
    # Inline menyuni chiqarish
    await message.answer(
        "💻 **Asosiy menyu**\n\nQuyidagi bo'limlardan birini tanlang:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@router.message(Command("stat"))
async def show_stat(message: types.Message):
    # Adminni tekshirish
    if message.from_user.id == ADMIN_ID:
        count = await count_users()
        await message.answer(
            f"📊 **Bot statistikasi**\n\n"
            f"👤 Jami foydalanuvchilar: `{count}` ta\n"
            f"🟢 Holati: Ishchi",
            parse_mode="Markdown"
        )
    else:
        await message.answer("Siz admin emassiz! ❌")
