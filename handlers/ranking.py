from aiogram import Router, types, F
from aiogram.filters import Command
from database import get_top_users

router = Router()

@router.message(F.text == "🏆 Ranking")
@router.message(Command("ranking"))
async def show_ranking(message: types.Message):
    users = await get_top_users()
    if not users:
        await message.answer("Leaderboard is empty.")
        return
    
    text = "🏆 Top 10 Hackers\n\n"
    for i, user in enumerate(users, 1):
        text += f"{i}. {user['nickname']} — {user['points']} pts\n"
    await message.answer(text)
