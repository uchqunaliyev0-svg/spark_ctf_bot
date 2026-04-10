import os
import asyncio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.session.aiohttp import AiohttpSession

# --- 1. SOZLAMALAR ---
TOKEN = "8725722196:AAFJ7-ADisGy_n8hPQph3yVhsGMCk9pSXBo"

# Interface va sessiya barqarorligi uchun
session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

class ProfileEdit(StatesGroup):
    waiting_for_name = State()

# --- 2. SCOREBOARD (BU SENING ESKI INTERFACINGGA MOS) ---
def create_scoreboard_graph():
    # Bu yerda biz necha marta yozgan bazadan SELECT mantiqlari bo'ladi
    users = ["lowkeyciso", "yaasosed", "NothingsNwe", "alimovichx", "ubbyt"]
    scores = [2266, 1552, 1060, 1047, 790]
    
    plt.figure(figsize=(10, 6))
    plt.style.use('dark_background')
    colors = ['#00ff00', '#00cc00', '#009900', '#006600', '#003300']
    plt.bar(users, scores, color=colors)
    plt.title("SparkCTF Global Scoreboard", color='#00ff00', fontsize=18)
    plt.grid(axis='y', linestyle='--', alpha=0.2)
    
    graph_path = "spark_scoreboard.png"
    plt.savefig(graph_path)
    plt.close()
    return graph_path

# --- 3. BUYRUQLAR (SENING INTERFACING) ---

@dp.message(Command("start"))
async def start(message: Message):
    # Sening eski "Start" interfeysing:
    await message.answer(
        "⚡️ **SparkCTF Platformasiga xush kelibsiz!**\n\n"
        "Tizim tayyor. Buyruqlar:\n"
        "📊 /scoreboard - Reyting\n"
        "👤 /profile - Profilingiz", 
        parse_mode="Markdown"
    )

@dp.message(Command("profile"))
async def profile(message: Message):
    # Bu sening o'sha biz tahrirlagan "Interface"ing
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Ismni tahrirlash ✏️", callback_data="edit_name"))
    
    await message.answer(
        f"👤 **SparkCTF Profilingiz:**\n\n"
        f"Nik: `{message.from_user.username or 'O\'rnatilmagan'}`\n"
        f"Ochko: 1250\n"
        f"Rank: #15",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@dp.message(Command("scoreboard"))
async def send_scoreboard(message: Message):
    wait_msg = await message.answer("📊 Grafik tayyorlanmoqda...")
    try:
        graph = create_scoreboard_graph()
        await message.answer_photo(FSInputFile(graph), caption="🔥 **SparkCTF Top Hackers**")
        if os.path.exists(graph): os.remove(graph)
    except Exception as e:
        await message.answer(f"❌ Xato: {e}")
    finally:
        await wait_msg.delete()

# --- 4. FSM (NICKNAME EDIT) ---

@dp.callback_query(F.data == "edit_name")
async def edit_name_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("⌨️ Yangi nikingizni yuboring:")
    await state.set_state(ProfileEdit.waiting_for_name)
    await callback.answer()

@dp.message(ProfileEdit.waiting_for_name)
async def process_new_name(message: Message, state: FSMContext):
    # Bu yerga Supabase update mantiqingni qo'shsang bo'ladi
    await message.answer(f"✅ Profil yangilandi: **{message.text}**", parse_mode="Markdown")
    await state.clear()

# --- 5. ISHGA TUSHIRISH (BU SENING BOTINGNI MIYYASI) ---
async def main():
    print("⚡️ @SparkCTF_bot ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
