import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Handlerlarni import qilish (fayllaring nomiga qarab tekshirib ol)
from handlers import start, profile, tasks, ranking, info, admin
from database import init_db

# Loglarni sozlash (xatolarni terminalda ko'rish uchun)
logging.basicConfig(level=logging.INFO)

async def main():
    # Bot tokenni Railway o'zgaruvchilaridan oladi
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    bot = Bot(token=BOT_TOKEN)
    
    # FSM uchun xotira (bu muhim)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Ma'lumotlar bazasini ishga tushirish (Jadvallarni yaratish)
    await init_db()

    # --- ROUTERLARNI ULASH TARTIBI (JUDA MUHIM!) ---
    # 1. Birinchi bo'lib asosiy menyu routerlarini ulaymiz. 
    # Shunda ular har qanday holatda (state) ham birinchi bo'lib ishlaydi.
    dp.include_router(start.router)
    dp.include_router(profile.router) # Profile har doim tepada bo'lsin
    dp.include_router(tasks.router)
    dp.include_router(ranking.router)
    dp.include_router(info.router)

    # 2. Admin routerini ENG OXIRIDA ulaymiz.
    # Bu orqali adminning "raqam kirit" degan so'rovi boshqa tugmalarni yeb qo'ymaydi.
    dp.include_router(admin.router)

    print("🚀 @SparkCTF_bot ishga tushdi...")
    
    # Pollingni boshlash
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
