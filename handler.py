# from aiogram import F, Router
# from aiogram.types import Message, CallbackQuery
# from aiogram.filters import Command, StateFilter
# from aiogram.fsm.context import FSMContext
#
# from aiogram import types
#
# from utils import tz
# import config
# import user_interface
# import utils
# import keyboards
#
# users_test = {}
#
# buffer_deadline = {
#     'date': None,
#     'name': None,
#     'comment': None
# }
#
# router = Router()
#
#
#
# # todo не работает по разным файлам хз
#
#
#
#
# @router.callback_query(F.data == 'back_to_menu')
# async def back_to_menu(callback: CallbackQuery, state: FSMContext):
#     await state.clear()
#     await callback.message.answer("Выберите действие:", reply_markup=keyboards.ADMIN_KB)
#
#
# @router.callback_query(F.data == 'new_admin')
# async def new_admin(callback: CallbackQuery, state: FSMContext):
#     await callback.message.answer(
#         text="Введите telegram id человека (он может узнать его, написав нашему боту любое сообщение)",
#         reply_markup=keyboards.ADMIN_CANCEL
#     )
#     await state.set_state(utils.Admin.enter_new_admin_id)
#
#
# @router.message(utils.Admin.enter_new_admin_id)
# async def enter_admin_id(message: types.Message, state: FSMContext):
#     new_admin_id = message.text
#     if utils.valid_id(new_admin_id):
#         config.admin_id.append(new_admin_id)
#         await message.answer(text="Успешно добавлен новый администратор", reply_markup=keyboards.ADMIN_CANCEL)
#     else:
#         await message.answer(text="Telegram id состоит только из цифр, попробуйте ввести еще раз",
#                              reply_markup=keyboards.ADMIN_CANCEL)
#     await state.set_state(None)
#
#
# @router.callback_query(F.data == 'back_to_deadline_date_invitation')
# @router.callback_query(F.data == 'new_deadline')
# async def new_deadline(callback: CallbackQuery, state: FSMContext):
#     await callback.message.answer(
#         text=f"Введите дату и время события({tz}) в формате: дд.мм.ггггг чч.мм\n"
#              "К примеру 01.01.2025 15.30",
#         reply_markup=keyboards.ADMIN_CANCEL
#     )
#     await state.set_state(utils.Admin.enter_deadline_date)
#
#
# @router.callback_query(F.data == 'back_to_deadline_name_invitation')
# @router.message(utils.Admin.enter_deadline_date)
# async def enter_deadline_date(message: types.Message | CallbackQuery, state: FSMContext):
#     if isinstance(message, types.Message):
#         deadline_date = message.text
#         if utils.valid_date(deadline_date):
#             await state.update_data(date=deadline_date)
#             await message.answer(text="Введите имя события дедлайна",
#                                  reply_markup=keyboards.ADMIN_DEADLINE_DATE_BACK_CANCEL)
#             await state.set_state(utils.Admin.enter_deadline_name)
#         else:
#             # todo ...
#             await message.answer(text="Дата должна быть в формате...(к примеру ...) , попробуйте ввести еще раз",
#                                  reply_markup=keyboards.ADMIN_CANCEL)
#     elif isinstance(message, CallbackQuery):
#         await message.message.answer(text="Введите имя события дедлайна",
#                                      reply_markup=keyboards.ADMIN_DEADLINE_DATE_BACK_CANCEL)
#         await state.set_state(utils.Admin.enter_deadline_name)
#
#
# @router.callback_query(F.data == 'back_to_deadline_comment_invitation')  # todo
# @router.message(utils.Admin.enter_deadline_name)
# async def enter_deadline_name(message: types.Message | CallbackQuery, state: FSMContext):
#     if isinstance(message, types.Message):
#         deadline_name = message.text
#         if utils.valid_name(deadline_name):
#             await state.update_data(name=deadline_name)
#             await message.answer(text="Введите описание дедлайна",
#                                  reply_markup=keyboards.ADMIN_DEADLINE_NAME_BACK_CANCEL)
#             await state.set_state(utils.Admin.enter_deadline_comment)
#         else:
#             # todo ...
#             await message.answer(text="Имя события дедлайна должно ...(к примеру ...) , попробуйте ввести еще раз",
#                                  reply_markup=keyboards.ADMIN_DEADLINE_DATE_BACK_CANCEL)
#     elif isinstance(message, CallbackQuery):
#         await message.message.answer(text="Введите описание дедлайна",
#                                      reply_markup=keyboards.ADMIN_DEADLINE_NAME_BACK_CANCEL)
#         await state.set_state(utils.Admin.enter_deadline_comment)
#
#
# @router.message(utils.Admin.enter_deadline_comment)
# async def enter_deadline_comment(message: types.Message | CallbackQuery, state: FSMContext):
#     if isinstance(message, types.Message):
#         deadline_comment = message.text
#         if utils.valid_comment(deadline_comment):
#             await state.update_data(comment=deadline_comment)
#             data = await state.get_data()
#             # todo menu редактирования мб/ подтверждения сохранения + отмена сохранения
#             await message.answer(text=f"Вы ввели дедлайн: \n"
#                                       f"Имя {data['name']}\n"
#                                       f"Дата {data['date']}\n"
#                                       f"Описание {data['comment']}\n"
#                                  ,
#                                  # todo reply_markup=keyboards.
#                                  )
#             await state.set_state(utils.Admin.enter_deadline_name)
#         else:
#             # todo ...
#             await message.answer(text="Описание события дедлайна должно ... , попробуйте ввести еще раз",
#                                  reply_markup=keyboards.ADMIN_DEADLINE_NAME_BACK_CANCEL)
#     elif isinstance(message, CallbackQuery):
#         pass
#         # todo что тут можно сделать с логикой редактирования / подтверждения
#         # await message.message.answer(text="Введите имя события дедлайна",
#         #                      reply_markup=keyboards.ADMIN_DEADLINE_DATE_BACK_CANCEL)
#         # await state.set_state(utils.Admin.enter_deadline_name)
#
#
#
#
#
#
#
#
# @router.callback_query(F.data == 'agree')
# async def cmd_agree(callback: CallbackQuery):
#     user_id = callback.from_user.id
#     if users_test.get(user_id) is None:
#         await callback.answer('Вам отправлено окно...')
#         await callback.message.edit_text(text="Теперь вы будете получать рассылку!",
#                                          reply_markup=keyboards.NEGATION)
#         users_test[user_id] = True
#     else:
#         await callback.message.edit_text(text="Вы уже подписались на рассылку")
#
#
# @router.callback_query(F.data == 'disagree')
# async def cmd_disagree(callback: CallbackQuery):
#     if users_test.get(callback.from_user.id) is None:
#         await callback.answer('что-ж.. до новой встречи!')
#         await callback.message.edit_text(text="вы многое теряете, если захотите передумать, поменяйте ответ.",
#                                          reply_markup=keyboards.AGREEMENT)
#     else:
#         await callback.message.edit_text(text="вы уже подписаны. Хотите отменить подписку?",
#                                          reply_markup=keyboards.NEGATION)
#
#
# @router.callback_query(F.data == 'unsubscribe')
# async def unsubscribe_handle(callback: CallbackQuery):
#     if users_test.get(callback.from_user.id) is not None:
#         # todo: сделать удаление с проверкой
#         users_test.pop(callback.from_user.id)
#         await callback.answer('Жаль терять такого пользователя')
#         await callback.message.edit_text(text="вы многое теряете, если захотите передумать, поменяйте ответ.",
#                                          reply_markup=keyboards.AGREEMENT)
#     else:
#         await callback.message.edit_text(text="вы уже отписались от рассылки",
#                                          reply_markup=keyboards.AGREEMENT)
#
# @router.message(Command("start"))
# async def start(message: types.Message):
#     user_id = message.from_user.id
#     if user_id in config.admin_id:
#         await message.answer("Выберите действие:", reply_markup=keyboards.ADMIN_KB)
#     else:
#         if users_test.get(user_id) is not None:
#             await message.answer(
#                 user_interface.TEXT_UNSUBSCRIBE,
#                 reply_markup=keyboards.NEGATION)
#         else:
#             await message.answer(
#                 user_interface.TEXT_AGREE,
#                 reply_markup=keyboards.AGREEMENT)
#
# @router.message()
# async def message_handler(msg: Message):
#     await msg.answer(f"Твой ID: {msg.from_user.id}")
#
#
