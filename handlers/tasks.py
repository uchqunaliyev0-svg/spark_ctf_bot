from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_tasks, delete_task_db

router = Router()
ADMIN_ID = 5472714251 

@router.message(F.text == "🚩 Tasks")
@router.message(Command("tasks"))
async def show_tasks(message: types.Message, state: FSMContext):
    await state.clear()
    tasks_list = await get_tasks()
    
    if not tasks_list:
        await message.answer("📭 <b>No challenges available.</b>", parse_mode="HTML")
        return

    for t in tasks_list:
        builder = InlineKeyboardBuilder()
        # Admin bo'lsang, o'chirish tugmasi chiqadi
        if message.from_user.id == ADMIN_ID:
            builder.row(types.InlineKeyboardButton(text="🗑 Delete Task", callback_data=f"del_{t['title']}"))
        
        text = f"🚩 <b>{t['title']}</b>\n💰 Points: {t['points']} pts"
        await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(F.data.startswith("del_"))
async def delete_handler(callback: types.CallbackQuery):
    task_name = callback.data.split("_")[1]
    await delete_task_db(task_name)
    await callback.message.delete()
    await callback.answer(f"✅ {task_name} deleted!")
