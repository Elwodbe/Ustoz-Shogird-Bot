from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.shogird import UstozState
from keyboards.inline.hudud import kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()
ADMINS = [6510725580]
CHANNEL_ID = -1002843291457  # Ustoz arizalari kanal ID

# Foydalanuvchiga yuboriladigan tasdiqlash tugmalari
tasdiqlash_buttons = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Ha"), KeyboardButton(text="Yo‘q")]],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Adminga yuboriladigan inline tugmalar
kanalga_joylash_uchun_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="ustoz_ha"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="ustoz_yoq")
        ]
    ]
)


@router.message(F.text == "Ustoz kerak")
async def ustoz_kerak(message: types.Message, state: FSMContext):
    await message.answer("""<b>Ustoz topish uchun ariza berish</b>

Hozir sizga birnecha savollar beriladi. 
Har biriga javob bering. 
Oxirida agar hammasi to‘g‘ri bo‘lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.""", parse_mode="HTML")
    await message.answer("<b>Ism, familiyangizni kiriting?</b>", parse_mode="HTML")
    await state.set_state(UstozState.name)

@router.message(UstozState.name)
async def yosh(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🕑 <b>Yosh:</b>\n\nYoshingizni kiriting?\nMasalan, 19", parse_mode="HTML")
    await state.set_state(UstozState.yosh)

@router.message(UstozState.yosh)
async def texnologiya(message: types.Message, state: FSMContext):
    await state.update_data(yosh=message.text)
    await message.answer("📚 <b>Texnologiya:</b>\n\nTalab qilinadigan texnologiyalarni kiriting?\nMasalan: Python, Django", parse_mode="HTML")
    await state.set_state(UstozState.texnologiya)

@router.message(UstozState.texnologiya)
async def aloqa(message: types.Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    await message.answer("📞 <b>Aloqa:</b>\n\nBog‘lanish uchun raqamingizni kiriting?\nMasalan, +998 90 123 45 67", parse_mode="HTML")
    await state.set_state(UstozState.aloqa)

@router.message(UstozState.aloqa)
async def hudud(message: types.Message, state: FSMContext):
    await state.update_data(aloqa=message.text)
    await message.answer("🌐 <b>Hudud:</b>\n\nQaysi hududdansiz?", reply_markup=kb, parse_mode="HTML")
    await state.set_state(UstozState.hudud)

@router.callback_query(F.data.startswith("hudud_"))
async def narx(callback: types.CallbackQuery, state: FSMContext):
    hudud_nomi = callback.data.split("_")[1]
    await state.update_data(hudud=hudud_nomi)
    await callback.message.answer("💰 <b>Narxi:</b>\n\nTo‘lov qilasizmi yoki tekinmi?", parse_mode="HTML")
    await state.set_state(UstozState.narxi)
    await callback.answer()

@router.message(UstozState.narxi)
async def kasb(message: types.Message, state: FSMContext):
    await state.update_data(narx=message.text)
    await message.answer("👨🏻‍💻 <b>Kasbi:</b>\n\nIshlaysizmi yoki o‘qiysizmi?\nMasalan, Talaba", parse_mode="HTML")
    await state.set_state(UstozState.kasbi)

@router.message(UstozState.kasbi)
async def murojat_qilish_vaqti(message: types.Message, state: FSMContext):
    await state.update_data(kasb=message.text)
    await message.answer("🕰 <b>Murojaat qilish vaqti:</b>\n\nMasalan, 9:00 - 18:00", parse_mode="HTML")
    await state.set_state(UstozState.murojat_qilish_vaqti)

@router.message(UstozState.murojat_qilish_vaqti)
async def maqsad(message: types.Message, state: FSMContext):
    await state.update_data(murojat_qilish_vaqti=message.text)
    await message.answer("🔎 <b>Maqsad:</b>\n\nMaqsadingizni qisqacha yozing", parse_mode="HTML")
    await state.set_state(UstozState.maqsad)

@router.message(UstozState.maqsad)
async def confirm(message: types.Message, state: FSMContext):
    await state.update_data(maqsad=message.text)
    data = await state.get_data()
    username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"

    text = f"""<b>Ustoz kerak:</b>

🏅 <b>Ismi:</b> {data.get("name")}
🕑 <b>Yosh:</b> {data.get("yosh")}
📚 <b>Texnologiya:</b> {data.get("texnologiya")}
📞 <b>Telegram:</b> {username}
☎️ <b>Aloqa:</b> {data.get("aloqa")}
🌐 <b>Hudud:</b> {data.get("hudud")}
💰 <b>Narxi:</b> {data.get("narx")}
👨🏻‍💻 <b>Kasbi:</b> {data.get("kasb")}
🕰 <b>Murojaat vaqti:</b> {data.get("murojat_qilish_vaqti")}
🔎 <b>Maqsad:</b> {data.get("maqsad")}

#ustoz
"""

    await message.answer(text, parse_mode="HTML")
    await message.answer("Barcha ma'lumotlar to‘g‘rimi?", reply_markup=tasdiqlash_buttons)
    await state.set_state(UstozState.confirm)

@router.message(UstozState.confirm)
async def send_to_admin(message: types.Message, state: FSMContext):
    if message.text == "Ha":
        data = await state.get_data()
        username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"

        text = f"""<b>✅ Yangi Ustoz So‘rovi</b>

🏅 <b>Ismi:</b> {data.get("name")}
🕑 <b>Yosh:</b> {data.get("yosh")}
📚 <b>Texnologiya:</b> {data.get("texnologiya")}
📞 <b>Telegram:</b> {username}
☎️ <b>Aloqa:</b> {data.get("aloqa")}
🌐 <b>Hudud:</b> {data.get("hudud")}
💰 <b>Narxi:</b> {data.get("narx")}
👨🏻‍💻 <b>Kasbi:</b> {data.get("kasb")}
🕰 <b>Murojaat vaqti:</b> {data.get("murojat_qilish_vaqti")}
🔎 <b>Maqsad:</b> {data.get("maqsad")}

<b>Kanalga joylashtiraymi?</b>
"""

        for admin in ADMINS:
            await message.bot.send_message(
                admin,
                text=text,
                reply_markup=kanalga_joylash_uchun_btn,
                parse_mode="HTML"
            )

        await message.answer("✅ Arizangiz adminga yuborildi.", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("❌ Ariza bekor qilindi.", reply_markup=ReplyKeyboardRemove())

    await state.clear()

@router.callback_query(F.data.in_({"ustoz_ha", "ustoz_yoq"}))
async def handle_channel_post(callback: types.CallbackQuery):
    if callback.data == "ustoz_ha":
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
