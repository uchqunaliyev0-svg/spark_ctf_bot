from aiogram import Router, types, F

router = Router()

@router.message(F.text.in_(["🚩 Topshiriqlar", "🚩 Tasks", "🚩 Задания"]))
async def show_tasks(message: types.Message):
    text = {
        "🚩 Topshiriqlar": "🚩 **Capture The Flag** topshiriqlari yaqin orada paydo bo'ladi!\nTayyor turing, pentester!",
        "🚩 Tasks": "🚩 **Capture The Flag** tasks will be available soon!\nStay tuned, pentester!",
        "🚩 Задания": "🚩 **Capture The Flag** задания скоро появятся!\nБудьте готовы, пентестер!"
    }
    await message.answer(text.get(message.text, "Soon..."), parse_mode="Markdown")
