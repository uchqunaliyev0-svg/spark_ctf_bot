from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_tasks, delete_task_db

router = Router()
ADMIN_ID = 5472714251 # <--- BU YERGA O'ZINGNI ID'INGNI YOZ, UCHQUN!

@router.message(F.text == "🚩 Tasks")
async def show_tasks(message: types.Message, state: FSMContext):
    await state.clear()
    tasks_list = await get_tasks()
    
    if not tasks_list:
        await message.answer("📭 No tasks available.")
        return

    for t in tasks_list:
        builder = InlineKeyboardBuilder()
        # Agar foydalanuvchi sen bo'lsang, o'chirish tugmasi chiqadi
        if message.from_user.id == ADMIN_ID:
            builder.row(types.InlineKeyboardButton(
                text="🗑 Delete Task", 
                callback_data=f"del_{t['title']}")
            )
        
        text = f"🚩 **{t['title']}**\n💰 Points: {t['points']} pts"
        await message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")

@router.callback_query(F.data.startswith("del_"))
async def delete_task_handler(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Access Denied!", show_alert=True)
        return
    
    task_title = callback.data.split("_")[1]
    await delete_task_db(task_title)
    await callback.message.delete()
    await callback.answer(f"✅ {task_title} deleted!")
