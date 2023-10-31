from peewee import SqliteDatabase, Model, IntegerField, CharField

from config_data import VariablesConstants


db = SqliteDatabase(VariablesConstants.DB_PATH)

class User(Model):
    """
    Class description:
    Описывает таблицу в базе данных.
    Дочерний класс, класса Model

    Attributes:
    user_id (int): id пользователя
    name (str): имя пользователя
    """
    user_id = IntegerField(primary_key=True)
    name = CharField()

    class Meta:
        """
        Class description:
        Определяет имя базы данных

        Attributes:
        database (str): имя базы данных
        """
        database = db

User.create_table()
