from aiogram import F, Router
from aiogram.types import CallbackQuery

import db

import keyboards

router = Router()


@router.callback_query(F.data == 'agree')
async def cmd_agree(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not db.is_user_id_in_db(user_id):
        await callback.answer('Вам отправлено окно...')
        await callback.message.edit_text(text="Теперь вы будете получать рассылку!",
                                         reply_markup=keyboards.NEGATION)
        db.insert_user_id_db(user_id)
    else:
        await callback.message.edit_text(text="Вы уже подписались на рассылку")


@router.callback_query(F.data == 'disagree')
async def cmd_disagree(callback: CallbackQuery):
    if not db.is_user_id_in_db(callback.from_user.id):
        await callback.answer('что-ж.. до новой встречи!')
        await callback.message.edit_text(text="вы многое теряете, если захотите передумать, поменяйте ответ.",
                                         reply_markup=keyboards.AGREEMENT)
    else:
        await callback.message.edit_text(text="вы уже подписаны. Хотите отменить подписку?",
                                         reply_markup=keyboards.NEGATION)


@router.callback_query(F.data == 'unsubscribe')
async def unsubscribe_handle(callback: CallbackQuery):
    if db.is_user_id_in_db(callback.from_user.id):
        # todo: сделать удаление с проверкой
        db.delete_user_id_db(callback.from_user.id)
        await callback.answer('Жаль терять такого пользователя')
        await callback.message.edit_text(text="вы многое теряете, если захотите передумать, поменяйте ответ.",
                                         reply_markup=keyboards.AGREEMENT)
    else:
        await callback.message.edit_text(text="вы уже отписались от рассылки",
                                         reply_markup=keyboards.AGREEMENT)
