from aiogram import types, F, Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

from aiogram.types import Message

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import types

import config

router = Router()
subscribed_users = {}


@router.message(Command("subscribe"))
async def subscribe_handler(msg: Message):
    user_id = msg.from_user.id
    subscribed_users[user_id] = True  # Подписываем пользователя
    await msg.answer("Ты подписался на уведомления!")


@router.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id in config.admin_id:
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton("Установить команды №1", callback_data="11"),
                     InlineKeyboardButton("Установить команды №2", callback_data="22"))

        await message.answer("Выберите действие:", reply_markup=keyboard)
    else:
        # todo:
        #  проверить, что человек подписался
        #  Если не подписался выдать кнопку подписаться
        #   Если подписан выдать кнопку отписаться
        await message.answer("Вы не админ")


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")
