import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from handlers import start, profile, ranking, tasks, info, admin
from database import init_db  # <--- Buni qo'shdik

# Tokenni Railway Variables'dan olamiz
TOKEN = os.getenv("BOT_TOKEN")

async def main():
    if not TOKEN:
        print("XATO: BOT_TOKEN topilmadi! Railway Variables'ni tekshiring.")
        return

    # 1. Bazani va ulanishlar pulini (pool) ishga tushiramiz
    await init_db() 
    print("✅ Ma'lumotlar bazasi ulanishi tayyor.")

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # 2. Routerlarni ulash
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(ranking.router)
    dp.include_router(tasks.router)
    dp.include_router(info.router)

    # 3. Botni ishga tushirish
    await bot.delete_webhook(drop_pending_updates=True)
    print("⚡️ @sparkCTF_bot is starting with Admin Mode...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi")
