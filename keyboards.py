from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ADMIN_KB = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить нового админа',
                          callback_data='new_admin')],
    [InlineKeyboardButton(text='Добавить новый дедлайн',
                          callback_data='new_deadline', )],
]
)

ADMIN_CANCEL = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться в меню',
                          callback_data='back_to_menu')],
]
)

ADMIN_DEADLINE_DATE_BACK_CANCEL = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться в главное меню',
                          callback_data='back_to_menu')],
    [InlineKeyboardButton(text='Вернуться на шаг назад(к дате)',
                          callback_data='back_to_deadline_date_invitation')],
]
)

ADMIN_DEADLINE_NAME_BACK_CANCEL = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться в главное меню',
                          callback_data='back_to_menu')],
    [InlineKeyboardButton(text='Вернуться на шаг назад(к имени события дедлайна)',
                          callback_data='back_to_deadline_name_invitation')],
]
)

ADMIN_DEADLINE_COMMENT_BACK_CANCEL = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться в главное меню',
                          callback_data='back_to_menu')],
    [InlineKeyboardButton(text='Вернуться на шаг назад(к описанию дедлайна)',
                          callback_data='back_to_deadline_comment_invitation')],
]
)

ADMIN_DEADLINE_SAVE_CANCEL = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сохранить',
                          callback_data='save_deadline')],
    [InlineKeyboardButton(text='Вернуться в главное меню',
                          callback_data='back_to_menu')],
]
)

AGREEMENT = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Принимаю',
                          callback_data='agree')],
    [InlineKeyboardButton(text='❌ Отклоняю',
                          callback_data='disagree')],
])

NEGATION = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌ Отписаться',
                          callback_data='unsubscribe')],
])
