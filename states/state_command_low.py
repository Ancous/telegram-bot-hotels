from telebot.handler_backends import StatesGroup, State


class LowState(StatesGroup):
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
