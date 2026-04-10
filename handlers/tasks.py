from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database import pool # bazadan tasklarni olish uchun

router = Router()

@router.message(F.text == "🚩 Tasks", state="*")
async def show_tasks(message: types.Message, state: FSMContext):
    await state.clear()
    
    async with pool.acquire() as conn:
        tasks = await conn.fetch("SELECT title, points FROM tasks")
    
    if not tasks:
        await message.answer("📭 Hozircha tasklar yo'q.")
        return

    text = "🚩 **MAVJUD TASKLAR:**\n\n"
    for t in tasks:
        text += f"🔹 {t['title']} — {t['points']} pt\n"
    
    await message.answer(text, parse_mode="Markdown")
