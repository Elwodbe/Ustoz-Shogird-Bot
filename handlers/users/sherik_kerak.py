from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.shogird import SherikState
from keyboards.inline.hudud import kb
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    InlineKeyboardMarkup, InlineKeyboardButton
)

router = Router()
ADMINS = [6510725580]
CHANNEL_ID = -1002843291457

# Tasdiqlash uchun reply keyboard (foydalanuvchiga)
tasdiqlash_buttons = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Ha"), KeyboardButton(text="Yo‘q")]],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Admin uchun inline keyboard
kanalga_joylash_uchun_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="kanalga_ha"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="kanalga_yoq")
        ]
    ]
)


@router.message(F.text == "Sherik kerak")
async def sherik_kerak(message: types.Message, state: FSMContext):
    await message.answer("""<b>Sherik topish uchun ariza berish</b>\n
Hozir sizga birnecha savollar beriladi.
Har biriga javob bering. 
Oxirida agar hammasi to‘g‘ri bo‘lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.""", parse_mode="HTML")
    await message.answer("<b>Ism, familiyangizni kiriting?</b>", parse_mode="HTML")
    await state.set_state(SherikState.name)


@router.message(SherikState.name)
async def texnologiya(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📚 Texnologiyalarni kiriting (masalan: Java, C++):")
    await state.set_state(SherikState.texnologiya)


@router.message(SherikState.texnologiya)
async def aloqa(message: types.Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    await message.answer("📞 <b>Aloqa raqamingizni kiriting</b>", parse_mode="HTML")
    await state.set_state(SherikState.aloqa)


@router.message(SherikState.aloqa)
async def hudud(message: types.Message, state: FSMContext):
    await state.update_data(aloqa=message.text)
    await message.answer("🌐 <b>Hudud:</b> Quyidagilardan birini tanlang:", reply_markup=kb, parse_mode="HTML")
    await state.set_state(SherikState.hudud)


@router.callback_query(F.data.startswith("hudud_"))
async def process_hudud_callback(callback: types.CallbackQuery, state: FSMContext):
    hudud_nomi = callback.data.split("_")[1]
    await state.update_data(hudud=hudud_nomi)
    await callback.message.answer("💰 <b>Narxi (summa yoki Tekin)</b>", parse_mode="HTML")
    await state.set_state(SherikState.narxi)
    await callback.answer()


@router.message(SherikState.narxi)
async def kasb(message: types.Message, state: FSMContext):
    await state.update_data(narxi=message.text)
    await message.answer("👨🏻‍💻 <b>Kasbingiz (Talaba, Ishchi va h.k.)</b>", parse_mode="HTML")
    await state.set_state(SherikState.kasb)


@router.message(SherikState.kasb)
async def murojat(message: types.Message, state: FSMContext):
    await state.update_data(kasb=message.text)
    await message.answer("🕰 <b>Murojaat qilish vaqti (masalan: 9:00 - 18:00)</b>", parse_mode="HTML")
    await state.set_state(SherikState.murojat_qilish_vaqti)


@router.message(SherikState.murojat_qilish_vaqti)
async def maqsad(message: types.Message, state: FSMContext):
    await state.update_data(murojat_qilish_vaqti=message.text)
    await message.answer("🔎 <b>Maqsadingizni qisqacha yozing</b>", parse_mode="HTML")
    await state.set_state(SherikState.maqsad)


@router.message(SherikState.maqsad)
async def confirm(message: types.Message, state: FSMContext):
    await state.update_data(maqsad=message.text)
    data = await state.get_data()
    username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"

    text = f"""<b>Sherik kerak:</b>

🏅 <b>Sherik:</b> {data.get("name")}
📚 <b>Texnologiya:</b> {data.get("texnologiya")}
📞 <b>Telegram:</b> {username}
☎️ <b>Aloqa:</b> {data.get("aloqa")}
🌐 <b>Hudud:</b> {data.get("hudud")}
💰 <b>Narxi:</b> {data.get("narxi")}
👨🏻‍💻 <b>Kasbi:</b> {data.get("kasb")}
🕰 <b>Murojaat vaqti:</b> {data.get("murojat_qilish_vaqti")}
🔎 <b>Maqsad:</b> {data.get("maqsad")}

#sherik"""

    await message.answer(text, parse_mode="HTML")
    await message.answer("Barcha ma'lumotlar to‘g‘rimi?", reply_markup=tasdiqlash_buttons)
    await state.set_state(SherikState.confirm)


@router.message(SherikState.confirm)
async def send_to_admin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"

    if message.text == "Ha":
        text = f"""<b>✅ Yangi Sherik Arizasi</b>

🏅 <b>Sherik:</b> {data.get("name")}
📚 <b>Texnologiya:</b> {data.get("texnologiya")}
📞 <b>Telegram:</b> {username}
☎️ <b>Aloqa:</b> {data.get("aloqa")}
🌐 <b>Hudud:</b> {data.get("hudud")}
💰 <b>Narxi:</b> {data.get("narxi")}
👨🏻‍💻 <b>Kasbi:</b> {data.get("kasb")}
🕰 <b>Murojaat vaqti:</b> {data.get("murojat_qilish_vaqti")}
🔎 <b>Maqsad:</b> {data.get("maqsad")}

<b>Kanalga joylashtiraymi?</b>"""

        for admin in ADMINS:
            await message.bot.send_message(
                chat_id=admin,
                text=text,
                reply_markup=kanalga_joylash_uchun_btn,
                parse_mode="HTML"
            )

        await message.answer("✅ Arizangiz adminga yuborildi.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("❌ Ariza bekor qilindi.", reply_markup=ReplyKeyboardRemove())

    await state.clear()


@router.callback_query(F.data.in_({"kanalga_ha", "kanalga_yoq"}))
async def handle_channel_post(callback: types.CallbackQuery):
    if callback.data == "kanalga_ha":
        await callback.bot.send_message(
            chat_id=CHANNEL_ID,
            text=callback.message.text,
            parse_mode="HTML"
        )
        await callback.message.edit_text(callback.message.text + "\n\n✅ Kanalga yuborildi.")
        await callback.answer("Kanalga yuborildi.")
    else:
        await callback.message.edit_text(callback.message.text + "\n\n❌ Kanalga yuborilmadi.")
        await callback.answer("Bekor qilindi.")
