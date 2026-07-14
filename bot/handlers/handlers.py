import asyncio

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import MenuButtonWebApp, WebAppInfo
from aiogram import Bot
import os
from aiogram.utils.i18n import gettext as _

import keyboards as kb
import states as st
from middlewares.i18n import i18n_middleware

# Gemini

from gemini import get_tasks

# Django

from asgiref.sync import sync_to_async
from services import create_user_or_update, get_or_update, paste_tasks, get_tasks_from_db, parse_tasks

user = Router()

@user.message(CommandStart())
async def command_start(message: Message, bot: Bot):
    
    obj, created = await create_user_or_update(
        message.from_user.id, 
        message.from_user.username, 
        message.from_user.first_name,
        message.chat.id     
        )
    
    pinned_message = await message.answer(
           _(
            "👋 <b>Hello! I am DailyDO</b>\n"
            "\n"
            "DailyDO is your handy daily assistant 📅\n"
            "I will remind you of your tasks at any convenient time so you never forget anything.\n"
            "\n"
            "<b>What I can do:</b>\n"
            "• create tasks\n"
            "• remind you about them\n"
            "• populate tasks using AI\n"
            "\n"
            "<b>Why it's convenient:</b>\n"
            "• everything is in Telegram\n"
            "• simple interaction\n"
            "• graphical user interface\n"
            "\n"
            "✨ Created by me and <b>@Innocento00</b>\n"
            "For any questions or suggestions, feel free to contact me."
        ),
        parse_mode="HTML"
    ) 
    
    await message.answer(_('Hello, {first_name} @{username}!').format(
        first_name = obj.first_name, username = obj.username), 
                         reply_markup=kb.get_menu())
    
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=kb.get_webapp()
        )

@user.message(F.text, F.func(lambda msg: msg.text == _('Language')))
async def change_language(message: Message, state: FSMContext):
    
    await state.set_state(st.LanguageState.language)
    await message.answer(
        _("Choose the language you prefer:"),
        reply_markup=kb.choose_language 
        )
    
@user.callback_query(st.LanguageState.language)
async def change_language_for_user(callback: CallbackQuery, state: FSMContext):
    try:
        user = await get_or_update(callback.from_user.id, callback.data)
    except Exception as e:
        return await callback.message.edit_text(
            _("Something went wrong. Try again later.")
            )
    
    i18n_middleware.set_locale(callback.data) 
    
    await callback.message.edit_text(
        _("Your language is now {language}").format(
            language = user.get_language_display()
        )
        )
    await callback.message.answer(
        _("What would you like to do next?"),
        reply_markup=kb.get_menu()
    )
    await state.clear()
    await callback.answer()
    

@user.message(F.text, F.func(lambda msg: msg.text == _("My tasks")))
async def command_show_tasks(message: Message):
    await message.answer(_("📋 Collecting your tasks... Please wait..."))
    tasks = await get_tasks_from_db(message.from_user.id)
    if tasks:
        grouped_tasks = {}
        for task in tasks:
            if task.date not in grouped_tasks:
                grouped_tasks[task.date] = []
            grouped_tasks[task.date].append(task)
        text_to_send=[_("<b>📅 Your tasks</b>\n")]
        for date, tasks in grouped_tasks.items():
            text_to_send.append(f"🗓 <b>{date}</b>")
            text_to_send.append("────────────────")
            for task in tasks:
                text_to_send.append(f'{task.text} {'✅' if task.is_done else '⬜'}')
            text_to_send.append('')
        final_text = "\n".join(text_to_send)
        await message.answer(final_text, parse_mode='HTML')
        return
    else:
        await message.answer(_("📭 You don't have any tasks yet."))
        return
        
