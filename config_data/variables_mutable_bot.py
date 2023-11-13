class VariablesMutableBot:
    """
    Класс для хранения изменяемых переменных

    Attributes:
    list_year (list): список с годами для создания клавиатуры
    list_month (list): список с числом месяца для создания клавиатуры
    list_days (list): список с числом дня месяца для создания клавиатуры
    list_del_filters (list): список со всеми фильтрами которые пользователю не надо выводить на клавиатуру
    list_del_accessibility (list): список специальных услуг в отеле, которые пользователю не надо выводить на клавиатуру
    list_del_traveler_type (list): список причин визита в отель, которые пользователю не надо выводить на клавиатуру
    list_del_meal_plan (list): список вариантов питания в отеле, которые пользователю не надо выводить на клавиатуру
    list_del_lodging (list): список вариантов размещения в отеле, которые пользователю не надо выводить на клавиатуру
    list_del_amenities (list): список услуг в отеле, которые пользователю не надо выводить на клавиатуру
    list_del_stars (list): список звездности отеля, которые пользователю не надо выводить на клавиатуру
    list_del_payment_type (list): список услуг оплаты в отеле, которые пользователю не надо выводить на клавиатуру
    list_del_bedroom_filter (list): список количества комнат в номере отеля, которые пользователю не надо выводить на клавиатуру
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
    list_del_filters = list()
    list_del_accessibility = list()
    list_del_traveler_type = list()
    list_del_meal_plan = list()
    list_del_lodging = list()
    list_del_amenities = list()
    list_del_stars = list()
    list_del_payment_type = list()
    list_del_bedroom_filter = list()
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
        cls.list_del_filters = list()
        cls.list_del_accessibility = list()
        cls.list_del_traveler_type = list()
        cls.list_del_meal_plan = list()
        cls.list_del_lodging = list()
        cls.list_del_amenities = list()
        cls.list_del_stars = list()
        cls.list_del_payment_type = list()
        cls.list_del_bedroom_filter = list()
        cls.count_room = 0
        cls.count_room_flag = 0
        cls.count_children = 0
        cls.count_children_flag = 0
        cls.year = False
        cls.month = False
