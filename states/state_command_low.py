from telebot.handler_backends import StatesGroup, State


class LowState(StatesGroup):
    """
    Класс состояний диалога с ботом при команде /low

    Attributes:
    city (object): class 'telebot.handler_backends.State'
    arrival_year (object): class 'telebot.handler_backends.State'
    arrival_month (object): class 'telebot.handler_backends.State'
    arrival_day (object): class 'telebot.handler_backends.State'
    departure_year (object): class 'telebot.handler_backends.State'
    departure_month (object): class 'telebot.handler_backends.State'
    departure_day (object): class 'telebot.handler_backends.State'
    room_count (object): class 'telebot.handler_backends.State'
    adults_count (object): class 'telebot.handler_backends.State'
    children_count (object): class 'telebot.handler_backends.State'
    children_age (object): class 'telebot.handler_backends.State'
    sort (object): class 'telebot.handler_backends.State'
    count (object): class 'telebot.handler_backends.State'

    Methods:
    None
    """
    city = State()
    arrival_year = State()
    arrival_month = State()
    arrival_day = State()
    departure_year = State()
    departure_month = State()
    departure_day = State()
    room_count = State()
    adults_count = State()
    children_count = State()
    children_age = State()
    sort = State()
    count = State()
