import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import start, profile, ranking, tasks, info, admin

# Botingni eski modullarini ulaymiz
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Sening handlers papkangdagi routerlarni ulaymiz
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(ranking.router)
    dp.include_router(tasks.router)
    dp.include_router(info.router)
    dp.include_router(admin.router)

    # Eski kutilayotgan xabarlarni tozalaymiz
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("⚡️ SparkCTF Bot eski zabardast holatiga qaytdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
