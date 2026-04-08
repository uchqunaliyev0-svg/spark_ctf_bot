from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_user, add_user
from keyboards.main_menu import get_lang_keyboard, get_main_menu

router = Router()

class Register(StatesGroup):
    language = State()
    nickname = State()
    country = State()

@router.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer(
            "🌐 Tilni tanlang / Выберите язык / Choose language:", 
            reply_markup=get_lang_keyboard()
        )
        await state.set_state(Register.language)
    else:
        # Bazadan tilni olamiz (index 3)
        lang = user[3] if len(user) > 3 else "uz"
        await message.answer(
            f"🚀 Spark CTF-ga xush kelibsiz!", 
            reply_markup=get_main_menu(lang)
        )

@router.message(Register.language)
async def set_lang(message: types.Message, state: FSMContext):
    text = message.text
    # Tilni aniqlash mantiqi
    if "Русский" in text:
        lang = "ru"
    elif "English" in text:
        lang = "en"
    else:
        lang = "uz"
    
    await state.update_data(language=lang)
    
    msgs = {
        "uz": "Nickname yoki ismingizni kiriting:", 
        "ru": "Введите никнейм или ваше имя:", 
        "en": "Enter your nickname or name:"
    }
    # Keyingi qadamda klaviaturani o'chirib turamiz
    await message.answer(msgs[lang], reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Register.nickname)

@router.message(Register.nickname)
async def set_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    data = await state.get_data()
    lang = data['language']
    
    # Davlatlar uchun ham tugma chiqaramiz
    kb = [
        [KeyboardButton(text="🇺🇿 O'zbekiston")],
        [KeyboardButton(text="🇷🇺 Rossiya")],
        [KeyboardButton(text="🇺🇸 AQSH")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
    
    msgs = {
        "uz": "Davlatni tanlang yoki yozing:", 
        "ru": "Выберите или введите страну:", 
        "en": "Select or enter country:"
    }
    await message.answer(msgs[lang], reply_markup=markup)
    await state.set_state(Register.country)

@router.message(Register.country)
async def set_country(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data['language']
    # Bazaga hamma ma'lumotni saqlaymiz
    await add_user(message.from_user.id, data['nickname'], message.text, lang)
    await state.clear()
    
    msgs = {
        "uz": "Tayyor! ✅ Endi menyudan foydalanishingiz mumkin.", 
        "ru": "Готово! ✅ Теперь вы можете использовать меню.", 
        "en": "Done! ✅ Now you can use the menu."
    }
    await message.answer(msgs[lang], reply_markup=get_main_menu(lang))
