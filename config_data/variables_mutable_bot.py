"""
Модуль с изменяемыми переменными в работе бота
"""


class VariablesMutableBot:
    """
    Класс для хранения изменяемых переменных

    Attributes:
    list_year (list): список с годами для создания клавиатуры
    list_month (list): список с числом месяца для создания клавиатуры
    list_days (list): список с числом дня месяца для создания клавиатуры
    count_range (int): минимальный показатель диапазона отбора отелей
    count_room (int): количество номеров
    count_room_flag (int): флаг-счетчик для отслеживания перехода к следующему состоянию диалога с ботом
    count_children (int): количество детей в номере
    count_children_flag (int): флаг-счетчик для отслеживания перехода к сбору данных следующего номера
    year (bool): флаг по выбору пользователем года (нынешней год или нет)
    month (bool): флаг по выбору пользователем месяца (нынешней месяц или нет)

    Methods:
    reset_parameters: обновляет все атрибуты класса
    """
    list_year = list()
    list_month = list()
    list_days = list()
    count_range = 0
    count_room = 0
    count_room_flag = 0
    count_children = 0
    count_children_flag = 0
    year = False
    month = False

    @classmethod
    def reset_parameters(cls) -> None:
        """
        Обновляет все атрибуты класса VariablesMutable

        Parameters:
        None

        Returns:
        None
        """
        cls.list_year = list()
        cls.list_month = list()
        cls.list_days = list()
        cls.count_range = 0
        cls.count_room = 0
        cls.count_room_flag = 0
        cls.count_children = 0
        cls.count_children_flag = 0
        cls.year = False
        cls.month = False
