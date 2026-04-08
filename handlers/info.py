from aiogram import Router, types, F

router = Router()

@router.message(F.text == "ℹ️ Info")
async def show_info(message: types.Message):
    # Hech qanday murakkab Markdownlarsiz, oddiy matn
    text = (
        "🤖 Spark CTF Bot\n\n"
        "Flag formati: SPARK{flag_nomi}\n"
        "Tuzuvchi: @uchqun_aliyev"
    )
    await message.answer(text)
