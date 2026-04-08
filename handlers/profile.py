from aiogram import Router, types, F
from database import get_user
router = Router()
@router.message(F.text == "👤 Profile")
async def show_profile(message: types.Message):
    user = await get_user(message.from_user.id)
    if user:
        text = f"👤 Profile\n\nNick: {user[1]}\nSolved: {user[3]}\nPoints: {user[2]}"
        await message.answer(text)
