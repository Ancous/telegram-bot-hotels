"""
Модуль с постоянными(неизменяемыми) переменными в работе бота
"""

import os
import telebot

from dotenv import load_dotenv

load_dotenv()


class VariablesConstantsBot:
    """
    Класс для хранения постоянных переменных

    Attributes:
    BOT (object): class 'telebot.TeleBot' для запуска бота
    DB_PATH (str): название базы данных
    COMMANDS (tuple): кортеж с командами бота
    DESCRIPTION_COMMANDS (str): описание команд бота
    DICT_SORT_API_HOSTEL (dict): словарь для вывода пользователю возможной сортировки и перевода значений сортировки
                                 для работы с API-Hotels.com
    DICT_MOUNT_STR_INT (dict): словарь для перевода строкового значения месяца в числовое значение
    """
    BOT = telebot.TeleBot(os.getenv("TOKEN_BOT"))
    DB_PATH = "UserDatabase.db"
    COMMANDS = ("/start", "/help", "/low", "/high", "/custom", "/history")
    DESCRIPTION_COMMANDS = (
        "/start............начало диалога с ботом\n"
        "/help.............информация по кнопкам и командам\n"
        "/high.............вывод лучших показателей\n"
        "/low...............вывод худших показателей\n"
        "/custom.......вывод показателей пользовательского диапазона\n"
        "/history........вывод истории запросов"
    )
    DICT_SORT_API_HOSTEL = {
        "Сортировка по ценам": "PRICE_LOW_TO_HIGH",
        "Сортировка по оценкам проживающих": "REVIEW",
        "Сортировка по расстоянию до центра": "DISTANCE",
        "Сортировка по звездности отелей": "PROPERTY_CLASS",
    }
    DICT_MOUNT_STR_INT = {
        "Январь": 1, "Февраль": 2, "Март": 3, "Апрель": 4,
        "Май": 5, "Июнь": 6, "Июль": 7, "Август": 8,
        "Сентябрь": 9, "Октябрь": 10, "Ноябрь": 11, "Декабрь": 12
    }
