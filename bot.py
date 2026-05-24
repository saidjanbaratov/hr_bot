import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Ariza topshirish")],
        [KeyboardButton(text="📞 Aloqa")]
    ],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Assalomu alaykum 👋\nHR bo‘limi botiga xush kelibsiz.",
        reply_markup=menu
    )


@dp.message()
async def handler(message: Message):
    if message.text == "📝 Ariza topshirish":
        await message.answer("👤 Ism familiyangizni yozing:")
    elif message.text == "📞 Aloqa":
        await message.answer("📞 HR telefon:\n+998 50 003 26 55")
    else:
        await message.answer("Pastdagi tugmalardan foydalaning 👇", reply_markup=menu)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
