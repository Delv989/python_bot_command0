from aiogram import F, Router
from aiogram.types import CallbackQuery

import bot_tools
import db_async

import keyboards
import utils

router = Router()


@router.callback_query(F.data == 'agree')
async def cmd_agree(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not await db_async.is_user_id_in_db(user_id):
        await db_async.insert_user_id_db(user_id)
        await bot_tools.send_deadline_to_users(user_id)
        await callback.answer('Вам отправлено окно...')
        await callback.message.edit_text(text="Теперь вы будете получать рассылку!",
                                         reply_markup=keyboards.NEGATION)
    else:
        await callback.message.edit_text(text="Вы уже подписались на рассылку")


@router.callback_query(F.data == 'disagree')
async def cmd_disagree(callback: CallbackQuery):
    if not await db_async.is_user_id_in_db(callback.from_user.id):
        await callback.answer('что-ж.. до новой встречи!')
        await callback.message.edit_text(text="Вы много теряете. Если передумаете, поменяйте ответ.",
                                         reply_markup=keyboards.AGREEMENT)
    else:
        await callback.message.edit_text(text="вы уже подписаны. Хотите отменить подписку?",
                                         reply_markup=keyboards.NEGATION)


@router.callback_query(F.data == 'unsubscribe')
async def unsubscribe_handle(callback: CallbackQuery):
    if await db_async.is_user_id_in_db(callback.from_user.id):
        await db_async.delete_user_id_db(callback.from_user.id)
        await callback.answer('Жаль терять такого пользователя')
        await callback.message.edit_text(text="Вы много теряете. Если передумаете, поменяйте ответ.s",
                                         reply_markup=keyboards.AGREEMENT)
    else:
        await callback.message.edit_text(text="вы уже отписались от рассылки",
                                         reply_markup=keyboards.AGREEMENT)


@router.callback_query(F.data == "all_deadlines")
async def show_all_deadlines(callback: CallbackQuery):
    deadlines = await db_async.show_all_deadlines()
    if await db_async.is_user_id_in_db(callback.from_user.id):
        await callback.message.answer(utils.convert_deadlines_to_output_2_users(deadlines))
    else:
        await callback.message.answer(text="Вы не подписаны на получения рассылки",
                                      reply_markup=keyboards.AGREEMENT)
