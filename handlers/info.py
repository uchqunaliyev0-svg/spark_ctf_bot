from aiogram import Router, types, F
router = Router()
@router.message(F.text == "ℹ️ Info")
async def show_info(message: types.Message):
    text = "🤖 Spark CTF Bot\n\nFlag format: SPARK{flag_name}\nDeveloper: @uchqun_aliyev"
    await message.answer(text)
