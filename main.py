kkimport asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from database import init_db
from handlers import start, profile, tasks # Hamma routerlarni import qilamiz

async def main():
    # Bazani ishga tushiramiz (yangi ustunlar bilan)
    await init_db()
    
    # FSM uchun xotira ajratamiz
    storage = MemoryStorage()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=storage)

    # Routerlarni tartib bilan ulaymiz
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(tasks.router)

    print("Spark CTF bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