@user.message(F.text, F.func(lambda msg: msg.text == _("Create tasks")))
async def command_create_tasks(message: Message, state: FSMContext):
    await state.set_state(st.FormTasks.tasks)
    help_message = await message.answer(
       _(
            "✨ <b>How to Create Tasks</b>\n"
            "\n"
            "To help the AI understand your request correctly, please follow these guidelines:\n"
            "\n"
            "📅 <b>Dates</b>\n"
            "• You can include up to <b>5 different dates</b> in a single message.\n"
            "• If a task has <b>no date</b>, it will automatically be assigned to <b>today</b>.\n"
            "\n"
            "📝 <b>Best Practice</b>\n"
            "For the most accurate results, group tasks by date.\n"
            "\n"
            "<b>Example:</b>\n"
            "\n"
            "<b>Tomorrow:</b>\n"
            "• Buy groceries\n"
            "• Go to the gym\n"
            "\n"
            "<b>Friday:</b>\n"
            "• Finish the report\n"
            "• Call John\n"
            "\n"
            "This format helps the AI assign each task to the correct date.\n"
            "\n"
            "⚠️ <b>Current Limitations</b>\n"
            "• Don't ask the bot to <b>delete</b>, <b>move</b>, <b>edit</b>, or <b>complete</b> existing tasks.\n"
            "• The bot currently <b>only creates new tasks</b>.\n"
            "• If your message contains more than <b>5 different dates</b>, it may not be processed correctly.\n"
            "\n"
            "💡 <b>Tip</b>\n"
            "You can write naturally, just make sure each task has a clear date (or no date if it should be scheduled for today)."
        ),
        parse_mode="HTML"
    )
    start_message = await message.answer(
        _("Awaiting your tasks:"),
        reply_markup=kb.get_cancel_button()
        )
    await state.update_data(
        help_message_id=help_message.message_id,
        start_message_id=start_message.message_id
    )

@user.callback_query(st.FormTasks.tasks, F.data == "cancel_command")
async def cancel_tasks(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    help_message_id = data.get("help_message_id")
    await callback.message.edit_text(_('Command was cancelled.'), reply_markup=None)
    await callback.message.answer(_('What would you like to do next?'))
    if help_message_id:
        try:
            await callback.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=help_message_id
            )
        except Exception:
            pass
    await state.clear()
    await callback.answer()

@user.message(st.FormTasks.tasks)
async def confirmation_tasks(message: Message, state: FSMContext):
    data = await state.get_data()
    start_message_id = data.get("start_message_id")
    if start_message_id:
        try:
            await message.bot.edit_message_reply_markup(
                chat_id=message.chat.id,
                message_id=start_message_id,
                reply_markup=None
            )
        except Exception:
            pass
    current_tasks = message.text.strip()
    await state.update_data(raw_tasks=current_tasks)
    await state.set_state(st.FormTasks.confirm_tasks)
    
    await message.answer(
        _("Are these tasks correct?\n\n{current_tasks}").format(
            current_tasks = current_tasks
            ),
        reply_markup=kb.get_confirm_button()
    )

@user.callback_query(st.FormTasks.confirm_tasks, F.data == "cancel_tasks")
async def cancel_writed_tasks(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(_("Command was cancelled."))
    await callback.message.answer(_('What would you like to do next?'))
    data = await state.get_data()
    help_message_id = data.get("help_message_id")
    if help_message_id:
        try:
            await callback.message.bot.edit_message_reply_markup(
                chat_id=callback.message.chat.id,
                message_id=help_message_id,
                reply_markup=None
            )
        except Exception:
            pass
    await state.clear()
    await callback.answer()

@user.callback_query(st.FormTasks.confirm_tasks, F.data == "rewrite_tasks")
async def rewrite_tasks(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.FormTasks.tasks)
    await callback.message.edit_text(_("Okay, send the tasks again:"))
    await callback.answer()

@user.callback_query(st.FormTasks.confirm_tasks, F.data == "confirm_tasks")
async def process_tasks(callback: CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    help_message_id = data.get("help_message_id")
    await callback.message.edit_text(_("Please wait... Your tasks are being processed..."))
    
    if help_message_id:
        try:
            await callback.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=help_message_id
            )
        except Exception:
            pass
    
    data = await state.get_data()
    current_tasks = data.get('raw_tasks')
    await state.clear()
    await callback.answer()
    
    try:
        json_tasks = await get_tasks(current_tasks)
    except Exception as e:
        await callback.message.answer(_("Something went wrong. Try again later."))
        return
        
    validated_tasks = parse_tasks(json_tasks)
    if not validated_tasks:
        await callback.message.answer(_("Something went wrong. Try again later."))
        return
    
    success = await paste_tasks(validated_tasks, callback.from_user.id)
    if success:
        await callback.message.answer(_("Your tasks successfully saved!"))
    else:
        await callback.message.answer(_('Something went wrong. Try again later.'))
    

@user.message(F.text)
async def message_text(message: Message):
    await message.answer(_("Sorry, I don't understand this command."),
                         reply_markup=kb.webapp)

@user.message()
async def message_types(message: Message):
    await message.answer(_("Bot does not support this type of file.")+"\n"+
                         _("In the future, we will add support for processing voice recordings, text files, and photos."))