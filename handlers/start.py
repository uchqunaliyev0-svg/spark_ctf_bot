from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_user, add_user
from keyboards.main_menu import get_main_menu

router = Router()

class Registration(StatesGroup):
    waiting_for_nickname = State()

@router.message(StateFilter("*"), CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    user = await get_user(message.from_user.id)
    if user:
        await message.answer(f"Welcome back, **{user['nickname']}**!", reply_markup=get_main_menu(), parse_mode="Markdown")
    else:
        await message.answer("👋 **Welcome to Spark CTF!**\nYou are not registered yet. Please enter your **Hacker Nickname**:")
        await state.set_state(Registration.waiting_for_nickname)

@router.message(Registration.waiting_for_nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    if len(message.text) < 3 or len(message.text) > 15:
        await message.answer("⚠️ Nickname must be between 3 and 15 characters!")
        return
    
    await add_user(message.from_user.id, message.text)
    await state.clear()
    await message.answer(f"✅ Registered successfully as **{message.text}**!", reply_markup=get_main_menu(), parse_mode="Markdown")
