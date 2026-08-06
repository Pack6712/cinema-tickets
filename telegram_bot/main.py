import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Start command handler
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "🎬 Добро пожаловать в Cinema Tickets!\n\n"
        "Выберите действие:",
        reply_markup=get_main_keyboard()
    )

def get_main_keyboard():
    """Get main keyboard"""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎬 Фильмы")],
            [KeyboardButton(text="🔎 Поиск")],
            [KeyboardButton(text="🎟 Купить билет")],
            [KeyboardButton(text="🎫 Мои билеты")],
            [KeyboardButton(text="❤️ Избранное")],
            [KeyboardButton(text="👤 Профиль")],
        ],
        resize_keyboard=True,
    )

async def main():
    logger.info("🤖 Telegram Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
