from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from database import get_user
from locales import get_text

router = Router()

INFO_BTNS = ["ℹ️ Info", "ℹ️ Инфо"]

@router.message(StateFilter("*"), F.text.in_(INFO_BTNS))
@router.message(StateFilter("*"), Command("info"))
async def info_handler(message: types.Message, state: FSMContext):
    await state.clear()
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'en') if user else 'en'
    
    text = get_text(lang, "info_text")
    await message.answer(text, parse_mode="HTML")
