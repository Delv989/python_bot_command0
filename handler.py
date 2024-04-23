from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from aiogram import types
import config
import user_interface
import utils
import keyboards

router = Router()
users_test = {}

@router.callback_query(utils.Admin.choose_option)
async def answer(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'new_admin':
        await callback.message.answer(
            text="Введите telegram id человека (он может узнать его написав нашему боту сообщение /id)"
        )
        await state.set_state(utils.Admin.enter_new_admin_id)
    elif callback.data == 'new_deadline':
        await callback.message.answer("Добавляем дедлайн")


@router.message(utils.Admin.enter_new_admin_id)
async def new_admin(message: types.Message, state: FSMContext):
    new_admin_id = message.text
    if utils.valid_id(new_admin_id):
        config.admin_id.append(new_admin_id)
        await message.answer(text="Успешно добавлен новый администратор", reply_markup=keyboards.ADMIN_KB)
        await state.set_state(None)
        print("Валидный id")  # todo del
    else:
        await message.answer(text="Telegram id состоит только из цифр, попробуйте ввести еще раз", reply_markup=keyboards.ADMIN_KB)
        # todo добавить кнопку отмены
        print("Ошибочный id")  # todo del


# @router.message(Command("subscribe"))
# async def subscribe_handler(msg: Message):
#     user_id = msg.from_user.id
#     # Подписываем пользователя
#     await msg.answer("Ты подписался на уведомления!")





@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in config.admin_id:
        await state.set_state(utils.Admin.choose_option)
        await message.answer("Выберите действие:", reply_markup=keyboards.ADMIN_KB)
    else:
        if users_test.get(user_id) is not None:
            await message.answer(
                user_interface.TEXT_UNSUBSCRIBE,
                reply_markup=keyboards.NEGATION)
        else:
            await message.answer(
                user_interface.TEXT_AGREE,
                reply_markup=keyboards.AGREEMENT)


@router.callback_query(F.data == 'agree')
async def cmd_agree(callback: CallbackQuery):
    user_id = callback.from_user.id
    if users_test.get(user_id) is None:
        await callback.answer('Вам отправлено окно...')
        await callback.message.edit_text(text="Теперь вы будете получать рассылку!",
                                         reply_markup=keyboards.NEGATION)
        users_test[user_id] = True
    else:
        await callback.message.edit_text(text="Вы уже подписались на рассылку")


@router.callback_query(F.data == 'disagree')
async def cmd_disagree(callback: CallbackQuery):
    if users_test.get(callback.from_user.id) is None:
        await callback.answer('что-ж.. до новой встречи!')
        await callback.message.edit_text(text="вы многое теряете, если захотите передумать, поменяйте ответ.",
                                         reply_markup=keyboards.AGREEMENT)
    else:
        await callback.message.edit_text(text="вы уже подписаны. Хотите отменить подписку?",
                                         reply_markup=keyboards.NEGATION)


@router.callback_query(F.data == 'unsubscribe')
async def unsubscribe_handle(callback: CallbackQuery):
    if users_test.get(callback.from_user.id) is not None:
        # todo: сделать удаление с проверкой
        users_test.pop(callback.from_user.id)
        await callback.answer('Жаль терять такого пользователя')
        await callback.message.edit_text(text="вы многое теряете, если захотите передумать, поменяйте ответ.",
                                         reply_markup=keyboards.AGREEMENT)
    else:
        await callback.message.edit_text(text="вы уже отписались от рассылки",
                                         reply_markup=keyboards.AGREEMENT)


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")
