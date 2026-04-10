import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import start, profile, ranking, tasks, info

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Sening papkangdagi routerlarni ulash
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(ranking.router)
    dp.include_router(tasks.router)
    dp.include_router(info.router)

    await bot.delete_webhook(drop_pending_updates=True)
    print("⚡️ SparkCTF Bot is back to original state!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
