from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_tasks, delete_task_db

router = Router()
ADMIN_ID = 5472714251 # ID'ingni tekshirib qo'y

@router.message(F.text == "🚩 Tasks")
async def show_tasks(message: types.Message, state: FSMContext):
    await state.clear()
    tasks_list = await get_tasks()
    
    if not tasks_list:
        await message.answer("📭 **No challenges available right now.**", parse_mode="Markdown")
        return

    builder = InlineKeyboardBuilder()
    for t in tasks_list:
        # Har bir task uchun alohida tugma
        builder.row(types.InlineKeyboardButton(
            text=f"🔓 {t['title']} — {t['points']}pt", 
            callback_data=f"view_{t['title']}")
        )
        
        # Admin bo'lsang, yoniga o'chirish tugmasini qo'shadi
        if message.from_user.id == ADMIN_ID:
            builder.row(types.InlineKeyboardButton(
                text=f"🗑 Delete {t['title']}", 
                callback_data=f"del_{t['title']}")
            )

    await message.answer(
        "📋 **AVAILABLE CHALLENGES:**\nSelect a task to see details.",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("view_"))
async def view_task(callback: types.CallbackQuery):
    task_title = callback.data.split("_")[1]
    # Kelajakda bu yerda task haqida to'liq ma'lumot chiqadi
    await callback.answer(f"Task: {task_title}\nSubmit the flag in the chat!", show_alert=True)

@router.callback_query(F.data.startswith("del_"))
async def delete_task_handler(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ No permission!", show_alert=True)
        return
    
    task_name = callback.data.split("_")[1]
    await delete_task_db(task_name)
    await callback.answer(f"✅ {task_name} deleted!")
    await callback.message.edit_text("Task removed. Update the list by clicking '🚩 Tasks'.")
