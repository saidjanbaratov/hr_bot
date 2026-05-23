import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
HR_ADMINS = os.getenv("HR_ADMINS", "")

admin_ids = []
for admin_id in HR_ADMINS.split(","):
    admin_id = admin_id.strip()
    if admin_id:
        admin_ids.append(int(admin_id))

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

phone_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Telefon yuborish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


async def send_to_admins(message: Message, hr_text: str):
    for admin_id in admin_ids:
        await bot.send_message(
            chat_id=admin_id,
            text=hr_text
        )

        if message.document:
            await bot.send_document(
                chat_id=admin_id,
                document=message.document.file_id,
                caption="📎 Resume/CV fayli"
            )

        elif message.photo:
            await bot.send_photo(
                chat_id=admin_id,
                photo=message.photo[-1].file_id,
                caption="📎 Resume/CV rasmi"
            )

        else:
            await bot.send_message(
                chat_id=admin_id,
                text=f"📎 Resume/CV: {message.text}"
            )


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Assalomu alaykum 👋\n"
        "HR bo‘limi botiga xush kelibsiz.",
        reply_markup=menu
    )


@dp.message()
async def handler(message: Message):
    user_id = message.from_user.id
    text = message.text

    if text == "📞 Aloqa":
        await message.answer(
            "📞 HR telefon:\n+998 50 003 26 55",
            reply_markup=menu
        )
        return

    if text == "📝 Ariza topshirish":
        users[user_id] = {"step": "name"}
        await message.answer("👤 Ism familiyangizni yozing:")
        return

    if user_id not in users:
        await message.answer(
            "Pastdagi tugmalardan foydalaning 👇",
            reply_markup=menu
        )
        return

    step = users[user_id]["step"]

    if step == "name":
        users[user_id]["name"] = text
        users[user_id]["step"] = "age"
        await message.answer("🎂 Yoshingizni yozing:")
        return

    if step == "age":
        users[user_id]["age"] = text
        users[user_id]["step"] = "phone"
        await message.answer(
            "📱 Telefon raqamingizni yuboring:",
            reply_markup=phone_menu
        )
        return

    if step == "phone":
        if message.contact:
            users[user_id]["phone"] = message.contact.phone_number
        else:
            users[user_id]["phone"] = text

        users[user_id]["step"] = "position"
        await message.answer("💼 Qaysi lavozimga topshiryapsiz?")
        return

    if step == "position":
        users[user_id]["position"] = text
        users[user_id]["step"] = "experience"
        await message.answer("📌 Ish tajribangizni yozing:")
        return

    if step == "experience":
        users[user_id]["experience"] = text
        users[user_id]["step"] = "resume"
        await message.answer(
            "📎 Resume/CV yuboring.\n"
            "PDF, DOCX yoki rasm yuborishingiz mumkin.\n\n"
            "Agar resume yo‘q bo‘lsa: Yo‘q deb yozing."
        )
        return

    if step == "resume":
        try:
            data = users[user_id]

            hr_text = (
                "🆕 YANGI ARIZA\n\n"
                f"👤 Ism: {data['name']}\n"
                f"🎂 Yosh: {data['age']}\n"
                f"📞 Telefon: {data['phone']}\n"
                f"💼 Lavozim: {data['position']}\n"
                f"📌 Tajriba: {data['experience']}"
            )

            if not admin_ids:
                await message.answer(
                    "❌ HR admin ID kiritilmagan. Render’da HR_ADMINS qo‘shing.",
                    reply_markup=menu
                )
                return

            await send_to_admins(message, hr_text)

            await message.answer(
                "✅ Arizangiz HR adminlarga yuborildi!",
                reply_markup=menu
            )

            del users[user_id]
            return

        except Exception as error:
            await message.answer(
                f"❌ Xatolik bo‘ldi:\n{error}",
                reply_markup=menu
            )
            return


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
