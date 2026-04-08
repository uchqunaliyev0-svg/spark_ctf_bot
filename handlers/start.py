from aiogram import Router, types, F
from aiogram.filters import Command
from database import get_user, add_user, db  # db bu yerda count uchun kerak
from keyboards.main_menu import get_main_menu

router = Router()

# BU YERGA O'ZINGIZNING TELEGRAM ID-NGIZNI YOZING (Screenshotda 1894004823 edi)
ADMIN_ID = 1894004823 

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    user = await get_user(message.from_id)
    if not user:
        await add_user(message.from_id, message.from_user.full_name)
        await message.answer(f"🔥 Salom {message.from_user.first_name}!\nSpark CTF-ga xush kelibsiz. Ro'yxatdan o'tdingiz!")
    
    await message.answer(
        "💻 **Asosiy menyu**\n\nQuyidagi tugmalardan birini tanlang:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@router.message(Command("stat"))
async def show_stat(message: types.Message):
    if message.from_id == ADMIN_ID:
        # Bazadagi foydalanuvchilar sonini olish
        count = await db.fetchval("SELECT COUNT(*) FROM users")
        await message.answer(f"📊 **Bot statistikasi:**\n\nJami foydalanuvchilar: `{count}` ta", parse_mode="Markdown")
    else:
        await message.answer("Siz admin emassiz! ❌")



