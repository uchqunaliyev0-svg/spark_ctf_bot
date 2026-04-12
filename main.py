import asyncio
import os
from aiogram import Bot, Dispatcher
from handlers import start, profile, tasks, ranking, admin, info, rename
from database import init_db
from middlewares.throttling import ThrottlingMiddleware

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    
    # ANTI-FLOOD YOQILDI
    dp.message.middleware(ThrottlingMiddleware(limit=1.0))
    
    await init_db()
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(tasks.router)
    dp.include_router(ranking.router)
    dp.include_router(info.router)
    dp.include_router(rename.router)

    print("🚀 SPARK CTF SECURE SYSTEM IS LIVE!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
