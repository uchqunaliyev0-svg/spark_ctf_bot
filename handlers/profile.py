from aiogram import Router, types, F
from database import get_user

router = Router()

@router.message(F.text == "👤 Profile")
async def show_profile(message: types.Message):
    user = await get_user(message.from_user.id)
    if user:
        text = (
            f"👤 **Profil**\n\n"
            f"Nick: {user[1]}\n"
            f"Yechilgan: {user[3]}\n"
            f"Ball: {user[2]}"
        )
        await message.answer(text, parse_mode="Markdown")
