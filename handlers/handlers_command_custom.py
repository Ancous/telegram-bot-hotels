"""
Модуль поддержания состояния диалога с пользователем по команде custom
"""

import telebot
from telebot.types import ReplyKeyboardRemove
from datetime import datetime

from config_data import VariablesMutableBot, VariablesConstantsBot, FunctionsBot
from database import create_request_db, create_response_db
from hotels_api import checking_city_country_recording_city_id, CustomApi
from keyboards import KeyboardsBot
from states import CustomState


@VariablesConstantsBot.BOT.message_handler(state="*", commands=["custom"])
def state_custom_start(message) -> None:
    """
    Функция начального состояния диалога с ботом по команде custom
    Обновляет все атрибуты класса VariablesMutable

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    VariablesMutableBot.reset_parameters()
    VariablesConstantsBot.BOT.send_message(
        chat_id=message.from_user.id,
        text="В какой стране будем производить подбор отелей:",
        reply_markup=ReplyKeyboardRemove()
    )
    VariablesConstantsBot.BOT.set_state(
        user_id=message.from_user.id,
        state=CustomState.country
    )
    with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
        data["custom_state"] = {}


@VariablesConstantsBot.BOT.message_handler(state=CustomState.country)
def state_custom_country(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Производит запись страны для поиска

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
        data["custom_state"]["country"] = message.text
    VariablesConstantsBot.BOT.send_message(
        chat_id=message.from_user.id,
        text="В каком городе:"
    )
    VariablesConstantsBot.BOT.set_state(
        user_id=message.from_user.id,
        state=CustomState.city
    )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.city)
def state_custom_city(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Проверяет наличие id-города по запросу к hostel-api
    Производит запись id-города для поиска

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
        data["custom_state"]["city"] = message.text
    city_id = checking_city_country_recording_city_id(
        dict_result=data["custom_state"]
    )
    if not city_id:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Страна или город с таким названием не были найдены.\n"
                 "Введите стану и город еще раз.\n"
                 "В какой стране производим поиск."
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.country
        )
    else:
        data["custom_state"]["city_id"] = city_id
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Определитесь с датой заезда в отель.\nЗаезд. Выберите год:",
            reply_markup=KeyboardsBot.keyboard_year()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.arrival_year
        )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.arrival_year)
def state_custom_arrival_year(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Производит запись года заселения в номер

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text in VariablesMutableBot.list_year:
        if int(message.text) == datetime.now().year:
            VariablesMutableBot.year = True
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["custom_state"]["arrival_year"] = int(message.text)
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Заезд. Выберите месяц:",
            reply_markup=KeyboardsBot.keyboard_month()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.arrival_month
        )
        return
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nЗаезд. Выберите год предложенный ниже:",
            reply_markup=KeyboardsBot.keyboard_year()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.arrival_year
        )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.arrival_month)
def state_custom_arrival_month(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Производит запись месяца заселения в номер

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text.capitalize() in VariablesMutableBot.list_month:
        if VariablesConstantsBot.DICT_MOUNT_STR_INT.get(message.text.capitalize()) == datetime.now().month:
            VariablesMutableBot.month = True
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["custom_state"]["arrival_month"] = VariablesConstantsBot.DICT_MOUNT_STR_INT[message.text.capitalize()]
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Заезд. Выберите день:",
            reply_markup=KeyboardsBot.keyboard_day(
                year=data["custom_state"]["arrival_year"],
                month=data["custom_state"]["arrival_month"]
            )
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.arrival_day
        )
        return
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nЗаезд. Выберите месяц предложенный ниже:",
            reply_markup=KeyboardsBot.keyboard_month()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.arrival_month
        )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.arrival_day)
def state_custom_arrival_day(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Производит запись дня заселения в номер

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
        if message.text in VariablesMutableBot.list_days:
            data["custom_state"]["arrival_day"] = int(message.text)
            VariablesMutableBot.year = False
            VariablesMutableBot.month = False
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Определитесь с датой выезда из отель.\nВыезд. Выберите год:",
                reply_markup=KeyboardsBot.keyboard_year(
                    data["custom_state"]["arrival_year"]
                )
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.departure_year
            )
            return
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Неверный ввод.\nЗаезд. Выберите день предложенный ниже:",
                reply_markup=KeyboardsBot.keyboard_day(
                    year=data["custom_state"]["arrival_year"],
                    month=data["custom_state"]["arrival_month"]
                )
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.arrival_day
            )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.departure_year)
def state_custom_departure_year(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Производит запись года выезда из номера

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
        if message.text in VariablesMutableBot.list_year:
            data["custom_state"]["departure_year"] = int(message.text)
            if not data["custom_state"]["arrival_year"] == data["custom_state"]["departure_year"]:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Выезд. Выберите месяц:",
                    reply_markup=KeyboardsBot.keyboard_month()
                )
            else:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Выезд. Выберите месяц:",
                    reply_markup=KeyboardsBot.keyboard_month(data["custom_state"]["arrival_month"])
                )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.departure_month
            )
            return
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Неверный ввод.\nВыезд. Выберите год предложенный ниже:",
                reply_markup=KeyboardsBot.keyboard_year(data["custom_state"]["arrival_year"])
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.departure_year
            )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.departure_month)
def state_custom_departure_month(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Производит запись месяца выезда из номера

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
        if message.text.capitalize() in VariablesMutableBot.list_month:
            data["custom_state"]["departure_month"] = VariablesConstantsBot.DICT_MOUNT_STR_INT[
                message.text.capitalize()
            ]
            if (int(data["custom_state"]["arrival_year"]) == int(data["custom_state"]["departure_year"]) and
                    int(data["custom_state"]["arrival_month"]) == int(data["custom_state"]["departure_month"])):
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Выезд. Выберите день:",
                    reply_markup=KeyboardsBot.keyboard_day(
                        year=int(data["custom_state"]["departure_year"]),
                        month=int(data["custom_state"]["departure_month"]),
                        start_day=int(data["custom_state"]["arrival_day"])
                    )
                )
            else:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Выезд. Выберите день:",
                    reply_markup=KeyboardsBot.keyboard_day(
                        year=data["custom_state"]["departure_year"],
                        month=data["custom_state"]["departure_month"]
                    )
                )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.departure_day
            )
        else:
            if not data["custom_state"]["arrival_year"] == data["custom_state"]["departure_year"]:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Неверный ввод.\nВыезд. Выберите месяц предложенный ниже:",
                    reply_markup=KeyboardsBot.keyboard_month()
                )
            else:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Неверный ввод.\nВыезд. Выберите месяц предложенный ниже:",
                    reply_markup=KeyboardsBot.keyboard_month(data["custom_state"]["arrival_month"])
                )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.departure_month
            )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.departure_day)
def state_custom_departure_day(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Производит запись дня выезда из номера

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
        if message.text in VariablesMutableBot.list_days:
            data["custom_state"]["departure_day"] = int(message.text)
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.room_count
            )
        else:
            if (int(data["custom_state"]["arrival_year"]) == int(data["custom_state"]["departure_year"]) and
                    int(data["custom_state"]["arrival_month"]) == int(data["custom_state"]["departure_month"])):
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Неверный ввод.\nВыезд. Выберите день предложенный ниже:",
                    reply_markup=KeyboardsBot.keyboard_day(
                        year=data["custom_state"]["departure_year"],
                        month=data["custom_state"]["departure_month"],
                        start_day=data["custom_state"]["arrival_day"]
                    )
                )
            else:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Неверный ввод.\nВыезд. Выберите день предложенный ниже:",
                    reply_markup=KeyboardsBot.keyboard_day(
                        year=data["custom_state"]["departure_year"],
                        month=data["custom_state"]["departure_month"]
                    )
                )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.departure_day
            )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.room_count)
def state_custom_room_count(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Запоминает количество арендуемых номеров

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text.isdigit() and int(message.text) >= 1:
        VariablesMutableBot.count_room = int(message.text)
        VariablesMutableBot.count_room_flag += 1
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text=f"Количество взрослых в {VariablesMutableBot.count_room_flag}-ом номере:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.adults_count
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВведите количество номеров в положительном числовом выражении:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.room_count
        )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.adults_count)
def state_custom_adults_count(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Производит запись о количестве проживающих в номере

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text.isdigit() and int(message.text) >= 1:
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if "adults" in data["custom_state"]:
                data["custom_state"]["adults"].append(int(message.text))
            else:
                data["custom_state"]["adults"] = [int(message.text)]
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text=f"Количество детей в {VariablesMutableBot.count_room_flag}-ом номере:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.children_count
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВведите количество взрослых в положительном числовом выражении:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.adults_count
        )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.children_count)
def state_custom_children_count(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Запоминает количество детей и производит запись о детях если понадобится

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text.isdigit() and int(message.text) >= 0:
        VariablesMutableBot.count_children = int(message.text)
        if not VariablesMutableBot.count_children == 0:
            VariablesMutableBot.count_children_flag += 1
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Возраст {VariablesMutableBot.count_children_flag}-ого ребенка:",
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.children_age
            )
        elif not VariablesMutableBot.count_room == VariablesMutableBot.count_room_flag:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if "children_age" in data["custom_state"]:
                    data["custom_state"]["children_age"].append([])
                else:
                    data["custom_state"]["children_age"] = [[]]
            VariablesMutableBot.count_room_flag += 1
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Количество взрослых в {VariablesMutableBot.count_room_flag}-ом номере:",
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.adults_count
            )
        else:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if "children_age" in data["custom_state"]:
                    data["custom_state"]["children_age"].append([])
                else:
                    data["custom_state"]["children_age"] = [[]]
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.chat.id,
                text="По какой категории отсортировать показатели:",
                reply_markup=KeyboardsBot.keyboard_sort()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.sort
            )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВведите количество детей в положительном числовом выражении:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.children_count
        )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.children_age)
def state_custom_children_age(message) -> None:
    """
    Функция состояния диалога с ботом по команде high
    Записывает возраст детей

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text.isdigit() and int(message.text) in range(1, 19):
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if "children_age" not in data["custom_state"]:
                data["custom_state"]["children_age"] = [[int(message.text)]]
            elif len(data["custom_state"]["children_age"]) == VariablesMutableBot.count_room_flag:
                data["custom_state"]["children_age"][VariablesMutableBot.count_room_flag - 1].append(int(message.text))
            else:
                data["custom_state"]["children_age"].append([int(message.text)])
        if not VariablesMutableBot.count_children == VariablesMutableBot.count_children_flag:
            VariablesMutableBot.count_children_flag += 1
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Возраст {VariablesMutableBot.count_children_flag}-ого ребенка:",
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.children_age
            )
        elif not VariablesMutableBot.count_room == VariablesMutableBot.count_room_flag:
            VariablesMutableBot.count_children = 0
            VariablesMutableBot.count_children_flag = 0
            VariablesMutableBot.count_room_flag += 1
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Количество взрослых в {VariablesMutableBot.count_room_flag}-ом номере:",
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.adults_count
            )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.chat.id,
                text="По какой категории отсортировать показатели:",
                reply_markup=KeyboardsBot.keyboard_sort()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.sort
            )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\n"
                 "Введите возраст ребёнка в положительном числовом выражении\n"
                 "Так же возраст ребенка должен быть в диапазоне от 1 до 18 лет:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.children_age
        )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.sort)
