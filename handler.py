from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, CallbackQuery

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from aiogram import types

import config
import utils
import keyboards

router = Router()
subscribed_users = {}








@router.callback_query(StateFilter(None))
async def answer(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'new_admin':
        await callback.message.answer(
            text="Введите telegram id человека (он может узнать его написав нашему боту сообщение /id)")
        await state.set_state(utils.Admin.enter_new_admin_id)
    elif callback.data == 'new_deadline':
        await callback.message.answer("Добавляем дедлайн")


@router.message(utils.Admin.enter_new_admin_id)
async def new_admin(message: types.Message, state: FSMContext):
    new_admin_id = message.text
    if utils.valid_id(new_admin_id):
        config.admin_id.append(new_admin_id)
        await message.answer("Успешно добавлен новый администратор")
        await state.set_state(None)
        print("Валидный id") #todo del
    else:
        await message.answer("Telegram id состоит только из цифр, попробуйте ввести еще раз")
        #todo добавить кнопку отмены
        print("Ошибочный id") #todo del





@router.message(Command("subscribe"))
async def subscribe_handler(msg: Message):
    user_id = msg.from_user.id
    subscribed_users[user_id] = True  # Подписываем пользователя
    await msg.answer("Ты подписался на уведомления!")


@router.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id in config.admin_id:
        await message.answer("Выберите действие:", reply_markup=keyboards.ADMIN_KB)
    else:
        # todo:
        #  проверить, что человек подписался
        #  Если не подписался выдать кнопку подписаться
        #   Если подписан выдать кнопку отписаться
        await message.answer("Вы не админ")


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")
