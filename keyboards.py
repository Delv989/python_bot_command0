from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ADMIN_KB = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить нового админа',
                          callback_data='new_admin')],
    [InlineKeyboardButton(text='Добавить новый дедлайн',
                          callback_data='new_deadline')],
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