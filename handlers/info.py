from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()

@router.message(F.text == "ℹ️ Info")
@router.message(Command("info"))
async def info_handler(message: types.Message):
    text = (
        "🚀 **SPARK CTF PLATFORM**\n"
        "━━━━━━━━━━━━━━━\n"
        "This is a private CTF platform for Cyber University students.\n\n"
        "🔹 **Commands:**\n"
        "/tasks - List all challenges\n"
        "/profile - Your stats\n"
        "/ranking - Leaderboard\n\n"
        "👤 **Developer:** @uchqun_aliyev\n"
        "🛡 **Status:** Active"
    )
    await message.answer(text, parse_mode="Markdown")
