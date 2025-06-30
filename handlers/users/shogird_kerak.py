from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.shogird import ShogirdState
from keyboards.inline.hudud import kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()
ADMINS = [6510725580]
CHANNEL_ID = -1002843291457  # Kanal ID

tasdiqlash_buttons = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Ha"), KeyboardButton(text="Yo‘q")]],
    resize_keyboard=True,
    one_time_keyboard=True
)

kanalga_joylash_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="shogird_ha"),
            InlineKeyboardButton(text="❌ Yo‘q", callback_data="shogird_yoq"),
        ]
    ]
)

@router.message(F.text == "Shogird kerak")
async def shogird_kerak(message: types.Message, state: FSMContext):
    await message.answer("""<b>Shogird topish uchun ariza berish</b>

Hozir sizga birnecha savollar beriladi. 
Har biriga javob bering. 
Oxirida agar hammasi to‘g‘ri bo‘lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.""", parse_mode="HTML")
    await message.answer("<b>Ism, familiyangizni kiriting?</b>", parse_mode="HTML")
    await state.set_state(ShogirdState.name)

@router.message(ShogirdState.name)
async def yosh(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🕑 <b>Yosh:</b>\nMasalan, 19", parse_mode="HTML")
    await state.set_state(ShogirdState.yosh)

@router.message(ShogirdState.yosh)
async def texnologiya(message: types.Message, state: FSMContext):
    await state.update_data(yosh=message.text)
    await message.answer("📚 <b>Yo‘nalish:</b>\nMasalan, Python, SMM, Grafika dizayn", parse_mode="HTML")
    await state.set_state(ShogirdState.texnologiya)

@router.message(ShogirdState.texnologiya)
async def aloqa(message: types.Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    await message.answer("📞 <b>Aloqa:</b>\nMasalan, +998 90 123 45 67", parse_mode="HTML")
    await state.set_state(ShogirdState.aloqa)

@router.message(ShogirdState.aloqa)
async def hudud(message: types.Message, state: FSMContext):
    await state.update_data(aloqa=message.text)
    await message.answer("🌐 <b>Hudud:</b>\nTanlang", reply_markup=kb, parse_mode="HTML")
    await state.set_state(ShogirdState.hudud)

@router.callback_query(F.data.startswith("hudud_"))
async def narx(callback: types.CallbackQuery, state: FSMContext):
    hudud_nomi = callback.data.split("_")[1]
    await state.update_data(hudud=hudud_nomi)
    await callback.message.answer("💰 <b>Narxi:</b>\nTekin yoki narx kiriting", parse_mode="HTML")
    await state.set_state(ShogirdState.narxi)
    await callback.answer()

@router.message(ShogirdState.narxi)
async def kasb(message: types.Message, state: FSMContext):
    await state.update_data(narx=message.text)
    await message.answer("👨🏻‍💻 <b>Kasbingiz:</b>\nMasalan, Ustoz", parse_mode="HTML")
    await state.set_state(ShogirdState.kasbi)

@router.message(ShogirdState.kasbi)
async def murojat_qilish_vaqti(message: types.Message, state: FSMContext):
    await state.update_data(kasb=message.text)
    await message.answer("🕰 <b>Murojaat vaqti:</b>\nMasalan, 9:00 - 18:00", parse_mode="HTML")
    await state.set_state(ShogirdState.murojat_qilish_vaqti)

@router.message(ShogirdState.murojat_qilish_vaqti)
async def maqsad(message: types.Message, state: FSMContext):
    await state.update_data(murojat_qilish_vaqti=message.text)
    await message.answer("🔎 <b>Maqsad:</b>\nQanday shogird kerak?", parse_mode="HTML")
    await state.set_state(ShogirdState.maqsad)

@router.message(ShogirdState.maqsad)
async def confirm(message: types.Message, state: FSMContext):
    await state.update_data(maqsad=message.text)
    data = await state.get_data()
    username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"

    text = f"""<b>Shogird kerak:</b>

🏅 <b>Ismi:</b> {data.get("name")}
🕑 <b>Yosh:</b> {data.get("yosh")}
📚 <b>Yo‘nalish:</b> {data.get("texnologiya")}
📞 <b>Telegram:</b> {username}
☎️ <b>Aloqa:</b> {data.get("aloqa")}
🌐 <b>Hudud:</b> {data.get("hudud")}
💰 <b>Narxi:</b> {data.get("narx")}
👨🏻‍💻 <b>Kasbi:</b> {data.get("kasb")}
🕰 <b>Murojaat vaqti:</b> {data.get("murojat_qilish_vaqti")}
🔎 <b>Maqsad:</b> {data.get("maqsad")}

#shogird
"""
    await message.answer(text, parse_mode="HTML")
    await message.answer("Barcha ma'lumotlar to‘g‘rimi?", reply_markup=tasdiqlash_buttons)
    await state.set_state(ShogirdState.confirm)

@router.message(ShogirdState.confirm)
async def send_to_admin(message: types.Message, state: FSMContext):
    if message.text == "Ha":
        data = await state.get_data()
        username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"

        text = f"""<b>✅ Yangi Shogird So‘rovi</b>

🏅 <b>Ismi:</b> {data.get("name")}
🕑 <b>Yosh:</b> {data.get("yosh")}
📚 <b>Yo‘nalish:</b> {data.get("texnologiya")}
📞 <b>Telegram:</b> {username}
☎️ <b>Aloqa:</b> {data.get("aloqa")}
🌐 <b>Hudud:</b> {data.get("hudud")}
💰 <b>Narxi:</b> {data.get("narx")}
👨🏻‍💻 <b>Kasbi:</b> {data.get("kasb")}
🕰 <b>Murojaat vaqti:</b> {data.get("murojat_qilish_vaqti")}
🔎 <b>Maqsad:</b> {data.get("maqsad")}
"""

        for admin in ADMINS:
            await message.bot.send_message(admin, text, reply_markup=kanalga_joylash_inline, parse_mode="HTML")

        await message.answer("✅ Arizangiz adminga yuborildi.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("❌ Ariza bekor qilindi.", reply_markup=ReplyKeyboardRemove())

    await state.clear()

# 🔽 Inline tugma callbacklar
@router.callback_query(F.data.in_(["shogird_ha", "shogird_yoq"]))
async def kanalga_joylash(callback: types.CallbackQuery):
    if callback.data == "shogird_ha":
        await callback.answer("✅ Kanalga yuborildi.")
        await callback.bot.send_message(CHANNEL_ID, callback.message.text, parse_mode="HTML")
    else:
        await callback.answer("❌ Bekor qilindi.")
