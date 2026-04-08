import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from database import init_db
from handlers import start, profile, tasks, info # info qo'shildi

async def main():
    # Bazani ishga tushiramiz
    await init_db()

    # FSM uchun xotira ajratamiz
    storage = MemoryStorage()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=storage)

    # Routerlarni tartib bilan ulaymiz
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(tasks.router)
    dp.include_router(info.router) # info ulandi

    print("Spark CTF bot ishga tushdi...")
    
    # Eski xabarlarni o'tkazib yuborish (bot yoqilganda qotib qolmasligi uchun)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
