from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from database import add_user

router = Router()

@router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    await add_user(message.from_user.id, message.from_user.full_name)
    kb = [
        [types.KeyboardButton(text="🚩 Tasks"), types.KeyboardButton(text="👤 Profile")],
        [types.KeyboardButton(text="🏆 Ranking")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Welcome to Spark CTF!", reply_markup=keyboard)
