import os

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.types import MenuButtonWebApp
from aiogram.utils.i18n import gettext as _

def get_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("My tasks"))],
            [KeyboardButton(text=_("Create tasks"))],
            [KeyboardButton(text=_("Language"))]
        ],
        resize_keyboard=True,
        input_field_placeholder=_('Select the option'),
    )

choose_language = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇬🇧En", callback_data="en"),
                InlineKeyboardButton(text="🇺🇦Ukr", callback_data="uk"),
                InlineKeyboardButton(text="🏳️Rus", callback_data="ru"),
            ]
        ]
    )

webapp = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='DailyDoApp', web_app=WebAppInfo(url=os.getenv('WEBAPP_URL')))]
    ]
)

def get_webapp():
    return MenuButtonWebApp(
                    text="DailyDoApp",
                    web_app=WebAppInfo(
                        url=os.getenv('WEBAPP_URL')
                    )
                )

def get_confirm_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Save"), callback_data="confirm_tasks"),
                InlineKeyboardButton(text=_("Edit"), callback_data="rewrite_tasks"),
            ],
            [
                InlineKeyboardButton(text=_("Cancel"), callback_data="cancel_tasks"),
            ]
        ]
    )

def get_cancel_button():
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=_("Cancel"), callback_data="cancel_command"),
                ]
            ]
        )