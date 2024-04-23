from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TEXT_AGREE = "Это сервис для напоминаниях о дедлайнах официальных мероприятиях. Хотите получать уведомления?"
TEXT_UNSUBSCRIBE = "Хотите отписаться?"
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
