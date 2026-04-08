from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_user, add_user
from keyboards.main_menu import get_main_menu

router = Router()
class Register(StatesGroup): nickname = State()

@router.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Welcome to Spark CTF.\nPlease enter your Nickname to register:")
        await state.set_state(Register.nickname)
    else:
        await message.answer(f"Welcome back, {user[1]}.", reply_markup=get_main_menu())

@router.message(Register.nickname)
async def set_nickname(message: types.Message, state: FSMContext):
    nick = message.text[:15]
    await add_user(message.from_user.id, nick)
    await state.clear()
    await message.answer(f"Nickname saved: {nick}", reply_markup=get_main_menu())