def state_custom_sort(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Производит запись выбранной сортировки

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text in VariablesConstantsBot.DICT_SORT_API_HOSTEL:
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["custom_state"]["sort"] = VariablesConstantsBot.DICT_SORT_API_HOSTEL[message.text]
        if message.text == "Сортировка по ценам":
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой диапазон цен от 0 USD до 15000 USD\n\n"
                     "Минимальный диапазон:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.range_price
            )
        elif message.text == "Сортировка по оценкам проживающих":
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой диапазон рейтинга от 0 до 10\n\n"
                     "Минимальный диапазон:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.range_review
            )
        elif message.text == "Сортировка по расстоянию до центра":
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой диапазон расстояния от 0 до 15 км\n\n"
                     "Минимальный диапазон:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.range_distance
            )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой диапазон звезд от 0 до 5\n\n"
                     "Минимальный диапазон:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.range_star
            )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВыберите один из вариантов ниже:",
            reply_markup=KeyboardsBot.keyboard_sort()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.sort
        )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.range_price)
def state_custom_range_price(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с диапазоном цены

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    else:
        if message.text.replace('.', '', 1).isdigit() and 0 <= float(message.text) <= 15000:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if "range_min" in data["custom_state"]:
                    if float(message.text) < data["custom_state"]["range_min"]:
                        VariablesConstantsBot.BOT.send_message(
                            chat_id=message.from_user.id,
                            text="Неверный ввод.\nМаксимальная цена должна быть выше или равной минимальной."
                        )
                        VariablesConstantsBot.BOT.set_state(
                            user_id=message.from_user.id,
                            state=CustomState.range_price
                        )
                    else:
                        data["custom_state"]["range_max"] = round(float(message.text), 2)
                        VariablesConstantsBot.BOT.send_message(
                            chat_id=message.chat.id,
                            text="Количество не больше 20, которое необходимо вывести:"
                        )
                        VariablesConstantsBot.BOT.set_state(
                            user_id=message.from_user.id,
                            state=CustomState.count
                        )
                else:
                    data["custom_state"]["range_min"] = round(float(message.text), 2)
                    VariablesMutableBot.count_range = data["custom_state"]["range_min"]
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.from_user.id,
                        text="Максимальный диапазон:"
                    )
                    VariablesConstantsBot.BOT.set_state(
                        user_id=message.from_user.id,
                        state=CustomState.range_price
                    )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Неверный ввод.\n"
                     f"Введите цену  в  числовом выражении  от  {VariablesMutableBot.count_range} USD до 15000 USD."
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.range_price
            )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.range_review)
