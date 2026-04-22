from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_user, add_user, update_user_language
from keyboards.main_menu import get_main_menu
from locales import get_text

router = Router()

class Registration(StatesGroup):
    waiting_for_nickname = State()
    waiting_for_language = State()

def get_language_keyboard():
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.button(text="🇬🇧 English", callback_data="lang_en")
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.button(text="🇺🇿 O'zbekcha", callback_data="lang_uz")
    builder.adjust(1)
    return builder.as_markup()

@router.message(StateFilter("*"), CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    user = await get_user(message.from_user.id)
    if user:
        lang = user.get('language', 'en')
        await message.answer(get_text(lang, "welcome_back").format(user['nickname']), reply_markup=get_main_menu(lang), parse_mode="HTML")
    else:
        await message.answer(get_text("en", "welcome"), parse_mode="HTML")
        await state.set_state(Registration.waiting_for_nickname)

@router.message(Registration.waiting_for_nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    if len(message.text) < 3 or len(message.text) > 15:
        await message.answer(get_text("en", "nickname_error"))
        return
    
    await state.update_data(nickname=message.text)
    await message.answer(get_text("en", "lang_choose"), reply_markup=get_language_keyboard())
    await state.set_state(Registration.waiting_for_language)

@router.callback_query(Registration.waiting_for_language, F.data.startswith("lang_"))
async def process_language(callback: types.CallbackQuery, state: FSMContext):
    lang_code = callback.data.split("_")[1]
    data = await state.get_data()
    nickname = data.get("nickname")
    
    await add_user(callback.from_user.id, nickname, lang_code)
    await state.clear()
    
    await callback.message.edit_text(get_text(lang_code, "registered").format(nickname), parse_mode="HTML")
    await callback.message.answer(get_text(lang_code, "welcome_back").format(nickname), reply_markup=get_main_menu(lang_code), parse_mode="HTML")
