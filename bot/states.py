from aiogram.fsm.state import State, StatesGroup


class FormTasks(StatesGroup): 
    tasks = State()
    confirm_tasks = State()
    
class LanguageState(StatesGroup):
    language = State()