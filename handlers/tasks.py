from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database import get_tasks

router = Router()

@router.message(F.text == "🚩 Tasks", state="*")
async def show_tasks(message: types.Message, state: FSMContext):
    await state.clear()
    tasks_list = await get_tasks()
    
    if not tasks_list:
        await message.answer("📭 **No tasks available yet.**\nAdmin will add soon!", parse_mode="Markdown")
        return

    text = "🚩 **AVAILABLE TASKS:**\n━━━━━━━━━━━━━━━\n"
    for t in tasks_list:
        text += f"🔹 **{t['title']}** — {t['points']} pts\n"
    
    text += "\n💡 *Submit the flag directly to claim points!*"
    await message.answer(text, parse_mode="Markdown")
