import asyncio

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import keyboards as kb
import states as st

# Gemini

from gemini import get_tasks

# Django

from asgiref.sync import sync_to_async
from services import create_user_or_update, paste_tasks, get_tasks_from_db, parse_tasks

user = Router()

@user.message(CommandStart())
async def command_start(message: Message):
    
    obj, created = await create_user_or_update(
        message.from_user.id, 
        message.from_user.username, 
        message.from_user.first_name     
        )
    
    await message.answer(f'Hello, {obj.first_name} @{obj.username}', 
                         reply_markup=kb.menu)

@user.message(F.text=="My tasks")
async def command_show_tasks(message: Message):
    await message.answer("Collecting your tasks... Please wait.")
    tasks = await get_tasks_from_db(message.from_user.id)
    if tasks:
        grouped_tasks = {}
        for task in tasks:
            if task.date not in grouped_tasks:
                grouped_tasks[task.date] = []
            grouped_tasks[task.date].append(task)
        text_to_send=["Your tasks:\n"]
        for date, tasks in grouped_tasks.items():
            text_to_send.append(f'{date}/status:')
            for task in tasks:
                text_to_send.append(f'{task.text} {'yes' if task.is_done else 'no'}')
            text_to_send.append('')
        final_text = "\n".join(text_to_send)
        await message.answer(final_text)
        return
    else:
        await message.answer('You don`t have any task.')
        return
        
@user.message(F.text=="Create tasks")
async def command_create_tasks(message: Message, state: FSMContext):
    await state.set_state(st.FormTasks.tasks)
    await message.answer("Awaiting text:")
    
@user.message(st.FormTasks.tasks)
async def process_tasks(message: Message, state: FSMContext):
    current_tasks = message.text
    await state.clear()
    await message.answer('Please wait. Your tasks are being processed...')
    
    try:
        json_tasks = await get_tasks(current_tasks)
    except Exception as e:
        await message.answer(f'Something went wrong. Try again later.')
        return
        
    validated_tasks = parse_tasks(json_tasks)
    if not validated_tasks:
        await message.answer('Something went wrong. Try again later.')
        return
    
    success = await paste_tasks(validated_tasks, message.from_user.id)
    if success:
        await message.answer("Your tasks succesfully saved!")
    else:
        await message.answer('Something went wrong. Try again later.')
    

@user.message(F.text)
async def message_text(message: Message):
    await message.answer("Sorry. Bot do not understand this command.",
                         reply_markup=kb.webapp)

@user.message()
async def message_types(message: Message):
    await message.answer("Bot does not support this type of file.\n"
                         "In the future, we will add support for processing voice recordings, text files, and photos.")