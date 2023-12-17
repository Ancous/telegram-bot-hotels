"""
Модуль с описанием состояния диалога с ботом при команде custom
"""

from telebot.handler_backends import StatesGroup, State


class CustomState(StatesGroup):
    """
    Класс состояний диалога с ботом при команде /custom

    Attributes:
    country (object): class 'telebot.handler_backends.State'
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
    range_price (object): class 'telebot.handler_backends.State'
    range_review (object): class 'telebot.handler_backends.State'
    range_distance (object): class 'telebot.handler_backends.State'
    range_star (object): class 'telebot.handler_backends.State'
    count (object): class 'telebot.handler_backends.State'

    Methods:
    None
    """
    country = State()
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
    range_price = State()
    range_review = State()
    range_distance = State()
    range_star = State()
    count = State()