def state_custom_range_review(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с диапазоном рейтинга

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    else:
        if message.text.replace('.', '', 1).isdigit() and 0 <= float(message.text) <= 10:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if "range_min" in data["custom_state"]:
                    if float(message.text) < data["custom_state"]["range_min"]:
                        VariablesConstantsBot.BOT.send_message(
                            chat_id=message.from_user.id,
                            text="Неверный ввод.\nМаксимальный рейтинг должна быть выше или равный минимального."
                        )
                        VariablesConstantsBot.BOT.set_state(
                            user_id=message.from_user.id,
                            state=CustomState.range_review
                        )
                    else:
                        data["custom_state"]["range_max"] = round(float(message.text), 1)
                        VariablesConstantsBot.BOT.send_message(
                            chat_id=message.chat.id,
                            text="Количество не больше 20, которое необходимо вывести:"
                        )
                        VariablesConstantsBot.BOT.set_state(
                            user_id=message.from_user.id,
                            state=CustomState.count
                        )
                else:
                    data["custom_state"]["range_min"] = round(float(message.text), 1)
                    VariablesMutableBot.count_range = data["custom_state"]["range_min"]
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.from_user.id,
                        text="Максимальный диапазон:"
                    )
                    VariablesConstantsBot.BOT.set_state(
                        user_id=message.from_user.id,
                        state=CustomState.range_review
                    )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Неверный ввод.\n"
                     f"Введите рейтинг  в  числовом выражении  от  {VariablesMutableBot.count_range} до 10."
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.range_review
            )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.range_distance)
