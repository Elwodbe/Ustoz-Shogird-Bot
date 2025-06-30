from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Farg'ona", callback_data="hudud_Fargona"),
            InlineKeyboardButton(text="Andijon", callback_data="hudud_Andijon"),
        ],
        [
            InlineKeyboardButton(text="Namangan", callback_data="hudud_Namangan"),
            InlineKeyboardButton(text="Buxoro", callback_data="hudud_Buxoro"),
        ],
        [
            InlineKeyboardButton(text="Sirdaryo", callback_data="hudud_Sirdaryo"),
            InlineKeyboardButton(text="Samarqand", callback_data="hudud_Samarqand"),
        ],
        [
            InlineKeyboardButton(text="Toshkent", callback_data="hudud_Toshkent"),
            InlineKeyboardButton(text="Qoraqalpoqiston", callback_data="hudud_Qoraqalpoqiston"),
        ],
        [
            InlineKeyboardButton(text="Jizzax", callback_data="hudud_Jizzax"),
            InlineKeyboardButton(text="Navoiy", callback_data="hudud_Navoiy"),
        ],
        [
            InlineKeyboardButton(text="Surxondaryo", callback_data="hudud_Surxondaryo"),
            InlineKeyboardButton(text="Qashqadaryo", callback_data="hudud_Qashqadaryo"),
        ]
    ]
)
