from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from database import get_user

router = Router()

@router.message(StateFilter("*"), F.text == "👤 Profile")
@router.message(StateFilter("*"), Command("profile"))
async def show_profile(message: types.Message, state: FSMContext):
    await state.clear()
    user = await get_user(message.from_user.id)
    text = f"**PROFILE**\n\nNick: {user['nickname']}\nPoints: {user['points']} pts"
    await message.answer(text, parse_mode="Markdown")
