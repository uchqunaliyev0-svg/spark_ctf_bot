from aiogram import Router, types, F

router = Router()

@router.message(F.text == "ℹ️ Info")
@router.message(F.text == "/info")
async def info_handler(message: types.Message):
    text = (
        "🚀 **SPARK CTF PLATFORM**\n"
        "━━━━━━━━━━━━━━━\n"
        "Welcome to the next generation of CTF bots. Practice your skills, "
        "climb the leaderboard, and become a pro pentester!\n\n"
        "👤 **Developer:** @uchqun_aliyev\n"
        "🛠 **Stack:** Aiogram 3.x, PostgreSQL\n"
        "📡 **Host:** Railway Cloud"
    )
    await message.answer(text, parse_mode="Markdown")
