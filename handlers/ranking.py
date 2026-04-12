from aiogram import Router, types, F
from aiogram.filters import Command
from database import get_top_users

router = Router()

@router.message(F.text == "🏆 Ranking")
@router.message(Command("ranking"))
async def show_ranking(message: types.Message):
    top = await get_top_users()
    text = "🏆 **TOP 10:**\n" + "\n".join([f"{u['nickname']}: {u['points']}" for u in top])
    await message.answer(text, parse_mode="Markdown")
