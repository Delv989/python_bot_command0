from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import config
import user_interface
import utils
import keyboards
import db_async
from deadline import Deadline

router = Router()


@router.callback_query(F.data == 'show_deadlines')
async def show_deadlines(callback: CallbackQuery, state: FSMContext):
    deadlines = await db_async.show_all_deadlines()
    await callback.message.answer(utils.convert_deadlines_to_output(deadlines),
                                  reply_markup=keyboards.ADMIN_KB_DEADLINE_LIST
                                  )
    await state.set_state(utils.Admin.enter_deadline_id)


@router.callback_query(F.data == 'delete_deadline_invitation')
async def delete_deadline_invitation(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(user_interface.DELETE_DEADLINE, reply_markup=keyboards.ADMIN_CANCEL)
    await state.set_state(utils.Admin.delete_deadline)


@router.message(utils.Admin.delete_deadline)
async def delete_deadline(message: Message, state: FSMContext):
    id_ = message.text
    if utils.valid_id(id_):
        await db_async.delete_deadline_id(int(id_))
        await message.answer(user_interface.DOUBTFUL_BUT_OK, reply_markup=keyboards.ADMIN_CANCEL)
        await state.clear()
    else:
        await message.answer(text=user_interface.VALIDATE_ID,
                             reply_markup=keyboards.ADMIN_CANCEL)


@router.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(user_interface.MAIN_MENU_ADMIN, reply_markup=keyboards.ADMIN_KB)


@router.callback_query(F.data == 'new_admin')
async def new_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=user_interface.INVITATION_INPUT_ID,
        reply_markup=keyboards.ADMIN_CANCEL
    )
    await state.set_state(utils.Admin.enter_new_admin_id)


@router.message(utils.Admin.enter_new_admin_id)
async def enter_admin_id(message: Message, state: FSMContext):
    new_admin_id = message.text
    if utils.valid_id(new_admin_id):
        config.admin_id.append(int(new_admin_id))
        await message.answer(text=user_interface.SUCCESS_ADD_NEW_ADMIN, reply_markup=keyboards.ADMIN_CANCEL)
        await state.clear()
    else:
        await message.answer(text=user_interface.VALIDATE_ID,
                             reply_markup=keyboards.ADMIN_CANCEL)


@router.callback_query(F.data == 'back_to_deadline_date_invitation')
@router.callback_query(F.data == 'new_deadline')
async def new_deadline(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=user_interface.INVITATION_INPUT_DATE,
        reply_markup=keyboards.ADMIN_CANCEL
    )
    await state.set_state(utils.Admin.enter_deadline_date)


@router.callback_query(F.data == 'back_to_deadline_name_invitation')
@router.message(utils.Admin.enter_deadline_date)
async def enter_deadline_date(message: Message | CallbackQuery, state: FSMContext):
    if isinstance(message, Message):
        deadline_date = message.text
        deadline_date_converted = utils.convert_to_datetime(deadline_date)
        if deadline_date_converted is not None:
            if utils.valid_date(deadline_date_converted):
                await state.update_data(date=deadline_date_converted)
                await message.answer(text=user_interface.INVITATION_INPUT_NAME,
                                     reply_markup=keyboards.ADMIN_DEADLINE_DATE_BACK_CANCEL)
                await state.set_state(utils.Admin.enter_deadline_name)
            else:
                await message.answer(text=user_interface.VALIDATE_DATE_TOO_LATE,
                                     reply_markup=keyboards.ADMIN_CANCEL)
        else:
            await message.answer(text=user_interface.VALIDATE_DATE,
                                 reply_markup=keyboards.ADMIN_CANCEL)
    elif isinstance(message, CallbackQuery):
        await message.message.answer(text=user_interface.INVITATION_INPUT_NAME,
                                     reply_markup=keyboards.ADMIN_DEADLINE_DATE_BACK_CANCEL)
        await state.set_state(utils.Admin.enter_deadline_name)


@router.callback_query(F.data == 'back_to_deadline_comment_invitation')
@router.message(utils.Admin.enter_deadline_name)
async def enter_deadline_name(message: Message | CallbackQuery, state: FSMContext):
    if isinstance(message, Message):
        deadline_name = message.text
        if utils.valid_name(deadline_name):
            await state.update_data(name=deadline_name)
            await message.answer(text=user_interface.INVITATION_INPUT_COMMENT,
                                 reply_markup=keyboards.ADMIN_DEADLINE_NAME_BACK_CANCEL)
            await state.set_state(utils.Admin.enter_deadline_comment)
        else:
            await message.answer(text=user_interface.VALIDATE_NAME,
                                 reply_markup=keyboards.ADMIN_DEADLINE_DATE_BACK_CANCEL)
    elif isinstance(message, CallbackQuery):
        await message.message.answer(text=user_interface.INVITATION_INPUT_COMMENT,
                                     reply_markup=keyboards.ADMIN_DEADLINE_NAME_BACK_CANCEL)
        await state.set_state(utils.Admin.enter_deadline_comment)


@router.message(utils.Admin.enter_deadline_comment)
async def enter_deadline_comment(message: Message, state: FSMContext):
    deadline_comment = message.text
    if utils.valid_comment(deadline_comment):
        await state.update_data(comment=deadline_comment)
        data = await state.get_data()
        await message.answer(text=f"Вы ввели дедлайн: \n"
                                  f"Имя {data['name']}\n"
                                  f"Дата {data['date']}\n"
                                  f"Описание {data['comment']}\n"
                             ,
                             reply_markup=keyboards.ADMIN_DEADLINE_SAVE_CANCEL
                             )
        await state.set_state(utils.Admin.save_or_cancel)
    else:
        await message.answer(text=user_interface.VALIDATE_COMMENT,
                             reply_markup=keyboards.ADMIN_DEADLINE_NAME_BACK_CANCEL)


@router.callback_query(F.data == 'save_deadline')
async def save_deadline(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=user_interface.SUCCESS_ADD_NEW_DEADLINE,
        reply_markup=keyboards.ADMIN_CANCEL
    )
    data = await state.get_data()
    await state.clear()
    await db_async.insert_deadline(Deadline.from_dict(data))
