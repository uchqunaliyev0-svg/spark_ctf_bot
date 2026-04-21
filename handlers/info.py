from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(StateFilter("*"), F.text == "ℹ️ Info")
@router.message(StateFilter("*"), Command("info"))
async def info_handler(message: types.Message, state: FSMContext):
    await state.clear()
    text = (
        "<b>SPARK CTF PLATFORM</b>\n\n"
        "<b>Flag Format:</b> <code>SPARK{flag_here}</code>\n"
        "<b>Edit Nickname:</b> /rename\n\n"
        "<b>Developer:</b> @uchqun_aliyev\n"
        "<b>Status:</b> Secure Connection"
    )
    await message.answer(text, parse_mode="HTML")
