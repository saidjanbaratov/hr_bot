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

users = {}

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
    user_id = message.from_user.id
    text = message.text

    if text == "📞 Aloqa":
        await message.answer("📞 HR telefon:\n+998 50 003 26 55")
        return

    if text == "📝 Ariza topshirish":
        users[user_id] = {"step": "name"}
        await message.answer("👤 Ism familiyangizni yozing:")
        return

    if user_id in users:
        step = users[user_id]["step"]

        if step == "name":
            users[user_id]["name"] = text
            users[user_id]["step"] = "age"
            await message.answer("🎂 Yoshingizni yozing:")
            return

        if step == "age":
            users[user_id]["age"] = text
            await message.answer(
                f"✅ Ma’lumot qabul qilindi:\n\n"
                f"👤 Ism: {users[user_id]['name']}\n"
                f"🎂 Yosh: {users[user_id]['age']}"
            )
            del users[user_id]
            return

    await message.answer("Pastdagi tugmalardan foydalaning 👇", reply_markup=menu)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
