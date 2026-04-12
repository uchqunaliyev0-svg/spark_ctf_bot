from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import add_new_task, clear_all_tasks

router = Router()
ADMIN_ID = 5472714251

class AddTask(StatesGroup):
    waiting_for_title = State()
    waiting_for_points = State()
    waiting_for_flag = State()

@router.message(F.text == "/addtask")
async def start_add(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID: return
    await message.answer("Enter Task Title:")
    await state.set_state(AddTask.waiting_for_title)

@router.message(AddTask.waiting_for_title)
async def proc_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Points:")
    await state.set_state(AddTask.waiting_for_points)

@router.message(AddTask.waiting_for_points)
async def proc_points(message: types.Message, state: FSMContext):
    await state.update_data(points=int(message.text))
    await message.answer("Enter Flag:")
    await state.set_state(AddTask.waiting_for_flag)

@router.message(AddTask.waiting_for_flag)
async def proc_flag(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await add_new_task(data['title'], "Standard Challenge", data['points'], message.text)
    await state.clear()
    await message.answer("✅ Task added!")

@router.message(F.text == "/clear_all_garbage")
async def clear_garbage(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await clear_all_tasks()
        await message.answer("🧹 **ALL TASKS DELETED.** Your database is now fresh and clean!")

@router.message(Command("clear_garbage"))
async def clear_garbage(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        from database import clear_all_tasks
        await clear_all_tasks()
        await message.answer("🧹 **All tasks cleared!** Your bot is fresh now.")
