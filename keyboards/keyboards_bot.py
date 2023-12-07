from telebot import types
from typing import Optional

from config_data import FunctionsBot, VariablesMutableBot


class KeyboardsBot:
    """
    Класс содержащий клавиатуры для бота

    Attributes:
    None

    Methods:
    keyboard_start: создает клавиатуру для команды /start
    keyboard_year: создает клавиатуру календаря относительно списка list_year полученного из функции create_list_year для выбора года
    keyboard_month: создает клавиатуру календаря относительно списка list_month полученного из функции create_list_month для выбора месяца
    keyboard_day: создает клавиатуру календаря относительно списка list_day полученного из функции create_list_day для выбора дня месяца
    keyboard_sort: создает клавиатуру для отображения возможной сортировки
    keyboard_filter: создает клавиатуру для отображения возможных фильтров
    keyboard_guest_rating: создает клавиатуру для выбора оценки, которую пользователь хочет видеть в предложенных результатах
    keyboard_accessibility: создает клавиатуру для выбора специальных услуг, которые пользователь хочет видеть в предложенных результатах
    keyboard_traveler_type: создает клавиатуру для выбора причин визита в отель, которую пользователь хочет видеть в предложенных результатах
    keyboard_meal_plan: создает клавиатуру для выбора вариантов питания, которую пользователь хочет видеть в предложенных результатах
    keyboard_lodging: создает клавиатуру для выбора вариантов размещения, которую пользователь хочет видеть в предложенных результатах
    keyboard_amenities: создает клавиатуру для выбора вариантов услуг в отеле, которую пользователь хочет видеть в предложенных результатах
    keyboard_stars: создает клавиатуру для выбора вариантов звездности отеля, которую пользователь хочет видеть в предложенных результатах
    keyboard_payment_type: создает клавиатуру для выбора вариантов услуг оплаты, которую пользователь хочет видеть в предложенных результатах
    keyboard_bedroom_filter: создает клавиатуру для выбора количества комнат в номере отеля, которую пользователь хочет видеть в предложенных результатах
    keyboard_available_filter: создает клавиатуру для выбора показа только "свободных номеров на нужные даты" или "все"
    """
    @staticmethod
    def keyboard_start() -> object:
        """
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
        Создает клавиатуру календаря относительно списка list_year
        полученного из функции create_list_year для выбора года

        Arguments:
        start_year (Optional[int]): год который передается а функцию create_list_year

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, selective=False)
        if not start_year:
            baton_list = [types.KeyboardButton(text=str(year)) for year in FunctionsBot.create_list_year()]
        else:
            baton_list = [types.KeyboardButton(text=str(year)) for year in FunctionsBot.create_list_year(start_year=start_year)]
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

        Arguments:
        start_month (Optional[int]): число месяца которое передается а функцию create_list_month

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, selective=False)
        if not start_month:
            baton_list = [types.KeyboardButton(text=str(year)) for year in FunctionsBot.create_list_month()]
        else:
            baton_list = [types.KeyboardButton(text=str(year)) for year in FunctionsBot.create_list_month(start_month=start_month)]
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

        Arguments:
        year (int): первый элемент списка list_year (год заселения в номер)
        month (int): первый элемент списка list_month (месяц заселения в номер)
        start_day (Optional[int]): число дня месяца от которого создается список

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=10, selective=False)
        if not start_day:
            baton_list = [types.KeyboardButton(text=day_1) for day_1 in FunctionsBot.create_list_day(year=year, month=month)]
        else:
            baton_list = [types.KeyboardButton(text=day_1) for day_1 in FunctionsBot.create_list_day(year=year, month=month, start_day=start_day)]
        add_baton_list = []
        for baton in baton_list:
            add_baton_list.append(baton)
        rkm.add(*add_baton_list)
        return rkm

    @staticmethod
    def keyboard_sort() -> object:
        """
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
            types.KeyboardButton(text="Сортировка по расстоянию до центра"),
            types.KeyboardButton(text="Сортировка по звездности отелей")
        )
        return rkm

    @staticmethod
    def keyboard_filter() -> object:
        """
        Создает клавиатуру для отображения возможных фильтров

        Arguments:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, selective=False)
        baton_list = [
            types.KeyboardButton(text="Завершить с выбором фильтров"),
            types.KeyboardButton(text="Фильтр по ценам"),
            types.KeyboardButton(text="Фильтр по названию отеля"),
            types.KeyboardButton(text="Фильтр по оценкам проживающих"),
            types.KeyboardButton(text="Фильтр по специальным услугам"),
            types.KeyboardButton(text="Фильтр по причине визита"),
            types.KeyboardButton(text="Фильтр по питанию"),
            types.KeyboardButton(text="Фильтр по типу размещения"),
            types.KeyboardButton(text="Фильтр по услугам"),
            types.KeyboardButton(text="Фильтр по звездности отелей"),
            types.KeyboardButton(text="Фильтр по услугам оплаты"),
            types.KeyboardButton(text="Фильтр по количеству комнат в номере"),
            types.KeyboardButton(text="Фильтр по свободным номерам на нужные даты")
        ]
        new_baton_list = list()
        for baton in baton_list:
            if not baton.text in VariablesMutableBot.list_del_filters:
                new_baton_list.append(baton)
        rkm.add(*new_baton_list)
        return rkm

    @staticmethod
    def keyboard_guest_rating() -> object:
        """
        Создает клавиатуру для выбора оценки, которую пользователь хочет видеть в предложенных результатах

        Arguments:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5, selective=False)
        rkm.add(
            types.KeyboardButton(text="Минимальная оценка 7"),
            types.KeyboardButton(text="Минимальная оценка 8"),
            types.KeyboardButton(text="Минимальная оценка 9")
        )
        return rkm

    @staticmethod
    def keyboard_accessibility() -> object:
        """
        Создает клавиатуру для выбора специальных услуг, которые пользователь хочет видеть в предложенных результатах

        Arguments:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, selective=False)
        baton_list = [
            types.KeyboardButton(text="Завершить с выбором специальных услуг"),
            types.KeyboardButton(text="Сурдопереводчик"),
            types.KeyboardButton(text="Лесница для инвалидов"),
            types.KeyboardButton(text="Сервис для животных"),
            types.KeyboardButton(text="Лифт"),
            types.KeyboardButton(text="Комната для инвалидов"),
            types.KeyboardButton(text="Душевая кабина в уровень пола"),
            types.KeyboardButton(text="Душевая кабина для инвалидов"),
            types.KeyboardButton(text="Парковка для инвалидов")
        ]
        new_baton_list = list()
        for baton in baton_list:
            if not baton.text in VariablesMutableBot.list_del_accessibility:
                new_baton_list.append(baton)
        rkm.add(*new_baton_list)
        return rkm

    @staticmethod
    def keyboard_traveler_type() -> object:
        """
        Создает клавиатуру для выбора причин визита в отель,
        которую пользователь хочет видеть в предложенных результатах

        Arguments:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, selective=False)
        baton_list = [
            types.KeyboardButton(text="Завершить с выбором причины визита"),
            types.KeyboardButton(text="По работе"),
            types.KeyboardButton(text="По семейным обстоятельствам")
        ]
        new_baton_list = list()
        for baton in baton_list:
            if not baton.text in VariablesMutableBot.list_del_traveler_type:
                new_baton_list.append(baton)
        rkm.add(*new_baton_list)
        return rkm

    @staticmethod
    def keyboard_meal_plan() -> object:
        """
        Создает клавиатуру для выбора вариантов питания, которую пользователь хочет видеть в предложенных результатах

        Arguments:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, selective=False)
        baton_list = [
            types.KeyboardButton(text="Завершить с выбором вариантов питания"),
            types.KeyboardButton(text="Бесплатный завтрак"),
            types.KeyboardButton(text="Полупансион"),
            types.KeyboardButton(text="Полный пансион"),
            types.KeyboardButton(text="Всё включено")
        ]
        new_baton_list = list()
        for baton in baton_list:
            if not baton.text in VariablesMutableBot.list_del_meal_plan:
                new_baton_list.append(baton)
        rkm.add(*new_baton_list)
        return rkm

    @staticmethod
    def keyboard_lodging() -> object:
        """
        Создает клавиатуру для выбора вариантов размещения, которую пользователь хочет видеть в предложенных результатах

        Arguments:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, selective=False)
        baton_list = [
            types.KeyboardButton(text="Завершить с выбором типа размещения"),
            types.KeyboardButton(text="Вилла"),
            types.KeyboardButton(text="Апартаменты"),
            types.KeyboardButton(text="Пансион"),
            types.KeyboardButton(text="Таунхаус"),
            types.KeyboardButton(text="Агротуризм"),
            types.KeyboardButton(text="Отель"),
            types.KeyboardButton(text="Коттеджный поселок"),
            types.KeyboardButton(text="Квартира")
        ]
        new_baton_list = list()
        for baton in baton_list:
            if not baton.text in VariablesMutableBot.list_del_lodging:
                new_baton_list.append(baton)
        rkm.add(*new_baton_list)
        return rkm

    @staticmethod
    def keyboard_amenities() -> object:
        """
        Создает клавиатуру для выбора вариантов услуг в отеле,
        которую пользователь хочет видеть в предложенных результатах

        Arguments:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, selective=False)
        baton_list = [
            types.KeyboardButton(text="Завершить с выбором желаемых услуг в отеле"),
            types.KeyboardButton(text="Бесплатный транспорт в аэропорт"),
            types.KeyboardButton(text="Вид на океан"),
            types.KeyboardButton(text="Джакузи"),
            types.KeyboardButton(text="Домашние животные"),
            types.KeyboardButton(text="Казино"),
            types.KeyboardButton(text="Спа"),
            types.KeyboardButton(text="Детская кроватка"),
            types.KeyboardButton(text="Балкон или терраса"),
            types.KeyboardButton(text="Стоянка"),
            types.KeyboardButton(text="Электромобиль"),
            types.KeyboardButton(text="Ресторан в отеле"),
            types.KeyboardButton(text="Кухня"),
            types.KeyboardButton(text="Спортзал"),
            types.KeyboardButton(text="Бассейн"),
            types.KeyboardButton(text="Стиральная машина и сушилка"),
            types.KeyboardButton(text="Аквапарк"),
            types.KeyboardButton(text="Кондиционер"),
            types.KeyboardButton(text="Wi-fi")
        ]
        new_baton_list = list()
        for baton in baton_list:
            if not baton.text in VariablesMutableBot.list_del_amenities:
                new_baton_list.append(baton)
        rkm.add(*new_baton_list)
        return rkm

    @staticmethod
    def keyboard_stars() -> object:
        """
        Создает клавиатуру для выбора вариантов звездности отеля,
        которую пользователь хочет видеть в предложенных результатах

        Arguments:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5, selective=False)
        baton_list = [
            types.KeyboardButton(text="1"),
            types.KeyboardButton(text="2"),
            types.KeyboardButton(text="3"),
            types.KeyboardButton(text="4"),
            types.KeyboardButton(text="5")
        ]
        new_baton_list = list()
        for baton in baton_list:
            if not baton.text in VariablesMutableBot.list_del_stars:
                new_baton_list.append(baton)
        rkm.add(types.KeyboardButton(text="Завершить с выбором звёздности отеля"))
        rkm.add(*new_baton_list)
        return rkm

    @staticmethod
    def keyboard_payment_type() -> object:
        """
        Создает клавиатуру для выбора вариантов услуг оплаты,
        которую пользователь хочет видеть в предложенных результатах

        Arguments:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, selective=False)
        baton_list = [
            types.KeyboardButton(text="Завершить с выбором услуг по оплате"),
            types.KeyboardButton(text="Бесплатное аннулирование"),
            types.KeyboardButton(text="Оплата при заселении")
        ]
        new_baton_list = list()
        for baton in baton_list:
            if not baton.text in VariablesMutableBot.list_del_payment_type:
                new_baton_list.append(baton)
        rkm.add(*new_baton_list)
        return rkm

    @staticmethod
    def keyboard_bedroom_filter() -> object:
        """
        Создает клавиатуру для выбора количества комнат в номере отеля,
        которую пользователь хочет видеть в предложенных результатах

        Arguments:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, selective=False)
        baton_list = [
            types.KeyboardButton(text="Завершить с выбором количества комнат в номере"),
            types.KeyboardButton(text="Студия"),
            types.KeyboardButton(text="Одна комната"),
            types.KeyboardButton(text="Две комната"),
            types.KeyboardButton(text="Три комната"),
            types.KeyboardButton(text="Четыре комната")
        ]
        new_baton_list = list()
        for baton in baton_list:
            if not baton.text in VariablesMutableBot.list_del_bedroom_filter:
                new_baton_list.append(baton)
        rkm.add(*new_baton_list)
        return rkm

    @staticmethod
    def keyboard_available_filter() -> object:
        """
        Создает клавиатуру для выбора показа только "свободных номеров на нужные даты" или "все"

        Arguments:
        None

        Returns:
        object: class 'telebot.types.ReplyKeyboardMarkup'
        """
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5, selective=False)
        rkm.add(
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        )
        return rkm
