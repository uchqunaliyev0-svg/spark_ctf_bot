import asyncio
import logging
import matplotlib
matplotlib.use('Agg')  # Railway uchun shart!
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import start, profile, ranking, tasks, info, admin

async def main():
    # Bot va Dispatcher
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Sening papkangdagi routerlarni ulash
    # Har bir fayling ichida 'router' bor deb hisoblaymiz (standard aiogram 3)
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(ranking.router)
    dp.include_router(tasks.router)
    dp.include_router(info.router)
    dp.include_router(admin.router)

    print("⚡️ @SparkCTF_bot barcha modullari bilan ishga tushdi...")
    
    # Eski sessiyalarni tozalash (Conflict bo'lmasligi uchun)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi")
