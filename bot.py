import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
HR_GROUP_ID = os.getenv("HR_GROUP_ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_data = {}

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Ariza topshirish")],
        [KeyboardButton(text="📞 Aloqa")]
    ],
    resize_keyboard=True
)

phone_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        f"HR_GROUP_ID: {HR_GROUP_ID}\n"
        f"Siz yozgan chat ID: {message.chat.id}",
        reply_markup=menu
    )


@dp.message()
async def main_handler(message: Message):
    user_id = message.from_user.id
    text = message.text

    if text == "📝 Ariza topshirish":
        user_data[user_id] = {"step": "full_name"}
        await message.answer("👤 Ism familiyangizni yozing:")
        return

    if text == "📞 Aloqa":
        await message.answer("📞 HR telefon:\n+998 50 003 26 55")
        return

    if user_id in user_data:
        step = user_data[user_id]["step"]

        if step == "full_name":
            user_data[user_id]["full_name"] = text
            user_data[user_id]["step"] = "age"
            await message.answer("🎂 Yoshingizni yozing:")
            return

        if step == "age":
            user_data[user_id]["age"] = text
            user_data[user_id]["step"] = "phone"
            await message.answer(
                "📞 Telefon raqamingizni yuboring:",
                reply_markup=phone_menu
            )
            return

        if step == "phone":
            if message.contact:
                user_data[user_id]["phone"] = message.contact.phone_number
            else:
                user_data[user_id]["phone"] = text

            user_data[user_id]["step"] = "position"
            await message.answer(
                "💼 Qaysi lavozimga topshiryapsiz?",
                reply_markup=menu
            )
            return

        if step == "position":
            user_data[user_id]["position"] = text
            user_data[user_id]["step"] = "experience"
            await message.answer("📌 Ish tajribangizni yozing:")
            return

        if step == "experience":
            user_data[user_id]["experience"] = text
            user_data[user_id]["step"] = "resume"
            await message.answer(
                "📎 Resume/CV faylingizni yuboring.\n"
                "PDF, DOCX yoki rasm yuborishingiz mumkin.\n\n"
                "Agar resume yo‘q bo‘lsa: Yo‘q deb yozing."
            )
            return

        if step == "resume":
            try:
                application = user_data[user_id]

                hr_text = (
                    "🆕 YANGI ARIZA\n\n"
                    f"👤 Ism: {application['full_name']}\n"
                    f"🎂 Yosh: {application['age']}\n"
                    f"📞 Telefon: {application['phone']}\n"
                    f"💼 Lavozim: {application['position']}\n"
                    f"📌 Tajriba: {application['experience']}"
                )

                await bot.send_message(chat_id=HR_GROUP_ID, text=hr_text)

                if message.document:
                    await bot.send_document(
                        chat_id=HR_GROUP_ID,
                        document=message.document.file_id,
                        caption="📎 Nomzod resume/CV fayli"
                    )

                elif message.photo:
                    await bot.send_photo(
                        chat_id=HR_GROUP_ID,
                        photo=message.photo[-1].file_id,
                        caption="📎 Nomzod resume rasmi"
                    )

                else:
                    await bot.send_message(
                        chat_id=HR_GROUP_ID,
                        text=f"📎 Resume/CV: {text}"
                    )

                await message.answer(
                    "✅ Arizangiz HR guruhga yuborildi!",
                    reply_markup=menu
                )

                del user_data[user_id]
                return

            except Exception as error:
                await message.answer(f"❌ Xatolik bo‘ldi:\n{error}")
                return

    await message.answer(
        "Pastdagi tugmalardan foydalaning 👇",
        reply_markup=menu
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
