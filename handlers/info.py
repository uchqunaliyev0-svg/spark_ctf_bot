from aiogram import Router, types, F

router = Router()

@router.message(F.text == "ℹ️ Info")
async def show_info(message: types.Message):
    text = (
        "🤖 **Spark CTF Bot**\n\n"
        "Flag formati: `SPARK{flag_nomi}`\n"
        "Tuzuvchi: @uchqun_aliyev"
    )
    await message.answer(text, parse_mode="Markdown")
