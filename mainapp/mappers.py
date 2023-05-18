from mainapp.models import User
from config.middlware import BaseRegisteredClass
from database.exception import IntegrityError


class UserMapper(BaseRegisteredClass):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.tablename = "users"

    def all(self):
        sql = f"SELECT * FROM {self.tablename};"
        self.cursor.execute(sql)
        result = []
        for row in self.connection.fetchall():
            id, username, email, phone = row
            user = User(username, email, phone, id)
            result.append(user)
        return result

    def find_by_id(self, id):
        sql = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(sql, (id,))
        result = self.cursor.fetchone()
        if result:
            id, username, email, phone = result
            return User(username, email, phone, id)
        else:
            raise IntegrityError(f"record with id={id} not found")

    def insert(self, user):
        sql = f"INSERT INTO {self.tablename} (id, username, email, phone) VALUES (?, ?, ?, ?)"
        self.cursor.execute(sql, (user.id, user.username, user.email, user.phone))
        try:
            self.connection.commit()
        except Exception as e:
            raise IntegrityError(e.args)

    def update(self, user):
        sql = f"UPDATE {self.tablename} SET username=? WHERE id=?"

        self.cursor.execute(sql, (user.username, user.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise IntegrityError(e.args)

    def delete(self, user):
        sql = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(sql, (user.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise IntegrityError(e.args)
