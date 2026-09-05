from users.models import TelegramUser
from tasks.models import Task

from asgiref.sync import sync_to_async
import json

@sync_to_async
def create_user_or_update(id, username, first_name, chat_id):
    return TelegramUser.objects.update_or_create(
        id=id, 
        defaults={
            'username':username, 
            'first_name':first_name,
            'chat_id':chat_id
            }
        )

@sync_to_async
def get_or_update(id, language):
    user = TelegramUser.objects.get(id=id)
    user.language=language
    user.save()
    return user

@sync_to_async
def paste_tasks(tasks, user_id):
    try:
        tasks_to_create = []
        for task in tasks:
            for block in task['blocks']:
                new_task = Task(
                    user_id=user_id,
                    text = block.capitalize(),
                    date = task['date']
                    )
                tasks_to_create.append(new_task)
        Task.objects.bulk_create(tasks_to_create)
        return True
    except Exception:
        return False
    
@sync_to_async
def get_tasks_from_db(id):
    user = TelegramUser.objects.get(pk=id)
    tasks = list(user.tasks.all())
    return tasks

def parse_tasks(json_list):
    items = json.loads(json_list)
    try:
        array = items['items']
    except Exception:
        return None
    
    return array

@sync_to_async
def get_user_language(user_id, language='en'):
    
    try:
        user = TelegramUser.objects.get(id=user_id)
    except:
        return language
    
    if user and user.language:
        return user.language
    else:
        return language
    