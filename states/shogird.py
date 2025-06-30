from aiogram.fsm.state import StatesGroup, State

class SherikState(StatesGroup):
    name = State()
    texnologiya = State()
    aloqa = State()
    hudud = State()
    narxi = State()
    kasb = State()
    murojat_qilish_vaqti = State()
    maqsad = State()
    confirm = State()


class IshState(StatesGroup):
    name = State()
    yosh = State()
    texnologiya = State()
    aloqa = State()
    hudud = State()
    narxi = State()
    kasb = State()
    murojat_qilish_vaqti = State()
    maqsad = State()
    confirm = State()

class XodimState(StatesGroup):
    idora_nomi = State()
    texnologiya = State()
    aloqa = State()
    hudud = State()
    masul_ism_sharifi = State()
    murojat_qilish_vaqti = State()
    ish_vaqti = State()
    maosh = State()
    qoshimcha_malumotlar = State()
    confirm = State()

class UstozState(StatesGroup):
    name = State()
    yosh = State()
    texnologiya = State()
    aloqa = State()
    hudud = State()
    narxi = State()
    kasbi = State()
    murojat_qilish_vaqti = State()
    maqsad = State()
    confirm = State()

class ShogirdState(StatesGroup):
    name = State()
    yosh = State()
    texnologiya = State()
    aloqa = State()
    hudud = State()
    narxi = State()
    kasbi = State()
    murojat_qilish_vaqti = State()
    maqsad = State()
    confirm = State()
    
