from peewee import Model, IntegerField, CharField, SqliteDatabase


db = SqliteDatabase("UserDatabase.db")

class User(Model):
    """
    Описание класса:
    Описывает таблицу в базе данных.
    Дочерний класс, класса Model

    Атрибуты:
    user_id (int): id пользователя
    name (str): имя пользователя

    Возвращаемое значение:
    None
    """
    user_id = IntegerField(primary_key=True)
    name = CharField()

    class Meta:
        database = db

User.create_table()