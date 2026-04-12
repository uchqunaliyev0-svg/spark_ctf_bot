from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()

@router.message(F.text == "ℹ️ Info")
@router.message(Command("info"))
async def info_handler(message: types.Message):
    text = (
        "🚀 <b>SPARK CTF PLATFORM</b>\n"
        "━━━━━━━━━━━━━━━\n"
        "🔹 <b>Flag Format:</b> <code>spark{flag_here}</code>\n"
        "🔹 <b>Edit Nickname:</b> /rename\n\n"
        "👤 <b>Developer:</b> @uchqun_aliyev\n"
        "🛡 <b>Status:</b> Secure Connection"
    )
    await message.answer(text, parse_mode="HTML")
