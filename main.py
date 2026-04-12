import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start, profile, tasks, ranking, admin, info
from database import init_db

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())
    await init_db()

    # Routerlar tartibi
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(tasks.router)
    dp.include_router(ranking.router)
    dp.include_router(info.router) # Info qaytdi!
    dp.include_router(admin.router)

    print("🚀 Bot is running with Admin privileges...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
