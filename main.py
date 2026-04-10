import os
import asyncio
import matplotlib
matplotlib.use('Agg')  # Railway serverida xato bermasligi uchun majburiy!
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.session.aiohttp import AiohttpSession

# --- 1. SOZLAMALAR ---
TOKEN = "8301731327:AAEv4YVoeLLNvniNAJlDZbc1G7Xm0yf7PuE"
session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

class ProfileEdit(StatesGroup):
    waiting_for_name = State()

# --- 2. SCOREBOARD (DATABASE'DAN OLISHGA TAYYOR) ---
def create_scoreboard_graph():
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

# --- 3. BUYRUQLAR ---
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("⚡️ **SparkCTF Bot ishga tushdi!**\n/scoreboard - Reyting\n/profile - Profil", parse_mode="Markdown")

@dp.message(Command("profile"))
async def profile(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Ismni tahrirlash ✏️", callback_data="edit_name"))
    await message.answer(f"👤 **Profil:**\nNik: `{message.from_user.username}`\nOchko: 1250", reply_markup=builder.as_markup(), parse_mode="Markdown")

@dp.message(Command("scoreboard"))
async def send_scoreboard(message: Message):
    wait_msg = await message.answer("📊 Grafik tayyorlanmoqda...")
    try:
        graph = create_scoreboard_graph()
        await message.answer_photo(FSInputFile(graph), caption="🔥 **Top 5 Global Hackers**")
        if os.path.exists(graph): os.remove(graph)
    except Exception as e:
        await message.answer(f"❌ Xato: {e}")
    finally:
        await wait_msg.delete()

@dp.callback_query(F.data == "edit_name")
async def edit_name_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("⌨️ Yangi nikingizni yuboring:")
    await state.set_state(ProfileEdit.waiting_for_name)
    await callback.answer()

@dp.message(ProfileEdit.waiting_for_name)
async def process_new_name(message: Message, state: FSMContext):
    await message.answer(f"✅ Yangilandi: **{message.text}**", parse_mode="Markdown")
    await state.clear()

async def main():
    print("⚡️ @SparkCTF_bot Railway'da uchishga tayyor...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
