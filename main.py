import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start, profile, tasks

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlarni tartib bilan ulash
    dp.include_router(start.router)
    dp.include_router(profile.router) # Profil va Reyting shu yerda
    dp.include_router(tasks.router)   # Topshiriqlar shu yerda

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
