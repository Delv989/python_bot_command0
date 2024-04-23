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

#todo можно каждый раз выводить в тексте сообщения введенные данные

@router.callback_query(F.data == 'new_admin')
async def new_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите telegram id человека (он может узнать его написав нашему боту сообщение /id)",
        reply_markup=keyboards.ADMIN_CANCEL
    )
    await state.set_state(utils.Admin.enter_new_admin_id)


@router.callback_query(F.data == 'back_to_deadline_date_invitation')
@router.callback_query(F.data == 'new_deadline')
async def new_deadline(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите дату события в формате: ",  # todo
        reply_markup=keyboards.ADMIN_CANCEL
    )
    await state.set_state(utils.Admin.enter_deadline_date)


@router.callback_query(F.data == 'back_to_deadline_name_invitation')
@router.message(utils.Admin.enter_deadline_date)
async def enter_deadline_date(message: types.Message | CallbackQuery, state: FSMContext):
    if isinstance(message, types.Message):
        deadline_date = message.text
        if utils.valid_date(deadline_date):
            # todo temp save date
            await message.answer(text="Введите имя события дедлайна",
                                 reply_markup=keyboards.ADMIN_DEADLINE_DATE_BACK_CANCEL)
            await state.set_state(utils.Admin.enter_deadline_name)
        else:
            # todo ...
            await message.answer(text="Дата должна быть в формате...(к примеру ...) , попробуйте ввести еще раз",
                                 reply_markup=keyboards.ADMIN_CANCEL)
    elif isinstance(message, CallbackQuery):
        await message.message.answer(text="Введите имя события дедлайна",
                             reply_markup=keyboards.ADMIN_DEADLINE_DATE_BACK_CANCEL)
        await state.set_state(utils.Admin.enter_deadline_name)


@router.callback_query(F.data == 'back_to_deadline_name_invitation') #todo
@router.message(utils.Admin.enter_deadline_name)
async def enter_deadline_name(message: types.Message | CallbackQuery, state: FSMContext):
    if isinstance(message, types.Message):
        deadline_name = message.text
        if utils.valid_name(deadline_name):
            # todo temp save deadline_name
            await message.answer(text="Введите описание дедлайна",
                                 reply_markup=keyboards.ADMIN_DEADLINE_NAME_BACK_CANCEL)
            await state.set_state(utils.Admin.enter_deadline_comment)
        else:
            # todo ...
            await message.answer(text="Имя события дедлайна должно ...(к примеру ...) , попробуйте ввести еще раз",
                                 reply_markup=keyboards.ADMIN_DEADLINE_DATE_BACK_CANCEL)
    elif isinstance(message, CallbackQuery):
        await message.message.answer(text="Введите описание дедлайна", reply_markup=keyboards.ADMIN_DEADLINE_NAME_BACK_CANCEL)
        await state.set_state(utils.Admin.enter_deadline_comment)


@router.message(utils.Admin.enter_deadline_comment)
async def enter_deadline_comment(message: types.Message | CallbackQuery, state: FSMContext):
    if isinstance(message, types.Message):
        deadline_comment = message.text
        if utils.valid_comment(deadline_comment):
            # todo temp save deadline_comment + menu редактирования мб/ подтверждения сохранения + отмена сохранения
            await message.answer(text="Вы ввели: ....",
                                 # todo reply_markup=keyboards.
                                 )
            await state.set_state(utils.Admin.enter_deadline_name)
        else:
            # todo ...
            await message.answer(text="Описание события дедлайна должно ... , попробуйте ввести еще раз",
                                 reply_markup=keyboards.ADMIN_DEADLINE_NAME_BACK_CANCEL)
    elif isinstance(message, CallbackQuery):
        pass
        # todo что тут можно сделать с логикой редактирования / подтверждения
        # await message.message.answer(text="Введите имя события дедлайна",
        #                      reply_markup=keyboards.ADMIN_DEADLINE_DATE_BACK_CANCEL)
        # await state.set_state(utils.Admin.enter_deadline_name)


@router.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback: CallbackQuery):
    await callback.message.answer("Выберите действие:", reply_markup=keyboards.ADMIN_KB)


@router.message(utils.Admin.enter_new_admin_id)
async def enter_admin_id(message: types.Message, state: FSMContext):
    new_admin_id = message.text
    if utils.valid_id(new_admin_id):
        config.admin_id.append(new_admin_id)
        await message.answer(text="Успешно добавлен новый администратор", reply_markup=keyboards.ADMIN_CANCEL)
    else:
        await message.answer(text="Telegram id состоит только из цифр, попробуйте ввести еще раз",
                             reply_markup=keyboards.ADMIN_CANCEL)
    await state.set_state(None)


# @router.message(Command("subscribe"))
# async def subscribe_handler(msg: Message):
#     user_id = msg.from_user.id
#     # Подписываем пользователя
#     await msg.answer("Ты подписался на уведомления!")


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in config.admin_id:
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
