import sqlite3

def create_db():
    # create + connect to db
    connection = sqlite3.connect("task.db")
    cursor = connection.cursor()

    # create table to store tasks if not existent

    # table has ID, task name, completion, and priority_level
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_text TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            priority_level INTEGER DEFAULT 0
        )
    ''')

    # commit changes
    connection.commit()
    connection.close()

#insert task into database
def insert(task_text, priority_level=1):
    connection = sqlite3.connect("task.db")
    # inserting new row into table, providing insert as tuple task_text, (tuple improves security and maintainability)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO task (task_text, priority_level) VALUES (?, ?)", (task_text, int(priority_level)))

    #get the ID of the newly inserted task
    task_id = cursor.lastrowid   

    connection.commit()
    connection.close()

    return task_id

#getting task from db
def get_task():
    connection = sqlite3.connect("task.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, task_text, completed FROM task")
    # retrieve all rows, specific method to access libraries in python
    tasks = cursor.fetchall()
    connection.close()

    #dictionary to store task text as keys
    task_dict = {}
    for task in tasks:
        # _ means we are not interested in third
        task_id, task_text, _ = task
        task_dict[task_text] = task_id

    return task_dict

# updating tasks
def update(task_text, completion):
    connection = sqlite3.connect("task.db")
    cursor = connection.cursor()
    #update an existing row
    cursor.execute("UPDATE task SET completed=? WHERE task_text=?", (completion, task_text))
    connection.commit()
    connection.close()

#delete tasks
def delete(task_text):
    connection = sqlite3.connect("task.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM task WHERE task_text=?", (task_text,))
    connection.commit()
    connection.close()

# Get completion status of a task based on its ID
def get_completion(task_id):
    connection = sqlite3.connect("task.db")
    cursor = connection.cursor()
    cursor.execute("SELECT completed FROM task WHERE id=?", (task_id,))
    result = cursor.fetchone()
    connection.close()

    if result is not None:
        return result[0]
    else:
        return None
    
# get priority level
def get_priority_level(task_id):
    connection = sqlite3.connect("task.db")
    cursor = connection.cursor()
    cursor.execute("SELECT priority_level FROM task WHERE id=?", (task_id,))
    result = cursor.fetchone()
    connection.close()

    if result is not None:
        return result[0]
    else:
        return None