def state_custom_range_distance(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с диапазоном дистанции до центра города

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    else:
        if message.text.replace('.', '', 1).isdigit() and 0 <= float(message.text) <= 15:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if "range_min" in data["custom_state"]:
                    if float(message.text) < data["custom_state"]["range_min"]:
                        VariablesConstantsBot.BOT.send_message(
                            chat_id=message.from_user.id,
                            text="Неверный ввод.\nМаксимальная дистанция должна быть больше или равной минимальной."
                        )
                        VariablesConstantsBot.BOT.set_state(
                            user_id=message.from_user.id,
                            state=CustomState.range_distance
                        )
                    else:
                        data["custom_state"]["range_max"] = round(float(message.text), 2)
                        VariablesConstantsBot.BOT.send_message(
                            chat_id=message.chat.id,
                            text="Количество не больше 20, которое необходимо вывести:"
                        )
                        VariablesConstantsBot.BOT.set_state(
                            user_id=message.from_user.id,
                            state=CustomState.count
                        )
                else:
                    data["custom_state"]["range_min"] = round(float(message.text), 2)
                    VariablesMutableBot.count_range = data["custom_state"]["range_min"]
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.from_user.id,
                        text="Максимальный диапазон:"
                    )
                    VariablesConstantsBot.BOT.set_state(
                        user_id=message.from_user.id,
                        state=CustomState.range_distance
                    )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Неверный ввод.\n"
                     f"Введите дистанцию  в  числовом выражении  от  {VariablesMutableBot.count_range} до 15 км."
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.range_distance
            )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.range_star)
