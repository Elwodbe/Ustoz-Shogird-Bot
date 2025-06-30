from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.shogird import IshState
from keyboards.inline.hudud import kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

ADMINS = [6510725580]
KANAL_ID = -1002123456789  # <-- bu yerga o‘zingizning kanal ID'ingizni yozing (minusli)

tasdiqlash_buttons = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Ha"), KeyboardButton(text="Yo‘q")]],
    resize_keyboard=True,
    one_time_keyboard=True
)

tasdiq_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="ish_tasdiqla")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="ish_bekor")]
    ]
)

@router.message(F.text == "Ish joyi kerak")
async def ish_kerak(message: types.Message, state: FSMContext):
    await message.answer("""<b>Ish joyi topish uchun ariza berish</b>

Hozir sizga birnecha savollar beriladi. 
Har biriga javob bering. 
Oxirida agar hammasi to‘g‘ri bo‘lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.""", parse_mode="HTML")
    await message.answer("<b>Ism, familiyangizni kiriting?</b>", parse_mode="HTML")
    await state.set_state(IshState.name)

@router.message(IshState.name)
async def yosh(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🕑 <b>Yosh:</b>\n\nYoshingizni kiriting?\nMasalan: 23", parse_mode="HTML")
    await state.set_state(IshState.yosh)

@router.message(IshState.yosh)
async def texnologiya(message: types.Message, state: FSMContext):
    await state.update_data(yosh=message.text)
    await message.answer("📚 <b>Texnologiya:</b>\n\nMasalan: Python, Django", parse_mode="HTML")
    await state.set_state(IshState.texnologiya)

@router.message(IshState.texnologiya)
async def aloqa(message: types.Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    await message.answer("📞 <b>Aloqa:</b>\n\nBog‘lanish uchun raqamingiz?", parse_mode="HTML")
    await state.set_state(IshState.aloqa)

@router.message(IshState.aloqa)
async def hudud(message: types.Message, state: FSMContext):
    await state.update_data(aloqa=message.text)
    await message.answer("🌐 <b>Hudud:</b>\n\nQaysi viloyatdan?", reply_markup=kb, parse_mode="HTML")
    await state.set_state(IshState.hudud)

@router.callback_query(F.data.startswith("hudud_"))
async def narx(callback: types.CallbackQuery, state: FSMContext):
    hudud = callback.data.split("_")[1]
    await state.update_data(hudud=hudud)
    await callback.message.answer("💰 <b>Narxi:</b>\n\nTo‘lov qilasizmi yoki tekinmi?", parse_mode="HTML")
    await state.set_state(IshState.narxi)
    await callback.answer()

@router.message(IshState.narxi)
async def kasb(message: types.Message, state: FSMContext):
    await state.update_data(narxi=message.text)
    await message.answer("👨🏻‍💻 <b>Kasbingiz:</b>\n\nMasalan: Talaba", parse_mode="HTML")
    await state.set_state(IshState.kasb)

@router.message(IshState.kasb)
async def murojat_vaqti(message: types.Message, state: FSMContext):
    await state.update_data(kasb=message.text)
    await message.answer("🕰 <b>Murojaat vaqti:</b>\n\nQachon bog‘lanish mumkin?", parse_mode="HTML")
    await state.set_state(IshState.murojat_qilish_vaqti)

@router.message(IshState.murojat_qilish_vaqti)
async def maqsad(message: types.Message, state: FSMContext):
    await state.update_data(murojat_qilish_vaqti=message.text)
    await message.answer("🔎 <b>Maqsad:</b>\n\nQisqacha yozing", parse_mode="HTML")
    await state.set_state(IshState.maqsad)

@router.message(IshState.maqsad)
async def confirm(message: types.Message, state: FSMContext):
    await state.update_data(maqsad=message.text)
    data = await state.get_data()
    username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"

    matn = f"""<b>Ish joyi kerak:</b>

🏅 <b>Ismi:</b> {data.get("name")}
🕑 <b>Yosh:</b> {data.get("yosh")}
📚 <b>Texnologiya:</b> {data.get("texnologiya")}
📞 <b>Telegram:</b> {username}
☎️ <b>Aloqa:</b> {data.get("aloqa")}
🌐 <b>Hudud:</b> {data.get("hudud")}
💰 <b>Narxi:</b> {data.get("narxi")}
👨🏻‍💻 <b>Kasbi:</b> {data.get("kasb")}
🕰 <b>Murojaat vaqti:</b> {data.get("murojat_qilish_vaqti")}
🔎 <b>Maqsad:</b> {data.get("maqsad")}

#ishjoyi
"""
    await message.answer(matn, parse_mode="HTML")
    await message.answer("Barcha ma'lumotlar to‘g‘rimi?", reply_markup=tasdiqlash_buttons)
    await state.set_state(IshState.confirm)

@router.message(IshState.confirm)
async def admin_tasdiqlov(message: types.Message, state: FSMContext):
    if message.text == "Ha":
        data = await state.get_data()
        username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"

        text = f"""<b>✅ Yangi Ish Joyi So‘rovi</b>

🏅 <b>Ismi:</b> {data.get("name")}
🕑 <b>Yosh:</b> {data.get("yosh")}
📚 <b>Texnologiya:</b> {data.get("texnologiya")}
📞 <b>Telegram:</b> {username}
☎️ <b>Aloqa:</b> {data.get("aloqa")}
🌐 <b>Hudud:</b> {data.get("hudud")}
💰 <b>Narxi:</b> {data.get("narxi")}
👨🏻‍💻 <b>Kasbi:</b> {data.get("kasb")}
🕰 <b>Murojaat vaqti:</b> {data.get("murojat_qilish_vaqti")}
🔎 <b>Maqsad:</b> {data.get("maqsad")}
"""
        for admin in ADMINS:
            await message.bot.send_message(admin, text, reply_markup=tasdiq_inline, parse_mode="HTML")

        await message.answer("✅ Arizangiz adminga yuborildi.", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer("❌ Ariza bekor qilindi.", reply_markup=ReplyKeyboardRemove())
        await state.clear()

@router.callback_query(F.data == "ish_tasdiqla")
async def tasdiqlash(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("✅ Kanalga yuborildi!")
    await callback.message.bot.send_message(KANAL_ID, callback.message.html_text, parse_mode="HTML")
    await callback.message.edit_reply_markup()  # Tugmalarni olib tashlash

@router.callback_query(F.data == "ish_bekor")
async def bekor_qilish(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_caption("<b>❌ So‘rov bekor qilindi</b>", parse_mode="HTML")
    await callback.answer("Bekor qilindi.")
