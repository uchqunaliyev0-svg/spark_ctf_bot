from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main_menu import get_main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Salom {message.from_user.full_name}, SparkCTF-ga xush kelibsan! 🔥",
        reply_markup=get_main_menu()
    )

