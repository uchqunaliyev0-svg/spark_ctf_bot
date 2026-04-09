from aiogram import Router, types
from aiogram.filters import Command
from database import get_total_users

router = Router()

# SHU YERGA O'ZINGNING ID RAQAMINGNI YOZ:
ADMIN_ID = 12345678 

@router.message(Command("stats"))
async def show_stats(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        total = await get_total_users()
        await message.answer(f"📊 **Spark CTF Statistika**\n\n👤 Jami foydalanuvchilar: {total}", parse_mode="Markdown")
