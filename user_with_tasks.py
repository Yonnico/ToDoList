from database import db

sql_insert_query = "INSERT INTO tasks (user_id, task_index, title, description) VALUES (?, ?, ?, ?)"
sql_update_query = "UPDATE tasks SET done = True WHERE user_id = ? AND task_index = ?"
sql_delete_query = "DELETE FROM tasks WHERE user_id = ? AND task_index = ?"
sql_select_tasks_query = "SELECT * FROM tasks WHERE user_id = ?"
sql_select_task_query = "SELECT * FROM tasks WHERE user_id = ? AND task_index = ?"
sql_max_index_query = "SELECT MAX(task_index) FROM tasks WHERE user_id = ?"
    

class User:

    def __init__(self, user_id):
        self.user_id = user_id


    def task_exists(self, task_index):
        task = self.find_task(task_index)
        if task:
            return True
        else:
            return False
        

    def find_last_index(self):
        db.r_query(sql_max_index_query, (self.user_id,))
        result = db.cur.fetchone()
        index = result[0]
        return index


    def make_index(self):
        index = self.find_last_index()
        if index == None:
            index = 1
            return index
        else:
            index += 1
            return index
        

    def find_task(self, task_index):
        db.r_query(sql_select_task_query, (self.user_id, task_index))
        task = db.cur.fetchone()
        return task


    def create_task(self, title, description):
        status = "Задача успешно создана!"
        task_index = self.make_index()
        db.r_query(sql_insert_query, (self.user_id, task_index, title, description))
        if self.task_exists(task_index):
            return status
        else:
            status = "Упс что-то пошло не так..."
            return status


    def complete_task(self, task_index):
        if self.task_exists(task_index):
            db.r_query(sql_update_query, (self.user_id, task_index))
        else:
            status = "Задачи не существует или введён неправильный номер задачи!"
            return status


    def delete_task(self, task_index):
        status = "Задача успешно удалена"
        if self.task_exists(task_index):
            db.r_query(sql_delete_query, (self.user_id, task_index))
            return status
        else:
            status = "Задачи не существует или введён неправильный номер задачи!"
            return status


    def get_tasks(self):
        db.r_query(sql_select_tasks_query, (self.user_id,))
        tasks = db.cur.fetchall()
        return tasks
