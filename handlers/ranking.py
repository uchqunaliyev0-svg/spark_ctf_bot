from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database import get_top_users

router = Router()

@router.message(F.text == "🏆 Ranking")
async def show_ranking(message: types.Message, state: FSMContext):
    await state.clear()
    top_users = await get_top_users()
    if not top_users:
        await message.answer("Ranking list is empty.")
        return
    text = "🏆 **TOP 10 HACKERS:**\n━━━━━━━━━━━━━━━\n"
    for i, user in enumerate(top_users, 1):
        text += f"{i}. {user['nickname']} — {user['points']} pts\n"
    await message.answer(text, parse_mode="Markdown")
