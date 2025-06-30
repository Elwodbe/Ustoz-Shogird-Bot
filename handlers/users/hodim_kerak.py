from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.shogird import XodimState
from keyboards.inline.hudud import kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

ADMINS = [6510725580]
KANAL_ID = -1002123456789  # <-- o'z kanal ID'ingizni yozing

tasdiqlash_buttons = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Ha"), KeyboardButton(text="Yo‘q")]],
    resize_keyboard=True,
    one_time_keyboard=True
)

tasdiq_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="hodim_tasdiqla")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="hodim_bekor")]
    ]
)

@router.message(F.text == "Hodim kerak")
async def hodim_kerak(message: types.Message, state: FSMContext):
    await message.answer("""<b>Xodim topish uchun ariza berish</b>\n
Hozir sizga birnecha savollar beriladi.
Har biriga javob bering.
Oxirida agar hammasi to‘g‘ri bo‘lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.""", parse_mode="HTML")
    await message.answer("🎓 Idora nomi?")
    await state.set_state(XodimState.idora_nomi)

@router.message(XodimState.idora_nomi)
async def texnologiya(message: types.Message, state: FSMContext):
    await state.update_data(idora_name=message.text)
    await message.answer("""📚 <b>Texnologiya:</b>\nTalab qilinadigan texnologiyalar?\nMasalan: Java, C++""", parse_mode="HTML")
    await state.set_state(XodimState.texnologiya)

@router.message(XodimState.texnologiya)
async def aloqa(message: types.Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    await message.answer("📞 <b>Aloqa:</b>\nTelefon raqamingiz?", parse_mode="HTML")
    await state.set_state(XodimState.aloqa)

@router.message(XodimState.aloqa)
async def hudud(message: types.Message, state: FSMContext):
    await state.update_data(aloqa=message.text)
    await message.answer("🌐 <b>Hudud:</b>\nQaysi viloyatdan?", reply_markup=kb, parse_mode="HTML")
    await state.set_state(XodimState.hudud)

@router.callback_query(F.data.startswith("hudud_"))
async def masul(callback: types.CallbackQuery, state: FSMContext):
    hudud = callback.data.split("_")[1]
    await state.update_data(hudud=hudud)
    await callback.message.answer("✍️ Mas'ul ism sharifi?")
    await state.set_state(XodimState.masul_ism_sharifi)
    await callback.answer()

@router.message(XodimState.masul_ism_sharifi)
async def murojat_vaqti(message: types.Message, state: FSMContext):
    await state.update_data(masul_ism_sharifi=message.text)
    await message.answer("🕰 Murojaat vaqti?")
    await state.set_state(XodimState.murojat_qilish_vaqti)

@router.message(XodimState.murojat_qilish_vaqti)
async def ish_vaqti(message: types.Message, state: FSMContext):
    await state.update_data(murojat_qilish_vaqti=message.text)
    await message.answer("🕰 Ish vaqti?")
    await state.set_state(XodimState.ish_vaqti)

@router.message(XodimState.ish_vaqti)
async def maosh(message: types.Message, state: FSMContext):
    await state.update_data(ish_vaqti=message.text)
    await message.answer("💰 Maosh?")
    await state.set_state(XodimState.maosh)

@router.message(XodimState.maosh)
async def qoshimcha(message: types.Message, state: FSMContext):
    await state.update_data(maosh=message.text)
    await message.answer("‼️ Qo‘shimcha ma‘lumotlar?")
    await state.set_state(XodimState.qoshimcha_malumotlar)

@router.message(XodimState.qoshimcha_malumotlar)
async def confirm(message: types.Message, state: FSMContext):
    await state.update_data(qoshimcha_malumotlar=message.text)
    data = await state.get_data()
    username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"

    text = f"""<b>Xodim kerak:</b>
🏢 <b>Idora:</b> {data.get("idora_name")}
📚 <b>Texnologiya:</b> {data.get("texnologiya")}
🇺🇿 <b>Telegram:</b> {username}
📞 <b>Aloqa:</b> {data.get("aloqa")}
🌐 <b>Hudud:</b> {data.get("hudud")}
✍️ <b>Mas'ul:</b> {data.get("masul_ism_sharifi")}
🕰 <b>Murojaat vaqti:</b> {data.get("murojat_qilish_vaqti")}
🕰 <b>Ish vaqti:</b> {data.get("ish_vaqti")}
💰 <b>Maosh:</b> {data.get("maosh")}
‼️ <b>Qo‘shimcha:</b> {data.get("qoshimcha_malumotlar")}

#hodimkerak"""

    await message.answer(text, parse_mode="HTML")
    await message.answer("Barcha ma'lumotlar to‘g‘rimi?", reply_markup=tasdiqlash_buttons)
    await state.set_state(XodimState.confirm)

@router.message(XodimState.confirm)
async def send_to_admin(message: types.Message, state: FSMContext):
    if message.text == "Ha":
        data = await state.get_data()
        username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"

        text = f"""<b>✅ Yangi Xodim kerak So‘rovi</b>

🏢 <b>Idora:</b> {data.get("idora_name")}
📚 <b>Texnologiya:</b> {data.get("texnologiya")}
🇺🇿 <b>Telegram:</b> {username}
📞 <b>Aloqa:</b> {data.get("aloqa")}
🌐 <b>Hudud:</b> {data.get("hudud")}
✍️ <b>Mas'ul:</b> {data.get("masul_ism_sharifi")}
🕰 <b>Murojaat vaqti:</b> {data.get("murojat_qilish_vaqti")}
🕰 <b>Ish vaqti:</b> {data.get("ish_vaqti")}
💰 <b>Maosh:</b> {data.get("maosh")}
‼️ <b>Qo‘shimcha:</b> {data.get("qoshimcha_malumotlar")}"""

        for admin in ADMINS:
            await message.bot.send_message(admin, text, reply_markup=tasdiq_inline, parse_mode="HTML")
        await message.answer("✅ Arizangiz adminga yuborildi.", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer("❌ Ariza bekor qilindi.", reply_markup=ReplyKeyboardRemove())
        await state.clear()

@router.callback_query(F.data == "hodim_tasdiqla")
async def tasdiqlash(callback: types.CallbackQuery):
    await callback.answer("✅ Kanalga yuborildi!")
    await callback.message.bot.send_message(KANAL_ID, callback.message.html_text, parse_mode="HTML")
    await callback.message.edit_reply_markup()

@router.callback_query(F.data == "hodim_bekor")
async def bekor(callback: types.CallbackQuery):
    await callback.answer("❌ Bekor qilindi")
    await callback.message.edit_reply_markup()
