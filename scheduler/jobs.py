import asyncio
from collections import defaultdict
from datetime import datetime, date
from zoneinfo import ZoneInfo

import os

from asgiref.sync import sync_to_async

from bot.middlewares.i18n import i18n_middleware
from bot.services import get_user_language


from scheduler.sender import send_task
from tasks.models import Task

async def proccess_tasks_morning():
    tasks, languages = await get_reminder_list()
    if not tasks:
        print('NO TASKS')
        return
    print("TASKS:", tasks)
    await send_reminder_task_morning(tasks, languages)

async def proccess_tasks_evening():
    tasks, languages = await get_reminder_list()
    if not tasks:
        print('NO TASKS')
        return
    print("TASKS:", tasks)
    await send_reminder_task_evening(tasks, languages)

async def get_reminder_list():
    today = datetime.now(ZoneInfo(os.getenv('TIMEZONE'))).date()
    tasks = await get_tasks(today)
    tasks_by_user = defaultdict(list)
    users_language = dict()
    for task in tasks:
        if not task.user.chat_id:
            continue
        tasks_by_user[task.user.chat_id].append(task)
        if task.user.chat_id not in users_language:
            users_language[task.user.chat_id] = await get_user_language(task.user.id)
    return tasks_by_user, users_language

@sync_to_async
def get_tasks(today):
    return list(Task.objects.filter(date=today, is_done=False).select_related('user'))

# Morning reminder for tasks

async def send_reminder_task_morning(tasks, languages):
    for chat_id, tasks in tasks.items():
        await send_task(chat_id, build_tasks_text_morning(tasks, languages[chat_id]))
        
def build_tasks_text_morning(tasks, lang):
    text = translate("🌤 Your tasks for today", lang)
    lines = [text+'\n\n']
    for i, task in enumerate(tasks, start=1):
        lines.append(f"{i}. {task.text}")
    return "\n".join(lines)

# Evening reminder for tasks

async def send_reminder_task_evening(tasks, languages):
    for chat_id, tasks in tasks.items():
        await send_task(chat_id, build_tasks_text_evening(tasks, languages[chat_id]))
        
def build_tasks_text_evening(tasks, lang):
    text = translate("😞 You didn't finish these tasks today", lang)
    lines = [text+'\n']
    for i, task in enumerate(tasks, start=1):
        lines.append(f"{i}. {task.text}")
    return "\n".join(lines)

# locales

def translate(text, locale):
    return i18n_middleware.i18n.gettext(text, locale=locale)