from aiogram import Router, types, F
from database import get_user

router = Router()

@router.message(F.text.contains("Profil") | F.text.contains("Profile") | F.text.contains("Профиль"))
async def show_profile(message: types.Message):
    user = await get_user(message.from_user.id)
    if user:
        # user[1] - nick, user[2] - country, user[3] - lang, user[4] - points
        lang = user[3]
        text = {
            "uz": f"👤 **Profil**\n\n🆔 ID: `{user[0]}`\n👤 Nick: {user[1]}\n🌍 Davlat: {user[2]}\n🏆 Ball: {user[4]}",
            "ru": f"👤 **Профиль**\n\n🆔 ID: `{user[0]}`\n👤 Ник: {user[1]}\n🌍 Страна: {user[2]}\n🏆 Очки: {user[4]}",
            "en": f"👤 **Profile**\n\n🆔 ID: `{user[0]}`\n👤 Nick: {user[1]}\n🌍 Country: {user[2]}\n🏆 Points: {user[4]}"
        }
        await message.answer(text.get(lang, text["uz"]), parse_mode="Markdown")
    else:
        await message.answer("Siz hali ro'yxatdan o'tmagansiz. /start bosing.")
