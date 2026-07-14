import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

const resources = {
  en: {
    translation: {
      myTasks: 'My tasks',
      tasks: 'Tasks',
      status: 'Status',
      checkingTelegramAuth: 'Checking telegram auth...',
      noTasksForDay: 'You do not have tasks on this day',
      allTasks: 'All tasks',
      noTasksYet: 'No tasks yet',
      close: 'Close',
      editTask: 'Edit task',
      addTask: 'Add task',
      taskText: 'Task text',
      cancel: 'Cancel',
      save: 'Save',
      saveChanges: 'Save changes',
      saving: 'Saving...',
      creating: 'Creating...',
      deleteTaskTitle: 'Delete task?',
      delete: 'Delete',
      deleting: 'Deleting...',
      addTaskButton: 'Add',
      taskCompleted: 'Task completed',
      markAsDone: 'Mark as done',
      deleteTask: 'Delete task',
      editTaskAria: 'Edit task',
      couldNotUpdateStatus: 'Could not update status',
      couldNotDeleteTask: 'Could not delete task',
      guest: 'guest',
      openTaskDetails: 'Open task details',
      taskDetails: 'Task details',
      symbolsleft: 'symbols left'
    }
  },
  ru: {
    translation: {
      myTasks: 'Мои задачи',
      tasks: 'Задачи',
      status: 'Статус',
      checkingTelegramAuth: 'Проверяем авторизацию Telegram...',
      noTasksForDay: 'На этот день у вас нет задач',
      allTasks: 'Все задачи',
      noTasksYet: 'Пока задач нет',
      close: 'Закрыть',
      editTask: 'Редактировать задачу',
      addTask: 'Добавить задачу',
      taskText: 'Текст задачи',
      cancel: 'Отмена',
      save: 'Сохранить',
      saveChanges: 'Сохранить изменения',
      saving: 'Сохраняем...',
      creating: 'Создаём...',
      deleteTaskTitle: 'Удалить задачу?',
      delete: 'Удалить',
      deleting: 'Удаляем...',
      addTaskButton: 'Добавить',
      taskCompleted: 'Задача выполнена',
      markAsDone: 'Отметить выполненной',
      deleteTask: 'Удалить задачу',
      editTaskAria: 'Редактировать задачу',
      couldNotUpdateStatus: 'Не удалось обновить статус',
      couldNotDeleteTask: 'Не удалось удалить задачу',
      guest: 'гость',
      openTaskDetails: 'Открыть полное описание задачи',
      taskDetails: 'Задача',
      symbolsleft: 'символов осталось'
    }
  },
  uk: {
    translation: {
      myTasks: 'Мої завдання',
      tasks: 'Завдання',
      status: 'Статус',
      checkingTelegramAuth: 'Перевіряємо авторизацію Telegram...',
      noTasksForDay: 'На цей день у вас немає завдань',
      allTasks: 'Усі завдання',
      noTasksYet: 'Поки що завдань немає',
      close: 'Закрити',
      editTask: 'Редагувати завдання',
      addTask: 'Додати завдання',
      taskText: 'Текст завдання',
      cancel: 'Скасувати',
      save: 'Зберегти',
      saveChanges: 'Зберегти зміни',
      saving: 'Зберігаємо...',
      creating: 'Створюємо...',
      deleteTaskTitle: 'Видалити завдання?',
      delete: 'Видалити',
      deleting: 'Видаляємо...',
      addTaskButton: 'Додати',
      taskCompleted: 'Завдання виконано',
      markAsDone: 'Позначити виконаним',
      deleteTask: 'Видалити завдання',
      editTaskAria: 'Редагувати завдання',
      couldNotUpdateStatus: 'Не вдалося оновити статус',
      couldNotDeleteTask: 'Не вдалося видалити завдання',
      guest: 'гість',
      openTaskDetails: 'Відкрити повний опис завдання',
      taskDetails: 'Завдання',
      symbolsleft: 'символів залишилось'
    }
  }
}

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  })

export default i18n