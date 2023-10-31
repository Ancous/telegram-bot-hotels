import time
from calendar import monthrange
from datetime import datetime
from typing import Optional

from config_data.variables_constants_bot import VariablesConstants
from config_data.variables_mutable_bot import VariablesMutable


class Functions:
    """
    Class description:
    Класс хранения функций для работы бота

    Attributes:
    None

    Methods:
    welcome: формирует текст приветствия при выполнении команды /start
    create_list_year: создает список с годами для создания клавиатуры
    create_list_month : создает список с числом месяца для создания клавиатуры
    create_list_day: создает список с числом дня месяца для создания клавиатуры
    conversation_transition: отлавливает из введенного текста пользователя команды и вызывает нужную функции

    """
    @staticmethod
    def welcome(name: str) -> str:
        """
        Function description:
        Формирует текст приветствия при выполнении команды /start

        Parameters:
        name (str): имя пользователя

        Returns:
        str: текст приветствия
        """
        time_now = time.localtime(time.time()).tm_hour
        if 0 <= time_now <= 5:
            welcome_text = "Доброй ночи"
        elif 6 <= time_now <= 11:
            welcome_text = "Доброе утро"
        elif 12 <= time_now <= 17:
            welcome_text = "Добрый день"
        else:
            welcome_text = "Добрый вечер"
        return (f"{welcome_text} {name}. Для дальнейшего использования бота нажмите одну из кнопок ниже.\n"
                f"/start - начало диалога с ботом\n"
                f"/help - информация по кнопкам и командам\n"
                f"/low - вывод худших показателей\n"
                f"/high - вывод лучших показателей\n"
                f"/custom - вывод показателей пользовательского диапазона\n"
                f"/history - вывод истории запросов пользователей")

    @staticmethod
    def create_list_year(start_year: Optional[int] = None) -> list:
        """
        Function description:
        Создает список с годами для создания клавиатуры

        Parameters:
        start_year (Optional[int]): год от которого создается список

        Returns:
        list: список с годами для создания клавиатуры
        """
        count_keyboard = 6
        if start_year:
            difference = start_year - datetime.now().year
            new_count_keyboard = count_keyboard + start_year - datetime.now().year
            new_list_year = [str(datetime.now().year + year) for year in range(new_count_keyboard)]
            VariablesMutable.list_year = new_list_year[difference:]
            return new_list_year[difference:]
        else:
            VariablesMutable.list_year = [str(datetime.now().year + year) for year in range(count_keyboard)]
            return VariablesMutable.list_year

    @staticmethod
    def create_list_month(start_month: Optional[int] = None) -> list:
        """
        Function description:
        Создает список с числом месяца для создания клавиатуры

        Parameters:
        start_year (Optional[int]): число месяца от которого создается список

        Returns:
        list: список с числом месяца для создания клавиатуры
        """
        if start_month:
            new_list_month = list()
            flag = False
            for key, values in VariablesConstants.DICT_MOUNT_STR_INT.items():
                if flag:
                    new_list_month.append(key)
                if not flag and start_month == values:
                    flag = True
                    new_list_month.append(key)
            VariablesMutable.list_month = new_list_month
            return new_list_month
        else:
            VariablesMutable.list_month = [str(month) for month in VariablesConstants.DICT_MOUNT_STR_INT]
            return VariablesMutable.list_month

    @staticmethod
    def create_list_day(year: int, month: int, start_day: Optional[int] = None) -> list:
        """
        Function description:
        Создает список с числом дня месяца для создания клавиатуры

        Parameters:
        year (int): первый элемент списка list_year (год заселения в номер)
        month (int): первый элемент списка list_month (месяц заселения в номер)
        start_day (Optional[int]): число дня месяца от которого создается список

        Returns:
        list: список с числом дня месяца для создания клавиатуры
        """
        days = monthrange(int(year), int(month))[1]
        if start_day:
            new_list_days = list()
            flag = False
            for day_1 in VariablesMutable.list_days:
                if flag:
                    new_list_days.append(day_1)
                if not flag and start_day == int(day_1):
                    flag = True
            VariablesMutable.list_days = new_list_days
            return new_list_days
        else:
            VariablesMutable.list_days = [str(day + 1) for day in range(days)]
            return VariablesMutable.list_days

    @staticmethod
    def conversation_transition(message: object) -> None:
        """
        Function description:
        Отлавливает из введенного текста пользователя команды и вызывает нужную функции

        Parameters:
        message (object): class 'telebot.types.Message'

        Returns:
        None
        """
        import handlers
        if message.text == "/start":
            handlers.handlers_command_start.start(message)
        if message.text == "/help":
            handlers.handlers_command_help.my_help(message)
        if message.text == "/high":
            handlers.handlers_command_high.state_high_start(message)
        if message.text == "/low":
            handlers.handlers_command_low.state_low_start(message)
        # if message.text == "/custom":
        #     state_custom_start(message)
        # if message.text == "/history":
        #     history(message)
