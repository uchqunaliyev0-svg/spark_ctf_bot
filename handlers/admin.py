from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import add_new_task, clear_all_tasks

router = Router()
ADMIN_ID = 5472714251 # <--- AGAR ID BOSHQA BO'LSA, SHUNI O'ZGARTIR!

class AddTask(StatesGroup):
    waiting_for_title = State()
    waiting_for_points = State()
    waiting_for_flag = State()

@router.message(Command("addtask"))
async def start_add(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await state.clear()
    await message.answer("🛠 <b>ADMIN: NEW TASK</b>\n\nEnter task title (e.g. Steganography):", parse_mode="HTML")
    await state.set_state(AddTask.waiting_for_title)

@router.message(AddTask.waiting_for_title)
async def proc_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("💰 Enter points (e.g. 100):")
    await state.set_state(AddTask.waiting_for_points)

@router.message(AddTask.waiting_for_points)
async def proc_points(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Send a number!")
        return
    await state.update_data(points=int(message.text))
    await message.answer("🚩 Enter Flag (format: spark{...}):")
    await state.set_state(AddTask.waiting_for_flag)

@router.message(AddTask.waiting_for_flag)
async def proc_flag(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await add_new_task(data['title'], "CTF Challenge", data['points'], message.text)
    await state.clear()
    await message.answer(f"✅ <b>Task Created:</b> {data['title']}", parse_mode="HTML")

@router.message(Command("clear_garbage"))
async def clear_garbage(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await clear_all_tasks()
        await message.answer("🧹 <b>Database Cleared!</b>", parse_mode="HTML")
