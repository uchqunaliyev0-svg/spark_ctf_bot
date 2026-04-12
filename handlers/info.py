from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text == "ℹ️ Info")
@router.message(F.text == "/info")
async def show_info(message: types.Message, state: FSMContext):
    await state.clear()
    text = (
        "🚀 **SPARK CTF PLATFORM**\n"
        "━━━━━━━━━━━━━━━\n"
        "This bot is designed for cybersecurity enthusiasts to practice "
        "their skills through Capture The Flag (CTF) challenges.\n\n"
        "👨‍💻 **Developer:** @uchqun_aliyev\n"
        "🛡 **Version:** 2.0 (Stable)\n"
        "📍 **University:** Cyber University, Tashkent"
    )
    await message.answer(text, parse_mode="Markdown")
