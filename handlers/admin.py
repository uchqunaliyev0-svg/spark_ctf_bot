from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import add_new_task

router = Router()

class AddTask(StatesGroup):
    waiting_for_title = State()
    waiting_for_points = State()
    waiting_for_file = State()
    waiting_for_flag = State()

@router.message(F.text == "/addtask")
async def start_add(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Enter Task Title:")
    await state.set_state(AddTask.waiting_for_title)

@router.message(AddTask.waiting_for_title)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Points:")
    await state.set_state(AddTask.waiting_for_points)

@router.message(AddTask.waiting_for_points)
async def process_points(message: types.Message, state: FSMContext):
    await state.update_data(points=int(message.text))
    await message.answer("Upload File or /skip:")
    await state.set_state(AddTask.waiting_for_file)

@router.message(AddTask.waiting_for_file)
async def process_file(message: types.Message, state: FSMContext):
    file_id = message.document.file_id if message.document else "No file"
    await state.update_data(file_id=file_id)
    await message.answer("Enter Flag:")
    await state.set_state(AddTask.waiting_for_flag)

@router.message(AddTask.waiting_for_flag)
async def process_flag(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await add_new_task(data['title'], data['file_id'], data['points'], message.text)
    await state.clear()
    await message.answer("✅ Task Added!")
