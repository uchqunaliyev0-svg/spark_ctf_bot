from aiogram import Router, types
from aiogram.filters import CommandStart
from keyboards.main_menu import get_main_menu
from database import add_user

router = Router()

@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await add_user(message.from_user.id, message.from_user.full_name)
    await message.answer(
        f"Welcome **{message.from_user.first_name}**! ⚡️\nChoose an option from the menu below:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )
