import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
HR_GROUP_ID = int(os.getenv("HR_GROUP_ID"))

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

phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(
            text="📱 Telefon yuborish",
            request_contact=True
        )]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Assalomu alaykum 👋\nHR bo‘limi botiga xush kelibsiz.",
        reply_markup=menu
    )


@dp.message(F.text == "📞 Aloqa")
async def contact(message: Message):
    await message.answer(
        "📞 HR telefon:\n+998 50 003 26 55"
    )


@dp.message(F.text == "📝 Ariza topshirish")
async def apply(message: Message):
    users[message.from_user.id] = {}
    users[message.from_user.id]["step"] = "name"

    await message.answer(
        "👤 Ism familiyangizni yozing:"
    )


@dp.message()
async def process(message: Message):

    user_id = message.from_user.id

    if user_id not in users:
        await message.answer(
            "Pastdagi tugmalardan foydalaning 👇",
            reply_markup=menu
        )
        return

    step = users[user_id]["step"]

    if step == "name":
        users[user_id]["name"] = message.text
        users[user_id]["step"] = "age"

        await message.answer(
            "🎂 Yoshingizni yozing:"
        )
        return

    if step == "age":
        users[user_id]["age"] = message.text
        users[user_id]["step"] = "phone"

        await message.answer(
            "📱 Telefon raqamingizni yuboring:",
            reply_markup=phone_keyboard
        )
        return

    if step == "phone":

        if message.contact:
            users[user_id]["phone"] = message.contact.phone_number
        else:
            users[user_id]["phone"] = message.text

        users[user_id]["step"] = "position"

        await message.answer(
            "💼 Qaysi lavozimga topshiryapsiz?"
        )
        return

    if step == "position":
        users[user_id]["position"] = message.text
        users[user_id]["step"] = "experience"

        await message.answer(
            "📌 Ish tajribangizni yozing:"
        )
        return

    if step == "experience":
        users[user_id]["experience"] = message.text
        users[user_id]["step"] = "resume"

        await message.answer(
            "📎 Resume/CV yuboring.\n"
            "PDF, DOCX yoki rasm yuborishingiz mumkin.\n\n"
            "Agar resume yo‘q bo‘lsa: Yo‘q deb yozing."
        )
        return

    if step == "resume":

        data = users[user_id]

        text = (
            "🆕 YANGI ARIZA\n\n"
            f"👤 Ism: {data['name']}\n"
            f"🎂 Yosh: {data['age']}\n"
            f"📞 Telefon: {data['phone']}\n"
            f"💼 Lavozim: {data['position']}\n"
            f"📌 Tajriba: {data['experience']}"
        )

        await bot.send_message(
            HR_GROUP_ID,
            text
        )

        if message.document:
            await bot.send_document(
                HR_GROUP_ID,
                message.document.file_id,
                caption="📎 Resume/CV"
            )

        elif message.photo:
            await bot.send_photo(
                HR_GROUP_ID,
                message.photo[-1].file_id,
                caption="📎 Resume/CV"
            )

        else:
            await bot.send_message(
                HR_GROUP_ID,
                f"📎 Resume: {message.text}"
            )

        await message.answer(
            "✅ Arizangiz HR guruhga yuborildi!",
            reply_markup=menu
        )

        del users[user_id]


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
