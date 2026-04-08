from aiogram import Router, types, F
from aiogram.filters import Command
from database import get_tasks, check_flag_db

router = Router()

@router.message(F.text == "🚩 Tasks")
@router.message(Command("tasks"))
async def list_tasks(message: types.Message):
    tasks = await get_tasks()
    if not tasks:
        await message.answer("No tasks available yet. Stay tuned!")
        return
    
    response = "🚩 **Available Tasks:**\n\n"
    for t in tasks:
        task_name = t['name'].replace('_', ' ')
        response += f"🔹 **{task_name}** ({t['points']} pts)\n"
    
    response += "\n💡 Send the flag to me (Format: SPARK{...})"
    await message.answer(response, parse_mode="Markdown")

@router.message(F.text.startswith("SPARK{"))
async def handle_flag(message: types.Message):
    points = await check_flag_db(message.from_user.id, message.text.strip())
    if points:
        await message.answer(f"✅ Correct! You earned {points} points!")
    else:
        await message.answer("❌ Wrong flag or already solved.")
