"""
Модуль описания таблиц для телеграм бота
"""

from peewee import SqliteDatabase, Model, IntegerField, CharField, DateField, ForeignKeyField, TextField

from config_data import VariablesConstantsBot

db = SqliteDatabase(VariablesConstantsBot.DB_PATH)


class User(Model):
    """
    Описывает таблицу пользователей в базе данных.
    Дочерний класс, класса Model

    Attributes:
    id (int): идентификатор записи
    User (int): id пользователя
    Name (str): имя пользователя
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
    id (int): идентификатор записи
    User_id (int): связующая запись с таблицей User
    Type (str): тип запроса
    Param_sort (str): тип сортировки
    Range (str): данные диапазона при запросе по диапазону
    Country (str): страна поиска
    City (str): город поиска
    Arrival_date (data): дата заезда
    Departure_date (data): дата выезда
    Count_rooms (int): количество арендуемых номеров
    Count_adults (int): количество проживающих
    Count_children (int): количество детей
    """
    id = IntegerField(primary_key=True)
    User_id = ForeignKeyField(User)
    Type = CharField()
    Param_sort = CharField()
    Range = CharField(null=True)
    Country = CharField()
    City = CharField()
    Arrival_date = DateField()
    Departure_date = DateField()
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
    id (int): идентификатор записи
    Request_id (int): связующая запись с таблицей Request
    Name_hotels (str): название отеля
    Short_info (str): краткая информация по запросу
    Url_site (str): сайт отеля
    Photo (str): фотографии
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
