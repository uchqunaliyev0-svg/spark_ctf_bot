from aiogram import Router, types, F

router = Router()

@router.message(F.text == "🚩 Topshiriqlar")
async def show_tasks(message: types.Message):
    await message.answer("🚩 Topshiriqlar ro'yxati yaqinda ochiladi!")


