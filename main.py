import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start, profile, tasks, ranking, admin, info, rename
from database import init_db

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())
    await init_db()

    # Routerlarni ulash
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(tasks.router)
    dp.include_router(ranking.router)
    dp.include_router(info.router)
    dp.include_router(rename.router) # Rename router qo'shildi
    dp.include_router(admin.router)

    print("🚀 SPARK CTF IS LIVE!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
