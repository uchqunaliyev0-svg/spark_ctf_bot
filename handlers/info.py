from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()

@router.message(F.text == "ℹ️ Info")
@router.message(Command("info"))
async def info_handler(message: types.Message):
    text = (
        "🚀 <b>SPARK CTF PLATFORM</b>\n"
        "━━━━━━━━━━━━━━━\n"
        "This is a private CTF arena for Cyber University students.\n\n"
        "🔹 <b>Available Commands:</b>\n"
        "/tasks — List challenges\n"
        "/profile — Your stats\n"
        "/ranking — Leaderboard\n"
        "/info — This message\n\n"
        "👤 <b>Developer:</b> @uchqun_aliyev\n"
        "🛡 <b>Status:</b> Online & Secure"
    )
    await message.answer(text, parse_mode="HTML")
