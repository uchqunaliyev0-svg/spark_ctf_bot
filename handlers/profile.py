from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database import get_user

router = Router()

@router.message(F.text == "👤 Profile")
async def show_profile(message: types.Message, state: FSMContext):
    await state.clear()
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Profile not found.")
        return
    text = f"👤 **PROFILE**\nNick: {user['nickname']}\nPoints: {user['points']} pts"
    await message.answer(text, parse_mode="Markdown")
