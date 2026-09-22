# 🚀 Spark CTF Bot

A Telegram bot platform for managing CTF (Capture The Flag) 
competitions with real-time scoreboard and rating system.

## ✨ Features

- 🏆 Real-time scoreboard with graph visualization
- 👤 User profiles with points & solve tracking
- 🌍 Multi-language support (UZ, RU, EN)
- 📊 Global rating system
- 🔐 Flag submission system `SPARK{flag_here}`
- 🛡️ Secure connection

## 🛠️ Tech Stack

- Python
- Aiogram
- PostgreSQL (asyncpg) — masalan, bepul [Neon](https://neon.tech)
- FSM (Finite State Machine)

## 🚀 Getting Started

1. Clone the repo
2. Install requirements: `pip install -r requirements.txt`
3. Set environment variables:
   - `BOT_TOKEN` — token from @BotFather
   - `ADMIN_ID` — your Telegram user ID
   - `DATABASE_URL` — PostgreSQL connection string (e.g. from Neon)
4. Run: `python main.py` (tables are created automatically)

## 👨‍💻 Developer

Made by [@uchqun_aliyev](https://t.me/uchqun_aliyev)
