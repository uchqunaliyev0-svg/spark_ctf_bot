from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import add_new_task, clear_all_tasks
from config import ADMIN_ID

router = Router()

class AddTask(StatesGroup):
    waiting_for_category = State()
    waiting_for_title = State()
    waiting_for_points = State()
    waiting_for_file = State()
    waiting_for_flag = State()

@router.message(Command("addtask"))
async def start_add(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID: return
    await state.clear()
    
    # Mashhur CTF kategoriyalari bilan tugmalar
    builder = types.InlineKeyboardBuilder()
    categories = ["Web", "Crypto", "Pwn", "Reverse", "Forensics", "OSINT", "Misc"]
    for cat in categories:
        builder.button(text=cat, callback_data=f"admincat_{cat}")
    builder.adjust(2)
    
    await message.answer("📁 <b>Step 1:</b> Select or type Category name:", reply_markup=builder.as_markup(), parse_mode="HTML")
    await state.set_state(AddTask.waiting_for_category)

@router.callback_query(AddTask.waiting_for_category, F.data.startswith("admincat_"))
async def proc_cat_callback(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[1]
    await state.update_data(category=category)
    await callback.message.edit_text(f"📁 Category: <b>{category}</b>\n\n📝 Enter Task Title:", parse_mode="HTML")
    await state.set_state(AddTask.waiting_for_title)

@router.message(AddTask.waiting_for_category)
async def proc_cat_text(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer(f"📁 Category: <b>{message.text}</b>\n\n📝 Enter Task Title:", parse_mode="HTML")
    await state.set_state(AddTask.waiting_for_title)

@router.message(AddTask.waiting_for_title)
async def proc_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("💰 Points (e.g. 100):")
    await state.set_state(AddTask.waiting_for_points)

@router.message(AddTask.waiting_for_points)
async def proc_points(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Please enter a number for points!")
        return
    await state.update_data(points=int(message.text))
    await message.answer("📎 <b>Upload File</b> (Image/Zip) or send /skip:", parse_mode="HTML")
    await state.set_state(AddTask.waiting_for_file)

@router.message(AddTask.waiting_for_file)
async def proc_file(message: types.Message, state: FSMContext):
    if message.text == "/skip":
        await state.update_data(file_id=None)
    else:
        file_id = None
        if message.document:
            file_id = message.document.file_id
        elif message.photo:
            file_id = message.photo[-1].file_id
        await state.update_data(file_id=file_id)
        
    await message.answer("🚩 Enter Flag (format: <b>SPARK{...}</b>):", parse_mode="HTML")
    await state.set_state(AddTask.waiting_for_flag)

@router.message(AddTask.waiting_for_flag)
async def proc_flag(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await add_new_task(
        title=data['title'], 
        points=data['points'], 
        flag=message.text.strip(), 
        category=data['category'],
        file_id=data.get('file_id')
    )
    await state.clear()
    await message.answer(f"✅ <b>Task Created successfully!</b>\n\nTitle: {data['title']}\nCategory: {data['category']}", parse_mode="HTML")

@router.message(Command("clear_garbage"))
async def clear_garbage(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await clear_all_tasks()
        await message.answer("🧹 Database cleared!")
