import sqlite3
from config import path


class Database:

    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.cur = self.db.cursor()


    def r_query(self, q, values):
        self.cur.execute(q, values)
        self.db.commit()


    def close(self):
        self.db.close()


db = Database(path)
