from aiogram import Router, types, F

router = Router()

@router.message(F.text == "👤 Profil")
async def show_profile(message: types.Message):
    text = (
        f"👤 **Sening profiling:**\n\n"
        f"🆔 ID: `{message.from_user.id}`\n"
        f"🏆 Ballar: 0 XP\n"
        f"✅ Yechilgan tasklar: 0 ta"
    )
    await message.answer(text, parse_mode="Markdown")

@router.message(F.text == "📈 Reyting") # Tugmadagi emoji bilan bir xil bo'lsin
async def show_leaderboard(message: types.Message):
    await message.answer("📈 Reyting hozircha bo'sh. Tez orada yangilanadi!")
