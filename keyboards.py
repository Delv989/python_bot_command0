from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ADMIN_KB = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить нового админа',
                          callback_data='new_admin')],
    [InlineKeyboardButton(text='Добавить новый дедлайн',
                          callback_data='new_deadline')],
]
)