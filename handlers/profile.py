from aiogram import Router, types, F
from aiogram.filters import Command
from database import get_user

router = Router()

@router.message(F.text == "👤 Profile")
@router.message(Command("profile"))
async def show_profile(message: types.Message):
    user = await get_user(message.from_user.id)
    if user:
        text = (
            f"👤 **Profile**\n\n"
            f"Nick: {user[1]}\n"
            f"Solved: {user[3]}\n"
            f"Points: {user[2]}"
        )
        await message.answer(text, parse_mode="Markdown")
