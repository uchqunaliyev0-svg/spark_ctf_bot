from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()

@router.message(F.text == "ℹ️ Info")
@router.message(Command("info"))
async def show_info(message: types.Message):
    text = (
        "🤖 Spark CTF Bot\n\n"
        "Flag format: SPARK{flag_name}\n"
        "Developer: @uchqun_aliyev"
    )
    await message.answer(text)
