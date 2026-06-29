from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='My tasks')],
        [KeyboardButton(text='Create tasks')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Select the option'
)

webapp = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='DailyDoApp', url='google.com')]
    ]
)