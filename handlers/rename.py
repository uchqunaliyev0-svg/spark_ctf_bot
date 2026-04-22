from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import update_user_nickname, get_user
from locales import get_text

router = Router()

class Rename(StatesGroup):
    waiting_for_new_nickname = State()

@router.message(Command("rename"))
async def rename_cmd(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'en') if user else 'en'
    
    await message.answer(get_text(lang, "rename_prompt"), parse_mode="HTML")
    await state.set_state(Rename.waiting_for_new_nickname)

@router.message(Rename.waiting_for_new_nickname)
async def process_rename(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'en') if user else 'en'
    
    new_name = message.text
    if len(new_name) < 3 or len(new_name) > 15:
        await message.answer(get_text(lang, "nickname_error"))
        return
    
    await update_user_nickname(message.from_user.id, new_name)
    await state.clear()
    await message.answer(get_text(lang, "rename_success").format(new_name), parse_mode="HTML")
