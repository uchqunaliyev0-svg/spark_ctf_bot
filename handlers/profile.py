from aiogram import Router, types, F
from aiogram.filters import Command
from database import get_user

router = Router()

@router.message(F.text == "👤 Profile")
@router.message(Command("profile"))
async def show_profile(message: types.Message):
    user = await get_user(message.from_user.id)
    text = f"👤 **PROFILE**\nNick: {user['nickname']}\nPoints: {user['points']} pts"
    await message.answer(text, parse_mode="Markdown")
