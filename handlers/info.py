from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()

@router.message(F.text == "ℹ️ Info")
@router.message(Command("info"))
async def info_handler(message: types.Message):
    text = (
        "🚀 **SPARK CTF PLATFORM**\n"
        "━━━━━━━━━━━━━━━\n"
        "Welcome to the ultimate CTF arena! This bot is built for "
        "Cyber University students to test their hacking skills.\n\n"
        "🔹 **How to play?**\n"
        "1. Select a challenge in 🚩 Tasks\n"
        "2. Find the hidden flag (format: spark{...})\n"
        "3. Send the flag here to get points!\n\n"
        "👤 **Developer:** @uchqun_aliyev\n"
        "🛡 **Version:** 2.1 (Stable)"
    )
    await message.answer(text, parse_mode="Markdown")
