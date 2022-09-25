import sqlite3
from dotenv import dotenv_values

from student import Student

class SqliteDB:
    def __init__(self, table, db_path = ":memory:", **kwargs):
        self.conn = sqlite3.connect(db_path)
        self.__keys = kwargs
        self.table = table

    def create(self, primary_key=None):
        if primary_key not in self.__keys:
            primary_key = list(self.__keys.keys())[0]
        
        cursor = self.conn.cursor()
        cursor.execute(f"""
            CREATE TABLE {self.table} (
                {', '.join([f"{k} {i}" for k, i in self.__keys.items()])},
                CONSTRAINT pk_{self.table} PRIMARY KEY ({primary_key})
            )
        """)
        self.conn.commit()
        cursor.close()

    def insert(self, **kwargs):
        cursor = self.conn.cursor()

        ks = []
        vs = []

        for k, v in kwargs.items():
            ks.append(k)
            vs.append(v)

        cursor.execute(f"""
            INSERT INTO {self.table} ({','.join(ks)}) VALUES ({','.join([f'"{v}"' for v in vs])})
        """)

        self.conn.commit()
        cursor.close()

    def get_all(self):
        cursor = self.conn.cursor()

        cursor.execute(f"""
            SELECT * FROM {self.table}
        """)

        data = cursor.fetchall()
        cursor.close()

        return data

    def get_equality(self, **kwargs):
        cursor = self.conn.cursor()

        cursor.execute(f"""
            SELECT * FROM {self.table} WHERE {' AND '.join(f"{k}={v}" for k, v in kwargs.items())}
        """)

        data = cursor.fetchall()
        cursor.close()

        return data

    def close(self):
        self.conn.close()

class StudentDB(SqliteDB):
    def __init__(self):
        super(StudentDB, self).__init__("students", id="int", first_name="text", last_name="text", maths="int", science="int", eng="int", sst="int", it="int", email="text", db_path="students.db")

    def create(self):
        try:
            super().create(primary_key="id")
        except sqlite3.OperationalError:
            pass
        
    def insert(self, id, first_name, last_name, maths, science, eng, sst, it, email):
        try:
            super().insert(id=id, first_name=first_name, last_name=last_name, maths=maths, eng=eng, science=science, sst=sst, it=it, email=email)
        except sqlite3.IntegrityError:
            return False
        return True

    def get(self, id):
        data = super().get_equality(id=id)
        if data:
            return Student.from_list(data[0])
        return None

if __name__ == "__main__":
    # config = dotenv_values(".env")
    db = StudentDB()
    db.create()
    db.insert('2106306', "yash", "pawar", '100', '100', '123', '22', '23', "yp@contact.com")
    print(db.get(2106306))
    print(db.get(2106307))
    db.close()
