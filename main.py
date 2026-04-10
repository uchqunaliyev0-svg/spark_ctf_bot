import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import start, profile, tasks, ranking, admin
from database import init_db

logging.basicConfig(level=logging.INFO)

async def main():
    # Railway Variables'dan tokenni oladi
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())

    # Bazani ulaymiz
    await init_db()

    # --- TARTIB JUDA MUHIM ---
    dp.include_router(profile.router) # 1
    dp.include_router(tasks.router)   # 2
    dp.include_router(ranking.router) # 3
    dp.include_router(start.router)   # 4
    dp.include_router(admin.router)   # 5 (Eng oxirida)

    print("🚀 Spark CTF bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
