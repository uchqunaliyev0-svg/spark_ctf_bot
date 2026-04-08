from aiogram import Router, types, F
from database import get_tasks, check_flag_db

router = Router()

@router.message(F.text == "🚩 Tasks")
async def list_tasks(message: types.Message):
    tasks = await get_tasks()
    if not tasks:
        await message.answer("No tasks available yet. Stay tuned!")
        return
    
    response = "🚩 **Available Tasks:**\n\n"
    for t in tasks:
        response += f"🔹 **{t['name']}** ({t['points']} pts)\nDescription: {t['description']}\n\n"
    response += "💡 Send the flag to me (Format: SPARK{...})"
    await message.answer(response, parse_mode="Markdown")

@router.message(F.text.startswith("SPARK{"))
async def handle_flag(message: types.Message):
    points = await check_flag_db(message.from_user.id, message.text.strip())
    if points:
        await message.answer(f"✅ Correct! You earned {points} points!")
    else:
        await message.answer("❌ Wrong flag or already solved.")
