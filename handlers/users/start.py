from aiogram import types, Router
from aiogram.filters import Command
from keyboards.default.default_button import kb

router = Router()

@router.message(Command(commands=["start"]))
async def bot_start(message: types.Message):
    await message.answer(
        f"<b>Assalom alaykum, {message.from_user.full_name}!</b>\n\n"
        "<b>UstozShogird kanalining rasmiy botiga xush kelibsiz!</b>\n\n"
        "👉 /help buyrug‘i orqali bot imkoniyatlari bilan tanishing.",
        reply_markup=kb
    )
