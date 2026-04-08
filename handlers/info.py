from aiogram import Router, types, F

router = Router()

@router.message(F.text.in_(["ℹ️ Ma'lumot", "ℹ️ Info", "ℹ️ Инфо"]))
async def show_info(message: types.Message):
    text = {
        "uz": "🤖 **Spark CTF Bot**\n\nBu bot kiberxavfsizlik bo'yicha bilimlaringizni sinash uchun yaratilgan.\n\n🚩 Flag formati: spark{flag_nomi}\n👤 Tuzuvchi: @uchqun_ali",
        "en": "🤖 **Spark CTF Bot**\n\nThis bot is designed to test your cybersecurity skills.\n\n🚩 Flag format: spark{flag_name}\n👤 Creator: @uchqun_ali",
        "ru": "🤖 **Spark CTF Bot**\n\nЭтот бот создан для проверки ваших навыков кибербезопасности.\n\n🚩 Формат флага: spark{flag_name}\n👤 Создатель: @uchqun_ali"
    }
    msg = text["uz"]
    if message.text and "Info" in message.text: msg = text["en"]
    elif message.text and "Инфо" in message.text: msg = text["ru"]
    
    await message.answer(msg, parse_mode="Markdown")
