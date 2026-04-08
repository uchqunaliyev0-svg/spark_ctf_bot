from aiogram import Router, types, F
from database import get_top_users

router = Router()

@router.message(F.text == "🏆 Ranking")
async def show_ranking(message: types.Message):
    users = await get_top_users()
    if not users:
        await message.answer("No hackers in the leaderboard yet.")
        return
    text = "🏆 **Top 10 Hackers**\n\n"
    for i, user in enumerate(users, 1):
        text += f"{i}. {user['nickname']} — {user['points']} pts\n"
    await message.answer(text, parse_mode="Markdown")
