from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import config
import user_interface

router = Router()


@router.message(Command("subscribe"))
async def subscribe_handler(msg: Message):
    user_id = msg.from_user.id
    # Подписываем пользователя
    await msg.answer("Ты подписался на уведомления!")


users_test = {}


@router.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id in config.admin_id:
        # todo file admin
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton("Установить команды №1", callback_data="11"),
                     InlineKeyboardButton("Установить команды №2", callback_data="22"))

        await message.answer("Выберите действие:", reply_markup=keyboard)
    else:
        if users_test.get(user_id) is not None:
            import user_interface
            await message.answer(
                user_interface.TEXT_UNSUBSCRIBE,
                reply_markup=user_interface.NEGATION)
        else:
            import user_interface
            await message.answer(
                user_interface.TEXT_AGREE,
                reply_markup=user_interface.AGREEMENT)

    @router.callback_query(F.data == 'agree')
    async def cmd_agree(callback: CallbackQuery):
        user_id = callback.from_user.id
        if users_test.get(user_id) is None:
            await callback.answer('Вам отправлено окно...')
            await callback.message.edit_text(text="Теперь вы будете получать рассылку!",
                                             reply_markup=user_interface.NEGATION)
            users_test[user_id] = True
        else:
            await callback.message.edit_text(text="Вы уже подписались на рассылку")

    @router.callback_query(F.data == 'disagree')
    async def cmd_disagree(callback: CallbackQuery):
        if users_test.get(callback.from_user.id) is None:
            await callback.answer('что-ж.. до новой встречи!')
            await callback.message.edit_text(text="вы многое теряете, если захотите передумать, поменяйте ответ.",
                                             reply_markup=user_interface.AGREEMENT)
        else:
            await callback.message.edit_text(text="вы уже подписаны. Хотите отменить подписку?",
                                             reply_markup=user_interface.NEGATION)


@router.callback_query(F.data == 'unsubscribe')
async def unsubscribe_handle(callback: CallbackQuery):
    if users_test.get(callback.from_user.id) is not None:
        # todo: сделать удаление с проверкой
        users_test.pop(callback.from_user.id)
        await callback.answer('Жаль терять такого пользователя')
        await callback.message.edit_text(text="вы многое теряете, если захотите передумать, поменяйте ответ.",
                                         reply_markup=user_interface.AGREEMENT)
    else:
        await callback.message.edit_text(text="вы уже отписались от рассылки",
                                         reply_markup=user_interface.AGREEMENT)


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")
