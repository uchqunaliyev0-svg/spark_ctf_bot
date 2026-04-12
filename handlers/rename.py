from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import update_user_nickname

router = Router()

class Rename(StatesGroup):
    waiting_for_new_nickname = State()

@router.message(Command("rename"))
async def rename_cmd(message: types.Message, state: FSMContext):
    await message.answer("📝 Enter your <b>new hacker nickname:</b>", parse_mode="HTML")
    await state.set_state(Rename.waiting_for_new_nickname)

@router.message(Rename.waiting_for_new_nickname)
async def process_rename(message: types.Message, state: FSMContext):
    new_name = message.text
    if len(new_name) < 3 or len(new_name) > 15:
        await message.answer("❌ Nickname must be between 3 and 15 characters!")
        return
    
    await update_user_nickname(message.from_user.id, new_name)
    await state.clear()
    await message.answer(f"✅ Your nickname has been updated to: <b>{new_name}</b>", parse_mode="HTML")
