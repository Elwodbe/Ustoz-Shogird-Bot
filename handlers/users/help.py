from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command(commands=["help"]))
async def bot_help(message: types.Message):
    text = (
        "Buyruqlar:",
        "/start - Botni ishga tushirish",
        """/help - UzGeeks faollari tomonidan tuzilgan Ustoz-Shogird kanali. 

            Bu yerda Programmalash bo`yicha
            <a>#Ustoz</a>,  
            <a>#Shogird</a>,
            <a>#oquvKursi</a>,
            <a>#Sherik</a>,  
            <a>#Xodim</a> va
            <a>#IshJoyi</a> 
            topishingiz mumkin. 

            E'lon berish: <a>@UstozShogirdBot</a>

            Admin <a>@https://t.me/tee_12111</a>"""
    )
    await message.answer("\n".join(text))
