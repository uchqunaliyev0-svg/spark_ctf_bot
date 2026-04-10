from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database import get_tasks

router = Router()

@router.message(F.text == "🚩 Tasks", state="*")
async def show_tasks(message: types.Message, state: FSMContext):
    await state.clear()
    
    tasks_list = await get_tasks()
    if not tasks_list:
        await message.answer("📭 Hozircha yangi tasklar yo'q. Stay tuned!")
        return

    text = "🚩 **MAVJUD TASKLAR:**\n━━━━━━━━━━━━━━━\n"
    for t in tasks_list:
        text += f"🔹 **{t['title']}** — {t['points']} pt\n"
    
    text += "\n💡 Flagni yuborish uchun shunchaki xabarga yozing!"
    await message.answer(text, parse_mode="Markdown")
