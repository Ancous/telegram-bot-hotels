from telebot import types
from typing import Optional

from config_data import Functions


class Keyboards:

    @staticmethod
    def keyboard_start() -> object:
        """
        Function description:
        Создает клавиатуру для команды /start

        Arguments:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        rkm.add(
            types.KeyboardButton(text="/start"),
            types.KeyboardButton(text="/help"),
            types.KeyboardButton(text="/low"),
            types.KeyboardButton(text="/high"),
            types.KeyboardButton(text="/custom"),
            types.KeyboardButton(text="/history")
        )
        return rkm

    @staticmethod
    def keyboard_year(start_year: Optional[int] = None) -> object:
        """
        Function description:
        Создает пользователю клавиатуру календаря относительно списка list_year
        полученного из функции create_list_year для выбора года

        Arguments:
        start_year (Optional[int]): год который передается а функцию create_list_year

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, selective=False)
        if not start_year:
            baton_list = [types.KeyboardButton(text=str(year)) for year in Functions.create_list_year()]
        else:
            baton_list = [types.KeyboardButton(text=str(year)) for year in
                          Functions.create_list_year(start_year=start_year)]
        add_baton_list = []
        for baton in baton_list:
            add_baton_list.append(baton)
        rkm.add(*add_baton_list)
        return rkm

    @staticmethod
    def keyboard_month(start_month: Optional[int] = None) -> object:
        """
        Function description:
        Создает пользователю клавиатуру календаря относительно списка list_month
        полученного из функции create_list_month для выбора месяца

        Arguments:
        start_month (Optional[int]): число месяца которое передается а функцию create_list_month

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, selective=False)
        if not start_month:
            baton_list = [types.KeyboardButton(text=str(year)) for year in Functions.create_list_month()]
        else:
            baton_list = [types.KeyboardButton(text=str(year)) for year in
                          Functions.create_list_month(start_month=start_month)]
        add_baton_list = []
        for baton in baton_list:
            add_baton_list.append(baton)
        rkm.add(*add_baton_list)
        return rkm

    @staticmethod
    def keyboard_day(year: int, month: int, start_day: Optional[int] = None) -> object:
        """
        Function description:
        Создает пользователю клавиатуру календаря относительно списка list_day
        полученного из функции create_list_day для выбора дня месяца

        Arguments:
        year (int): первый элемент списка list_year (год заселения в номер)
        month (int): первый элемент списка list_month (месяц заселения в номер)
        start_day (Optional[int]): число дня месяца от которого создается список

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=10, selective=False)
        if not start_day:
            baton_list = [types.KeyboardButton(text=day_1) for day_1 in
                          Functions.create_list_day(year=year, month=month)]
        else:
            baton_list = [types.KeyboardButton(text=day_1) for day_1 in
                          Functions.create_list_day(year=year, month=month, start_day=start_day)]
        add_baton_list = []
        for baton in baton_list:
            add_baton_list.append(baton)
        rkm.add(*add_baton_list)
        return rkm

    @staticmethod
    def keyboard_sort() -> object:
        """
        Function description:
        Создает клавиатуру для отображения возможной сортировки

        Arguments:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, selective=False)
        rkm.add(
            types.KeyboardButton(text="Сортировка по ценам"),
            types.KeyboardButton(text="Сортировка по оценкам проживающих"),
            types.KeyboardButton(text="Сортировка по расстоянию от центра"),
            types.KeyboardButton(text="Сортировка по звездности отелей"),
            types.KeyboardButton(text="Сортировка по количеству отзывов проживающих")
        )
        return rkm