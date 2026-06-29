from aiogram.fsm.state import State, StatesGroup


class FormTasks(StatesGroup): 
    tasks = State()