"""
Модуль с изменяемыми переменные
"""

from telebot import types
from typing import Optional

from config_data import FunctionsBot


class KeyboardsBot:
    """
    Класс содержащий клавиатуры для бота

    Attributes:
    None

    Methods:
    keyboard_start: создает клавиатуру для команды /start
    keyboard_year: создает клавиатуру календаря относительно списка list_year полученного из функции create_list_year
                   для выбора года
    keyboard_month: создает клавиатуру календаря относительно списка list_month полученного из функции create_list_month
                    для выбора месяца
    keyboard_day: создает клавиатуру календаря относительно списка list_day полученного из функции create_list_day
                  для выбора дня месяца
    keyboard_sort: создает клавиатуру для отображения возможной сортировки

    """

    @staticmethod
    def keyboard_start() -> object:
        """
        Создает клавиатуру для команды /start

        Parameters:
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
        Создает клавиатуру календаря относительно списка list_year
        полученного из функции create_list_year для выбора года

        Parameters:
        start_year (Optional[int]): год который передается а функцию create_list_year

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, selective=False)
        if not start_year:
            baton_list = [
                types.KeyboardButton(text=str(year))
                for year in FunctionsBot.create_list_year()
            ]
        else:
            baton_list = [
                types.KeyboardButton(text=str(year))
                for year in FunctionsBot.create_list_year(start_year=start_year)
            ]
        add_baton_list = []
        for baton in baton_list:
            add_baton_list.append(baton)
        rkm.add(*add_baton_list)
        return rkm

    @staticmethod
    def keyboard_month(start_month: Optional[int] = None) -> object:
        """
        Создает клавиатуру календаря относительно списка list_month
        полученного из функции create_list_month для выбора месяца

        Parameters:
        start_month (Optional[int]): число месяца которое передается а функцию create_list_month

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, selective=False)
        if not start_month:
            baton_list = [
                types.KeyboardButton(text=str(year))
                for year in FunctionsBot.create_list_month()
            ]
        else:
            baton_list = [
                types.KeyboardButton(text=str(year))
                for year in FunctionsBot.create_list_month(start_month=start_month)
            ]
        add_baton_list = []
        for baton in baton_list:
            add_baton_list.append(baton)
        rkm.add(*add_baton_list)
        return rkm

    @staticmethod
    def keyboard_day(year: int, month: int, start_day: Optional[int] = None) -> object:
        """
        Создает клавиатуру календаря относительно списка list_day
        полученного из функции create_list_day для выбора дня месяца

        Parameters:
        year (int): первый элемент списка list_year (год заселения в номер)
        month (int): первый элемент списка list_month (месяц заселения в номер)
        start_day (Optional[int]): число дня месяца от которого создается список

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=10, selective=False)
        if not start_day:
            baton_list = [
                types.KeyboardButton(text=day_1)
                for day_1 in FunctionsBot.create_list_day(year=year, month=month)
            ]
        else:
            baton_list = [
                types.KeyboardButton(text=day_1)
                for day_1 in FunctionsBot.create_list_day(year=year, month=month, start_day=start_day)
            ]
        add_baton_list = []
        for baton in baton_list:
            add_baton_list.append(baton)
        rkm.add(*add_baton_list)
        return rkm

    @staticmethod
    def keyboard_sort() -> object:
        """
        Создает клавиатуру для отображения возможной сортировки

        Parameters:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, selective=False)
        rkm.add(
            types.KeyboardButton(text="Сортировка по ценам"),
            types.KeyboardButton(text="Сортировка по оценкам проживающих"),
            types.KeyboardButton(text="Сортировка по расстоянию до центра"),
            types.KeyboardButton(text="Сортировка по звездности отелей")
        )
        return rkm
