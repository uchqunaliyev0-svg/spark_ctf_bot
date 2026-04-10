from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from database import add_user

router = Router()

@router.message(CommandStart(), state="*")
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    
    # Foydalanuvchini bazaga qo'shish
    await add_user(message.from_user.id, message.from_user.full_name)
    
    # Menyu tugmalari
    kb = [
        [types.KeyboardButton(text="🚩 Tasks"), types.KeyboardButton(text="👤 Profile")],
        [types.KeyboardButton(text="🏆 Ranking")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        f"Salom {message.from_user.first_name}! Spark CTF platformasiga xush kelibsan.\n"
        "Pastdagi tugmalar orqali tasklarni yechishni boshla! 🔥",
        reply_markup=keyboard
    )
