import { useState, useEffect, useRef, useLayoutEffect } from 'react'
import './App.css'
import { GripVertical, Pencil, Trash2, ChevronDown, ArrowLeft } from 'lucide-react'
import { Plus } from 'lucide-react'
import { useTranslation } from 'react-i18next'

function App() {

  const API = import.meta.env.VITE_API_URL

  const { t, i18n } = useTranslation()

  const [tasks, setTasks] = useState([])
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0])
  const [isLoading, setIsLoading] = useState(false)
  const dateInputRef = useRef(null)
  const refreshPromiseRef = useRef(null)

  const [showAddForm, setShowAddForm] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [newTask, setNewTask] = useState({
    text: '',
    date: selectedDate,
  })
  const [editingTaskId, setEditingTaskId] = useState(null)
  const [taskErrors, setTaskErrors] = useState({})

  const [deleteTarget, setDeleteTarget] = useState(null)
  const [isDeleting, setIsDeleting] = useState(false)
  const [me, setMe] = useState(null)

  const [showAllTasksModal, setShowAllTasksModal] = useState(false)
  const [allTasks, setAllTasks] = useState([])
  const [isAllTasksLoading, setIsAllTasksLoading] = useState(false)

  const initStartedRef = useRef(false)

  const [detailsTask, setDetailsTask] = useState(null)

  const [hasOverflowMap, setHasOverflowMap] = useState({})
  const taskTextRefs = useRef({})

  useEffect(() => {
    if (initStartedRef.current) return
    initStartedRef.current = true
    initializeApp()
  }, [])

  useEffect(() => {
    if (isAuthenticated) {
      fetchTasks()
    }
  }, [selectedDate, isAuthenticated])

  useLayoutEffect(() => {
    checkTaskOverflow()
  }, [tasks])

  useEffect(() => {
    const handleResize = () => checkTaskOverflow()
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])
  
  useEffect(() => {
    const isAnyOverlayOpen =
      showAllTasksModal || showAddForm || !!deleteTarget || !!detailsTask

    if (isAnyOverlayOpen) {
      const scrollY = window.scrollY
      document.body.style.position = 'fixed'
      document.body.style.top = `-${scrollY}px`
      document.body.style.left = '0'
      document.body.style.right = '0'
      document.body.style.overflow = 'hidden'
      document.body.dataset.scrollY = scrollY
    } else {
      const scrollY = document.body.dataset.scrollY || '0'
      document.body.style.position = ''
      document.body.style.top = ''
      document.body.style.left = ''
      document.body.style.right = ''
      document.body.style.overflow = ''
      window.scrollTo(0, parseInt(scrollY, 10))
    }
  }, [showAllTasksModal, showAddForm, deleteTarget, detailsTask])

  const getAccessToken = () => localStorage.getItem('access_token')
  const getRefreshToken = () => localStorage.getItem('refresh_token')

  const saveTokens = ({ access, refresh }) => {
    if (access) localStorage.setItem('access_token', access)
    if (refresh) localStorage.setItem('refresh_token', refresh)
  }

  const clearTokens = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  const fetchAllTasks = async () => {
    try {
      setIsAllTasksLoading(true)

      const response = await authFetch(`${API}/api/task/tasks/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`)
      }

      const data = await response.json()
      setAllTasks(data)
    } catch (error) {
      console.error('Error fetching all tasks:', error)
    } finally {
      setIsAllTasksLoading(false)
    }
  }

  const fetchMe = async () => {
    try {
      const response = await authFetch(`${API}/api/user/me/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`)
      }

      const data = await response.json()
      setMe(data)
    } catch (error) {
      console.error('Error fetching user profile:', error)
    }
  }
  const refreshAccessToken = async () => {
    if (refreshPromiseRef.current) {
      return refreshPromiseRef.current
    }

    refreshPromiseRef.current = (async () => {
      const refresh = getRefreshToken()

      if (!refresh) {
        throw new Error('No refresh token')
      }

      const response = await fetch(`${API}/api/user/token/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh }),
      })

      if (!response.ok) {
        clearTokens()
        throw new Error(`Refresh failed: ${response.status}`)
      }

      const data = await response.json()
      saveTokens(data)
      return data.access
    })()

    try {
      return await refreshPromiseRef.current
    } finally {
      refreshPromiseRef.current = null
    }
  }

  const authFetch = async (url, options = {}, retry = true) => {
    const makeRequest = (token) =>
      fetch(url, {
        ...options,
        headers: {
          ...(options.headers || {}),
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
      })

    let response = await makeRequest(getAccessToken())

    if (response.status !== 401 || !retry) {
      return response
    }

    try {
      const newAccess = await refreshAccessToken()
      response = await makeRequest(newAccess)
      return response
    } catch (error) {
      clearTokens()
      setIsAuthenticated(false)
      setMe(null)
      throw error
    }
  }

  const setTaskTextRef = (taskId, el) => {
  if (el) {
    taskTextRefs.current[taskId] = el
  } else {
    delete taskTextRefs.current[taskId]
  }
}

  const checkTaskOverflow = () => {
    const next = {}

    Object.entries(taskTextRefs.current).forEach(([taskId, el]) => {
      if (!el) return

      const hasVerticalOverflow = el.scrollHeight > el.clientHeight + 1
      const hasHorizontalOverflow = el.scrollWidth > el.clientWidth + 1

      next[taskId] = hasVerticalOverflow || hasHorizontalOverflow
    })

    setHasOverflowMap(next)
  }

  const initializeApp = async () => {
    try {
      const tg = window.Telegram?.WebApp
      tg?.ready()

      const initData = tg?.initData

      if (!initData) {
        console.log('Error! No initData')
        return
      }

      const authResponse = await fetch(`${API}/api/user/auth/telegram/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ initData: initData }),
      })

      if (!authResponse.ok) {
        throw new Error(`Auth failed: ${authResponse.status}`)
      }

      const tokens = await authResponse.json()
      saveTokens(tokens)

      const meResponse = await fetch(`${API}/api/user/me/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${tokens.access}`,
        },
      })

      if (!meResponse.ok) {
        throw new Error(`Fetch me failed: ${meResponse.status}`)
      }

      const meData = await meResponse.json()
      setMe(meData)
      if (['en', 'ru', 'uk'].includes(meData.language)) {
        await i18n.changeLanguage(meData.language)
      } else {
        await i18n.changeLanguage('en')
      }
      setIsAuthenticated(true)
    } catch (error) {
      clearTokens()
      setIsAuthenticated(false)
      setMe(null)
      console.error('Auth error:', error)
    }
  }
  const openTaskDetails = (task) => {
    setDetailsTask(task)
  }

  const closeTaskDetails = () => {
    setDetailsTask(null)
  }


  const fetchTasks = async () => {
    setIsLoading(true)

    try {
      const response = await authFetch(`${API}/api/task/tasks/?date=${selectedDate}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`)
      }

      const data = await response.json()
      setTasks(data)
    } catch (error) {
      console.error('Error of getting tasks', error)
    } finally {
      setIsLoading(false)
    }
  }

    const changeDate = (offset) => {
      const dateObj = new Date(selectedDate)
      dateObj.setDate(dateObj.getDate() + offset)
      const year = dateObj.getFullYear()
      const month = String(dateObj.getMonth() + 1).padStart(2, '0')
      const day = String(dateObj.getDate()).padStart(2, '0')
      setSelectedDate(`${year}-${month}-${day}`)
    }

    const openDatePicker = () => {
      if (dateInputRef.current?.showPicker) {
        dateInputRef.current.showPicker()
      } else {
        dateInputRef.current?.focus()
      }
    }

    const formattedDate = new Date(selectedDate).toLocaleDateString('en-GB', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    })
    const avatarUrl = me?.username
    ? `https://cute-cat-avatars.laosing-cors.workers.dev/api/v1/${encodeURIComponent(me.username)}`
    : 'https://cute-cat-avatars.laosing-cors.workers.dev/api/v1/guest'

  const openEditForm = (task) => {
    setEditingTaskId(task.id)
    setNewTask({
      text: task.text,
      date: task.date,
    })
    setShowAddForm(true)
  }
  const openAddForm = () => {
    setEditingTaskId(null)
    setNewTask({
      text: '',
      date: selectedDate,
    })
    setShowAddForm(true)
  }

  const closeTaskForm = () => {
    setShowAddForm(false)
    setEditingTaskId(null)
    setNewTask({
      text: '',
      date: selectedDate,
    })
  }
  const goHome = () => {
    setShowAllTasksModal(false)
  }

  const handleTaskSubmit = async (e) => {
      e.preventDefault()

      const text = newTask.text.trim()
      if (!text) return

      const isEditing = editingTaskId !== null

      const payload = {
        text,
        date: newTask.date,
      }

      const url = isEditing
        ? `${API}/api/task/tasks/${editingTaskId}/`
        : `${API}/api/task/tasks/`

      const method = isEditing ? 'PATCH' : 'POST'

      try {
        setIsSubmitting(true)

        const response = await authFetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload),
        })

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`)
          }

          const savedTask = await response.json()

          if (isEditing) {
            if (savedTask.date === selectedDate) {
              setTasks((prev) => {
                const exists = prev.some((item) => item.id === savedTask.id)

                if (exists) {
                  return prev.map((item) =>
                    item.id === savedTask.id ? savedTask : item
                  )
                }

                return [...prev, savedTask]
              })
            } else {
              setTasks((prev) =>
                prev.filter((item) => item.id !== savedTask.id)
              )
            }

            setAllTasks((prev) =>
              prev.map((item) =>
                item.id === savedTask.id ? savedTask : item
              )
            )
          } else {
            await fetchTasks()
            await fetchAllTasks()
          }

          closeTaskForm()
      } catch (error) {
        console.error('Task save error:', error)
      } finally {
        setIsSubmitting(false)
      }
    }
  const handleToggleDone = async (task) => {
    const nextIsDone = !task.is_done

    setTaskErrors((prev) => {
      const updated = { ...prev }
      delete updated[task.id]
      return updated
    })
    setAllTasks((prev) =>
      prev.map((item) =>
        item.id === task.id
          ? { ...item, is_done: nextIsDone }
          : item
      )
    )
    setTasks((prev) =>
      prev.map((item) =>
        item.id === task.id
          ? { ...item, is_done: nextIsDone }
          : item
      )
    )

    try {
      const response = await authFetch(`${API}/api/task/tasks/${task.id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          is_done: nextIsDone,
        }),
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`)
      }
    } catch (error) {
      setTasks((prev) =>
        prev.map((item) =>
          item.id === task.id
            ? { ...item, is_done: task.is_done }
            : item
        )
      )
      setAllTasks((prev) =>
        prev.map((item) =>
          item.id === task.id
            ? { ...item, is_done: task.is_done }
            : item
        )
      )

      setTaskErrors((prev) => ({
        ...prev,
        [task.id]: t('couldNotUpdateStatus'),
      }))

      setTimeout(() => {
        setTaskErrors((prev) => {
          const updated = { ...prev }
          delete updated[task.id]
          return updated
        })
      }, 2500)

      console.error('Toggle done error:', error)
    }
  }
  const handleDeleteTask = async () => {
    if (!deleteTarget) return

    const task = deleteTarget

    setTaskErrors((prev) => {
      const updated = { ...prev }
      delete updated[task.id]
      return updated
    })

    setTasks((prev) => prev.filter((item) => item.id !== task.id))
    setAllTasks((prev) => prev.filter((item) => item.id !== task.id))
    closeDeleteConfirm()

    try {
      setIsDeleting(true)

      const response = await authFetch(`${API}/api/task/tasks/${task.id}/`, {
        method: 'DELETE',
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`)
      }
    } catch (error) {
      setTasks((prev) => {
        const alreadyExists = prev.some((item) => item.id === task.id)
        if (alreadyExists) return prev
        return [...prev, task]
      })
      setAllTasks((prev) => {
        const alreadyExists = prev.some((item) => item.id === task.id)
        if (alreadyExists) return prev
        return [...prev, task]
      })

      setTaskErrors((prev) => ({
        ...prev,
        [task.id]: t('couldNotDeleteTask'),
      }))

      setTimeout(() => {
        setTaskErrors((prev) => {
          const updated = { ...prev }
          delete updated[task.id]
          return updated
        })
      }, 2500)

      console.error('Delete task error:', error)
    } finally {
      setIsDeleting(false)
    }
  }
  const openDeleteConfirm = (task) => {
    setDeleteTarget(task)
  }

  const closeDeleteConfirm = () => {
    setDeleteTarget(null)
  }
  const openAllTasksModal = async () => {
    setShowAllTasksModal(true)
    await fetchAllTasks()
  }

  const closeAllTasksModal = () => {
    setShowAllTasksModal(false)
  }
  const groupedTasks = allTasks.reduce((acc, task) => {
    const dateKey = task.date

    if (!acc[dateKey]) {
      acc[dateKey] = []
    }

    acc[dateKey].push(task)
    return acc
  }, {})

  const sortedDates = Object.keys(groupedTasks).sort(
    (a, b) => new Date(b) - new Date(a)
  )
          
  return (
    <div className="app-container">

      <section className="title-block">
        <h1
          className="title-clickable"
          onClick={goHome}
        >
          {t('myTasks')}
        </h1>
        <div className="user-chip" onClick={openAllTasksModal} role="button" tabIndex={0}>
          <img
            className="user-avatar"
            src={avatarUrl}
            alt={me?.username ? `${me.username} avatar` : 'User avatar'}
          />
          <span className="user-name">
            {me?.username || t('guest')}
          </span>
        </div>
      </section>

      <section className="calendar-block">
        <div className="date-navigation">
          <button className="nav-arrow" onClick={() => changeDate(-1)}>
            &#10094;
          </button>

          <div className="date-picker-wrapper" onClick={openDatePicker}>
            <span className="date-display">{formattedDate}</span>
            <input
              ref={dateInputRef}
              type="date"
              className="apple-date-picker"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
            />
          </div>

          <button className="nav-arrow" onClick={() => changeDate(1)}>
            &#10095;
          </button>
        </div>
      </section>

      <section className="tasks-block">
        {!isAuthenticated ? (
          <p className="loading-text">{t('checkingTelegramAuth')}</p>
        ) : isLoading ? (
          <div className="spinner-container">
            <div className="spinner"></div>
          </div>
        ) : (
          <>
            <div className="tasks-head">
              <span className="tasks-head-label tasks-head-left">{t('tasks')}</span>
              <span className="tasks-head-label tasks-head-right">{t('status')}</span>
            </div>
            <ul className="task-list">
              {tasks.length === 0 ? (
                <li className="task-item empty">{t('noTasksForDay')}</li>
              ) : (
                tasks.map((task) => (
                  <li key={task.id} className="task-item">
                    <div className="task-content">
                      <div className={`task-text-block ${hasOverflowMap[task.id] ? 'has-expand' : ''}`}>
                        <span
                          ref={(el) => setTaskTextRef(task.id, el)}
                          className="task-text"
                        >
                          {task.text}
                        </span>

                        {hasOverflowMap[task.id] ? (
                          <button
                            type="button"
                            className="task-overlay-toggle"
                            aria-label={t('openTaskDetails')}
                            onClick={() => openTaskDetails(task)}
                          >
                            <ChevronDown size={20} strokeWidth={3} />
                          </button>
                        ) : null}

                        {taskErrors[task.id] && (
                          <span className="task-error-text">{taskErrors[task.id]}</span>
                        )}
                      </div>

                        <button
                          className="icon-btn edit-btn"
                          type="button"
                          aria-label={t('editTaskAria')}
                          onClick={() => openEditForm(task)}
                        >
                          <Pencil size={18} strokeWidth={2.2} />
                        </button>
                      </div>

                    <button
                      className={`done-btn ${task.is_done ? 'is-done' : ''}`}
                      type="button"
                      aria-label={task.is_done ? t('taskCompleted') : t('markAsDone')}
                      onClick={() => handleToggleDone(task)}
                    >
                      {task.is_done && <span>✓</span>}
                    </button>

                    <button
                      className="icon-btn delete-btn"
                      type="button"
                      aria-label={t('deleteTask')}
                      onClick={() => openDeleteConfirm(task)}
                    >
                      <Trash2 size={20} strokeWidth={2.3} />
                    </button>
                  </li>
                ))
              )}
            </ul>
            </>
          )}
        </section>
        {detailsTask && (
          <div className="modal-overlay" onClick={closeTaskDetails}>
            <div className="task-modal task-details-modal" onClick={(e) => e.stopPropagation()}>
              <div className="task-modal-header">
                <span className="task-modal-header-side" aria-hidden="true" />
                <div className="task-modal-header single">
                  <h2 className="task-modal-title">{t('taskDetails')}</h2>
                </div>
              </div>
              <div className="task-details-content-wrap">
                <div className="task-details-content">
                  <p className="task-details-text">{detailsTask.text}</p>
                </div>
              </div>
              <div className="task-details-footer">
                <button
                  type="button"
                  className="task-form-cancel task-details-close-btn"
                  onClick={closeTaskDetails}
                >
                  {t('close')}
                </button>
              </div>
            </div>
          </div>
        )}
        {showAllTasksModal && (
          <div className="all-tasks-page" onClick={closeAllTasksModal}>
            <div className="all-tasks-page-content" onClick={(e) => e.stopPropagation()}>
              <div className="all-tasks-header">
                <button
                  type="button"
                  className="all-tasks-back-btn"
                  aria-label={t('close')}
                  onClick={closeAllTasksModal}
                >
                  <ArrowLeft size={22} strokeWidth={2.3} />
                </button>

                <h2 className='alltasks-text-arrow'>{t('allTasks')}</h2>
                <span aria-hidden="true"></span>
              </div>
              {isAllTasksLoading ? (
                <div className="spinner-container">
                  <div className="spinner"></div>
                </div>
              ) : allTasks.length === 0 ? (
                <p className="loading-text">{t('noTasksYet')}</p>
              ) : (
                <div className="all-tasks-groups">
                  {sortedDates.map((dateKey) => (
                    <div key={dateKey} className="all-tasks-group">
                      <h3 className="all-tasks-date">
                        {new Date(dateKey).toLocaleDateString('en-GB', {
                          day: '2-digit',
                          month: 'short',
                          year: 'numeric',
                        })}
                      </h3>

                      <ul className="task-list">
                        {groupedTasks[dateKey].map((task) => (
                          <li key={task.id} className="task-item">
                            <div className="task-content">
                              <div className={`task-text-block ${hasOverflowMap[task.id] ? 'has-expand' : ''}`}>
                                <span
                                  ref={(el) => setTaskTextRef(task.id, el)}
                                  className="task-text"
                                >
                                  {task.text}
                                </span>

                                {hasOverflowMap[task.id] ? (
                                  <button
                                    type="button"
                                    className="task-overlay-toggle"
                                    aria-label={t('openTaskDetails')}
                                    onClick={() => openTaskDetails(task)}
                                  >
                                    <ChevronDown size={20} strokeWidth={3} />
                                  </button>
                                ) : null}

                                {taskErrors[task.id] && (
                                  <span className="task-error-text">{taskErrors[task.id]}</span>
                                )}
                              </div>

                                <button
                                  className="icon-btn edit-btn"
                                  type="button"
                                  aria-label={t('editTaskAria')}
                                  onClick={() => openEditForm(task)}
                                >
                                  <Pencil size={18} strokeWidth={2.2} />
                                </button>
                              </div>

                            <button
                              className={`done-btn ${task.is_done ? 'is-done' : ''}`}
                              type="button"
                              aria-label={task.is_done ? t('taskCompleted') : t('markAsDone')}
                              onClick={() => handleToggleDone(task)}
                            >
                              {task.is_done && <span>✓</span>}
                            </button>

                            <button
                              className="icon-btn delete-btn"
                              type="button"
                              aria-label={t('deleteTask')}
                              onClick={() => openDeleteConfirm(task)}
                            >
                              <Trash2 size={20} strokeWidth={2.3} />
                            </button>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
        {showAddForm && (
          <div className="modal-overlay" onClick={() => closeTaskForm()}>
            <div className="task-modal" onClick={(e) => e.stopPropagation()}>
              <h2>{editingTaskId ? t('editTask') : t('addTask')}</h2>

              <form onSubmit={handleTaskSubmit} className="task-form">
              <input
                type="text"
                placeholder={t('taskText')}
                value={newTask.text}
                maxLength={300}
                onChange={(e) =>
                  setNewTask((prev) => ({ ...prev, text: e.target.value }))
                }
                required
              />

              <div className={`task-char-counter ${newTask.text.length >= 270 ? 'is-near-limit' : ''}`}>
                {300 - newTask.text.length} {t('symbolsleft')}
              </div>

                <input
                  type="date"
                  value={newTask.date}
                  onChange={(e) =>
                    setNewTask((prev) => ({ ...prev, date: e.target.value }))
                  }
                  required
                />

                <div className="task-form-actions">
                  <button
                    type="button"
                    className="task-form-cancel"
                    onClick={() => closeTaskForm()}
                  >
                    {t('cancel')}
                  </button>

                  <button
                    type="submit"
                    className="task-form-submit"
                    disabled={isSubmitting}
                  >
                    {isSubmitting
                      ? editingTaskId
                        ? t('saving')
                        : t('creating')
                      : editingTaskId
                        ? t('saveChanges')
                        : t('save')}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
        {deleteTarget && (
          <div className="modal-overlay" onClick={closeDeleteConfirm}>
            <div className="task-modal delete-modal" onClick={(e) => e.stopPropagation()}>
              <h2>{t('deleteTaskTitle')}</h2>

              <div className="delete-modal-content">
                <p className="delete-modal-text">{deleteTarget.text}</p>
              </div>

              <div className="task-form-actions">
                <button
                  type="button"
                  className="task-form-cancel"
                  onClick={closeDeleteConfirm}
                  disabled={isDeleting}
                >
                  {t('cancel')}
                </button>

                <button
                  type="button"
                  className="task-form-submit delete-confirm-btn"
                  onClick={handleDeleteTask}
                  disabled={isDeleting}
                >
                  {isDeleting ? t('deleting') : t('delete')}
                </button>
              </div>
            </div>
          </div>
        )}
          <div className="add-task-wrap">
              <button
                className="floating-add-btn"
                type="button"
                aria-label="Add task"
                onClick={openAddForm}
              >
                <Plus size={18} strokeWidth={2.2} />
              <span className="floating-add-text">{t('addTaskButton')}</span>
            </button>
          </div>
    </div>
  )
}

export default App