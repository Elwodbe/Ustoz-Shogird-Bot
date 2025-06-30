from loader import dp,bot
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
import asyncio
from handlers.users.start import router
from handlers.users.help import router as help_router
from handlers.users.sherik_kerak import router as sherik_kerak
from handlers.users.ish_joyi import router as ish_kerak
from handlers.users.hodim_kerak import router as hodim_kerak
from handlers.users.ustoz_kerak import router as ustoz_kerak
from handlers.users.shogird_kerak import router as shogird_kerak

async def main():
    await set_default_commands(bot)
    await on_startup_notify(bot)
    
    dp.include_router(router)
    dp.include_router(help_router)
    dp.include_router(sherik_kerak)
    dp.include_router(ish_kerak)
    dp.include_router(hodim_kerak)
    dp.include_router(ustoz_kerak)
    dp.include_router(shogird_kerak)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())