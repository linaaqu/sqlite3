import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('tasks.db')
cursor = connection.cursor()

# Создаем таблицу Tasks
cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'Not Started',
    priority INTEGER DEFAULT 2 CHECK(priority BETWEEN 0 AND 3)
)''')

# Функция добавления новой задачи
def add_task(title, priority=2):
    cursor.execute('INSERT INTO Tasks (title, priority) VALUES (?, ?)', (title, priority))
    connection.commit()

# Функция обновления статуса задачи
def update_task_status(task_id, status):
    cursor.execute('UPDATE Tasks SET status = ? WHERE id = ?', (status, task_id))
    connection.commit()

# Функция вывода списка задач
def list_tasks():
    cursor.execute('SELECT * FROM Tasks ORDER BY priority DESC')
    tasks = cursor.fetchall()
    for task in tasks:
        print(task)

# Добавляем задачи с приоритетами
add_task('Подготовить презентацию', 1)
add_task('Закончить отчет', 3)
add_task('Подготовить ужин')

update_task_status(2, 'In Progress')
list_tasks()
connection.close()