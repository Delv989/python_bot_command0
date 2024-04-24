from aiogram import F, Router
from aiogram.types import CallbackQuery
from utils import users_test

import keyboards

router = Router()


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
