from aiogram.filters import Command
from aiogram import types, Router
from aiogram.fsm.context import FSMContext

import config
import user_interface
import keyboards
import db

router = Router()


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    if user_id in config.admin_id:
        await message.answer("Выберите действие:", reply_markup=keyboards.ADMIN_KB)
    else:
        if db.is_user_id_in_db(user_id):
            await message.answer(
                user_interface.TEXT_UNSUBSCRIBE,
                reply_markup=keyboards.NEGATION)
        else:
            await message.answer(
                user_interface.TEXT_AGREE,
                reply_markup=keyboards.AGREEMENT)


@router.message(Command("id"))
async def id_handler(msg: types.Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")


@router.message()
async def message_handler(msg: types.Message):
    await msg.answer('Извините, я пока ещё не знаю такую команду')
