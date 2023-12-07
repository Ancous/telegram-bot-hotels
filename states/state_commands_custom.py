from telebot.handler_backends import StatesGroup, State


class CustomState(StatesGroup):
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
    sort (object): class 'telebot.handler_backends.State'
    filters (object): class 'telebot.handler_backends.State'
    filters_price (object): class 'telebot.handler_backends.State'
    filters_hotel_name (object): class 'telebot.handler_backends.State'
    filters_guest_rating (object): class 'telebot.handler_backends.State'
    filters_accessibility (object): class 'telebot.handler_backends.State'
    filters_traveler_type (object): class 'telebot.handler_backends.State'
    filters_meal_plan (object): class 'telebot.handler_backends.State'
    filters_lodging (object): class 'telebot.handler_backends.State'
    filters_amenities (object): class 'telebot.handler_backends.State'
    filters_stars (object): class 'telebot.handler_backends.State'
    filters_payment_type (object): class 'telebot.handler_backends.State'
    filters_bedroom_filter (object): class 'telebot.handler_backends.State'
    filters_available_filter (object): class 'telebot.handler_backends.State'
    room_count (object): class 'telebot.handler_backends.State'
    adults_count (object): class 'telebot.handler_backends.State'
    children_count (object): class 'telebot.handler_backends.State'
    children_age (object): class 'telebot.handler_backends.State'
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
    sort = State()
    filters = State()
    filters_price = State()
    filters_hotel_name = State()
    filters_guest_rating = State()
    filters_accessibility = State()
    filters_traveler_type = State()
    filters_meal_plan = State()
    filters_lodging = State()
    filters_amenities = State()
    filters_stars = State()
    filters_payment_type = State()
    filters_bedroom = State()
    filters_available = State()
    room_count = State()
    adults_count = State()
    children_count = State()
    children_age = State()
    count = State()