def state_custom_range_star(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с диапазоном звездности отеля

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    else:
        if message.text.replace('.', '', 1).isdigit() and 0 <= int(message.text) <= 5:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if "range_min" in data["custom_state"]:
                    if int(message.text) < data["custom_state"]["range_min"]:
                        VariablesConstantsBot.BOT.send_message(
                            chat_id=message.from_user.id,
                            text="Неверный ввод.\nМаксимальная звезда должна быть больше равной минимальной."
                        )
                        VariablesConstantsBot.BOT.set_state(
                            user_id=message.from_user.id,
                            state=CustomState.range_star
                        )
                    else:
                        data["custom_state"]["range_max"] = int(message.text)
                        VariablesConstantsBot.BOT.send_message(
                            chat_id=message.chat.id,
                            text="Количество не больше 20, которое необходимо вывести:"
                        )
                        VariablesConstantsBot.BOT.set_state(
                            user_id=message.from_user.id,
                            state=CustomState.count
                        )
                else:
                    data["custom_state"]["range_min"] = int(message.text)
                    VariablesMutableBot.count_range = data["custom_state"]["range_min"]
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.from_user.id,
                        text="Максимальный диапазон:"
                    )
                    VariablesConstantsBot.BOT.set_state(
                        user_id=message.from_user.id,
                        state=CustomState.range_star
                    )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Неверный ввод.\n"
                     f"Введите звезду  в  числовом выражении  от  {VariablesMutableBot.count_range} до 5."
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.range_star
            )


@VariablesConstantsBot.BOT.message_handler(state=CustomState.count)
def state_custom_count(message) -> None:
    """
    Функция завершения состояния диалога с ботом по команде custom
    Выводит пользователю результаты по его запросу

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
        data["custom_state"]["count"] = message.text
    create_request_db(
        message=message,
        dict_result=data["custom_state"],
        command=list(data.keys())[0]
    )
    if message.text.isdigit() and int(message.text) in range(1, 21):
        hotels_api = CustomApi.custom_result(dict_result=data['custom_state'])
        if len(hotels_api) == 0:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.chat.id,
                text="По вашему запросу нет подходящих отелей."
            )
        else:
            for numb_count in range(len(hotels_api)):
                text = (
                    f"{hotels_api[numb_count]['name_hotels']}\n"
                    f"{hotels_api[numb_count]['sort_element']}\n"
                    f"{hotels_api[numb_count]['url']}"
                )
                if hotels_api[numb_count]["number_photo"] > 0:
                    photo_list = [
                        telebot.types.InputMediaPhoto(media=hotels_api[numb_count][f"photo_{i}"], caption=text)
                        if i == 0
                        else telebot.types.InputMediaPhoto(media=hotels_api[numb_count][f"photo_{i}"])
                        for i in range(hotels_api[numb_count]["number_photo"])
                    ]
                else:
                    no_photo = open("../python_basic_diploma/config_data/no_photo.jpg", "rb")
                    photo_list = [telebot.types.InputMediaPhoto(media=no_photo, caption=text)]
                VariablesConstantsBot.BOT.send_media_group(
                    chat_id=message.chat.id,
                    media=photo_list
                )
        create_response_db(
            list_result=hotels_api
        )
        VariablesConstantsBot.BOT.delete_state(
            user_id=message.from_user.id,
            chat_id=message.chat.id
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Неверный ввод.\n"
                 "Я хочу получить положительное число от 1 до 20:"
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.count
        )


VariablesConstantsBot.BOT.add_custom_filter(telebot.custom_filters.StateFilter(VariablesConstantsBot.BOT))
