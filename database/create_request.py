"""
Запись запроса поиска в базу данных
"""

from datetime import datetime

from config_data import VariablesConstantsBot, VariablesMutableBot
from database import Request, User


def create_request_db(message: object, dict_result: dict, command: str) -> None:
    """
    Записывает данные для поиска которые ввел пользователь

    Parameters:
    message (object): class 'telebot.types.Message'
    dict_result (dict): словарь с данными для записи в базу данных
    command (str): команда бота

    Returns:
    None
    """
    user_id = User.get(User=message.from_user.id)
    arrival_date_str = "-".join([
        str(dict_result["arrival_year"]),
        str(dict_result["arrival_month"]),
        str(dict_result["arrival_day"])]
    )
    departure_date_str = "-".join([
        str(dict_result["departure_year"]),
        str(dict_result["departure_month"]),
        str(dict_result["departure_day"])]
    )
    arrival_date = datetime.strptime(arrival_date_str, "%Y-%m-%d").date()
    departure_date = datetime.strptime(departure_date_str, "%Y-%m-%d").date()
    if command == "high_state":
        search_type = "Лучший показатель"
        search_range = None
    elif command == "low_state":
        search_type = "Худший показатель"
        search_range = None
    else:
        search_type = "Диапазон"
        search_range = f"{dict_result['range_min']} - {dict_result['range_max']}"
    Request.create(
        User_id=user_id.id,
        Type=search_type,
        Param_sort=[
            key
            for key in VariablesConstantsBot.DICT_SORT_API_HOSTEL
            if VariablesConstantsBot.DICT_SORT_API_HOSTEL[key] == dict_result["sort"]
        ][0],
        Range=search_range,
        Country=dict_result["country"].capitalize(),
        City=dict_result["city"].capitalize(),
        Arrival_date=arrival_date,
        Departure_month=departure_date,
        Count_rooms=VariablesMutableBot.count_room,
        Count_adults=sum(dict_result["adults"]),
        Count_children=len(sum(dict_result["children_age"], []))
    )
