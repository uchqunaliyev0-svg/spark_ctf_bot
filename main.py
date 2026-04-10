import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from handlers import start, profile, ranking, tasks, info, admin

# Tokenni Railway Variables'dan olamiz
TOKEN = os.getenv("BOT_TOKEN")

async def main():
    if not TOKEN:
        print("XATO: BOT_TOKEN topilmadi! Railway Variables'ni tekshiring.")
        return
        
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(admin.router)  # Admin buyruqlari birinchi navbatda tekshiriladi
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(ranking.router)
    dp.include_router(tasks.router)
    dp.include_router(info.router)

    await bot.delete_webhook(drop_pending_updates=True)
    print("⚡️ @sparkCTF_bot is starting with Admin Mode...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
