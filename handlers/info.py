from aiogram import Router, types, F

router = Router()

@router.message(F.text == "ℹ️ Info")
async def show_info(message: types.Message):
    text = (
        "🤖 **Spark CTF Bot**\n\n"
        "This bot is designed to test your cybersecurity skills.\n\n"
        "🚩 **Flag Format:** `SPARK{flag_here}`\n"
        "👤 **Owner:** @uchqun_aliyev\n\n"
        "Stay sharp, hacker! ⚡️"
    )
    await message.answer(text, parse_mode="Markdown")
