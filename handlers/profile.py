from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from database import get_user
from locales import get_text

router = Router()

PROFILE_BTNS = ["👤 Profile", "👤 Профиль", "👤 Profil"]

@router.message(StateFilter("*"), F.text.in_(PROFILE_BTNS))
@router.message(StateFilter("*"), Command("profile"))
async def show_profile(message: types.Message, state: FSMContext):
    await state.clear()
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Please /start first.")
        return

    lang = user.get('language', 'en')
    text = get_text(lang, "profile_text").format(
        user['nickname'], user['points'], user['solved_count']
    )
    await message.answer(text, parse_mode="HTML")
