"""
Модуль работы database
"""

from peewee import SqliteDatabase, Model, IntegerField, CharField, DateField, ForeignKeyField, TextField

from config_data import VariablesConstantsBot

db = SqliteDatabase(VariablesConstantsBot.DB_PATH)


class User(Model):
    """
    Описывает таблицу пользователей в базе данных.
    Дочерний класс, класса Model

    Attributes:
    id (int): ...
    user_id (int): id пользователя
    name (str): имя пользователя
    """
    id = IntegerField(primary_key=True)
    User = IntegerField(unique=True)
    Name = CharField()

    class Meta:
        """
        Определяет имя базы данных

        Attributes:
        database (str): имя базы данных
        """
        database = db


class Request(Model):
    """
    Описывает таблицу запросов в базе данных.
    Дочерний класс, класса Model

    Attributes:
    id (int): ...
    user (...): ...
    country (...): ...
    city (...): ...
    arrival_date (...): ...
    departure_month (...): ...
    adults (...): ...
    children (...): ...
    """
    id = IntegerField(primary_key=True)
    User_id = ForeignKeyField(User)
    Type = CharField()
    Param_sort = CharField()
    Range = CharField(null=True)
    Country = CharField()
    City = CharField()
    Arrival_date = DateField()
    Departure_month = DateField()
    Count_rooms = IntegerField()
    Count_adults = IntegerField()
    Count_children = IntegerField()

    class Meta:
        """
        Определяет имя базы данных

        Attributes:
        database (str): имя базы данных
        """
        database = db


class Response(Model):
    """
    Описывает таблицу ответов в базе данных.
    Дочерний класс, класса Model

    Attributes:
    id (int): ...
    url_site (...): ...
    foto (...): ...
    short_info (...): ...
    """
    id = IntegerField(primary_key=True)
    Request_id = ForeignKeyField(Request)
    Name_hotels = CharField()
    Short_info = CharField()
    Url_site = CharField()
    Photo = TextField()

    class Meta:
        """
        Определяет имя базы данных

        Attributes:
        database (str): имя базы данных
        """
        database = db


User.create_table()
Request.create_table()
Response.create_table()
