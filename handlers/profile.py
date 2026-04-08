from aiogram import Router, types, F
from database import get_user

router = Router()

@router.message(F.text == "👤 Profile")
async def show_profile(message: types.Message):
    user = await get_user(message.from_user.id)
    if user:
        text = (
            f"👤 **Hacker Profile**\n\n"
            f"👤 **Nick:** {user[1]}\n"
            f"🚩 **Solved:** {user[3]} tasks\n"
            f"🏆 **Points:** {user[2]}"
        )
        await message.answer(text, parse_mode="Markdown")
