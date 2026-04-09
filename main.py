import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from database import init_db
from handlers import start, profile, tasks, info, ranking, admin

async def main():
    await init_db()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Routerlarni to'g'ri tartibda ulash
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(tasks.router)
    dp.include_router(info.router)
    dp.include_router(ranking.router)
    dp.include_router(admin.router)

    print("Spark CTF bot is online...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
