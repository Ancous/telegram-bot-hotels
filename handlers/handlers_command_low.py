"""
Модуль поддержания состояния диалога с пользователем по команде low
"""

import telebot

from datetime import datetime
from telebot.types import ReplyKeyboardRemove

from states import LowState
from keyboards import KeyboardsBot
from database import create_request_db, create_response_db
from hotels_api import checking_city_country_recording_city_id, LowApi
from config_data import FunctionsBot, VariablesConstantsBot, VariablesMutableBot


@VariablesConstantsBot.BOT.message_handler(state="*", commands=["low"])
def state_low_start(message: telebot.types.Message) -> None:
    """
    Функция начального состояния диалога с ботом по команде low
    Обновляет все атрибуты класса VariablesMutable

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    VariablesMutableBot.reset_parameters()
    VariablesConstantsBot.BOT.send_message(
        chat_id=message.chat.id,
        text="По какой стране будем производить сортировку по отображению худших результатов:",
        reply_markup=ReplyKeyboardRemove()
    )
    VariablesConstantsBot.BOT.set_state(
        user_id=message.from_user.id,
        state=LowState.country
    )
    with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
        data.clear()
        data["low_state"] = {}


@VariablesConstantsBot.BOT.message_handler(state=LowState.country)
def state_high_country(message: telebot.types.Message) -> None:
    """
    Функция состояния диалога с ботом по команде low
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
        data["low_state"]["country"] = message.text
    VariablesConstantsBot.BOT.send_message(
        chat_id=message.chat.id,
        text="По какому городу:"
    )
    VariablesConstantsBot.BOT.set_state(
        user_id=message.from_user.id,
        state=LowState.city
    )


@VariablesConstantsBot.BOT.message_handler(state=LowState.city)
def state_high_city(message: telebot.types.Message) -> None:
    """
    Функция состояния диалога с ботом по команде low
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
        data["low_state"]["city"] = message.text
    city_id = checking_city_country_recording_city_id(
        dict_result=data["low_state"]
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
            state=LowState.country
        )
    else:
        data["low_state"]["city_id"] = city_id
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Определитесь с датой заезда в отель.\n"
                 "Заезд. Выберите год:",
            reply_markup=KeyboardsBot.keyboard_year()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.arrival_year
        )


@VariablesConstantsBot.BOT.message_handler(state=LowState.arrival_year)
def state_low_arrival_year(message: telebot.types.Message) -> None:
    """
    Функция состояния диалога с ботом по команде low
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
            data["low_state"]["arrival_year"] = int(message.text)
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Заезд. Выберите месяц:",
            reply_markup=KeyboardsBot.keyboard_month()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.arrival_month
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Неверный ввод.\n"
                 "Заезд. Выберите год предложенный ниже:",
            reply_markup=KeyboardsBot.keyboard_year()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.arrival_year
        )


@VariablesConstantsBot.BOT.message_handler(state=LowState.arrival_month)
def state_low_arrival_month(message: telebot.types.Message) -> None:
    """
    Функция состояния диалога с ботом по команде low
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
            data["low_state"]["arrival_month"] = VariablesConstantsBot.DICT_MOUNT_STR_INT[message.text.capitalize()]
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Заезд. Выберите день:",
            reply_markup=KeyboardsBot.keyboard_day(
                year=int(data["low_state"]["arrival_year"]),
                month=int(data["low_state"]["arrival_month"])
            )
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.arrival_day
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Неверный ввод.\n"
                 "Заезд. Выберите месяц предложенный ниже:",
            reply_markup=KeyboardsBot.keyboard_month()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.arrival_month
        )


@VariablesConstantsBot.BOT.message_handler(state=LowState.arrival_day)
def state_low_arrival_day(message: telebot.types.Message) -> None:
    """
    Функция состояния диалога с ботом по команде low
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
            data["low_state"]["arrival_day"] = int(message.text)
            VariablesMutableBot.year = False
            VariablesMutableBot.month = False
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.chat.id,
                text="Определитесь с датой выезда из отель.\n"
                     "Выезд. Выберите год:",
                reply_markup=KeyboardsBot.keyboard_year(start_year=int(data["low_state"]["arrival_year"]))
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.departure_year
            )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.chat.id,
                text="Неверный ввод.\n"
                     "Заезд. Выберите день предложенный ниже:",
                reply_markup=KeyboardsBot.keyboard_day(
                    year=int(data["low_state"]["arrival_year"]),
                    month=int(data["low_state"]["arrival_month"])
                )
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.arrival_day
            )


@VariablesConstantsBot.BOT.message_handler(state=LowState.departure_year)
def state_low_departure_year(message: telebot.types.Message) -> None:
    """
    Функция состояния диалога с ботом по команде low
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
            data["low_state"]["departure_year"] = int(message.text)
            if data["low_state"]["arrival_year"] == data["low_state"]["departure_year"]:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Выезд. Выберите месяц:",
                    reply_markup=KeyboardsBot.keyboard_month(start_month=int(data["low_state"]["arrival_month"]))
                )
            else:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Выезд. Выберите месяц:",
                    reply_markup=KeyboardsBot.keyboard_month()
                )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.departure_month
            )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.chat.id,
                text="Неверный ввод.\n"
                     "Выезд. Выберите год предложенный ниже:",
                reply_markup=KeyboardsBot.keyboard_year(start_year=int(data["low_state"]["arrival_year"]))
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.departure_year
            )


@VariablesConstantsBot.BOT.message_handler(state=LowState.departure_month)
def state_low_departure_month(message: telebot.types.Message) -> None:
    """
    Функция состояния диалога с ботом по команде low
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
            data["low_state"]["departure_month"] = VariablesConstantsBot.DICT_MOUNT_STR_INT[message.text.capitalize()]
            if (int(data["low_state"]["arrival_year"]) == int(data["low_state"]["departure_year"]) and
                    int(data["low_state"]["arrival_month"]) == int(data["low_state"]["departure_month"])):
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Выезд. Выберите день:",
                    reply_markup=KeyboardsBot.keyboard_day(
                        year=int(data["low_state"]["departure_year"]),
                        month=int(data["low_state"]["departure_month"]),
                        start_day=int(data["low_state"]["arrival_day"])
                    )
                )
            else:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Выезд. Выберите день:",
                    reply_markup=KeyboardsBot.keyboard_day(
                        year=int(data["low_state"]["arrival_year"]),
                        month=int(data["low_state"]["arrival_month"])
                    )
                )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.departure_day
            )
        else:
            if data["low_state"]["arrival_year"] == data["low_state"]["departure_year"]:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод.\n"
                         "Выезд. Выберите месяц предложенный ниже:",
                    reply_markup=KeyboardsBot.keyboard_month(start_month=int(data["low_state"]["arrival_month"]))
                )
            else:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод.\n"
                         "Выезд. Выберите месяц предложенный ниже:",
                    reply_markup=KeyboardsBot.keyboard_month()
                )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.departure_month
            )


@VariablesConstantsBot.BOT.message_handler(state=LowState.departure_day)
def state_low_departure_day(message: telebot.types.Message) -> None:
    """
    Функция состояния диалога с ботом по команде low
    Производит запись дня выезда из номера

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    with (VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data):
        if message.text in VariablesMutableBot.list_days:
            data["low_state"]["departure_day"] = int(message.text)
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.room_count
            )
        else:
            if (int(data["low_state"]["arrival_year"]) == int(data["low_state"]["departure_year"]) and
                    int(data["low_state"]["arrival_month"]) == int(data["low_state"]["departure_month"])):
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод.\n"
                         "Выезд. Выберите день предложенный ниже:",
                    reply_markup=KeyboardsBot.keyboard_day(
                        year=int(data["low_state"]["departure_year"]),
                        month=int(data["low_state"]["departure_month"]),
                        start_day=int(data["low_state"]["arrival_day"])
                    )
                )
            else:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод.\n"
                         "Выезд. Выберите день предложенный ниже:",
                    reply_markup=KeyboardsBot.keyboard_day(
                        year=int(data["low_state"]["arrival_year"]),
                        month=int(data["low_state"]["arrival_month"])
                    )
                )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.departure_day
            )


@VariablesConstantsBot.BOT.message_handler(state=LowState.room_count)
def state_low_room_count(message: telebot.types.Message) -> None:
    """
    Функция состояния диалога с ботом по команде low
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
            state=LowState.adults_count
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\n"
                 "Введите количество номеров в положительном числовом выражении:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.room_count
        )


@VariablesConstantsBot.BOT.message_handler(state=LowState.adults_count)
def state_low_adults_count(message: telebot.types.Message) -> None:
    """
    Функция состояния диалога с ботом по команде low
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
            if "adults" in data["low_state"]:
                data["low_state"]["adults"].append(int(message.text))
            else:
                data["low_state"]["adults"] = [int(message.text)]
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text=f"Количество детей в {VariablesMutableBot.count_room_flag}-ом номере:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.children_count
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\n"
                 "Введите количество взрослых в положительном числовом выражении:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.adults_count
        )


@VariablesConstantsBot.BOT.message_handler(state=LowState.children_count)
def state_low_children_count(message: telebot.types.Message) -> None:
    """
    Функция состояния диалога с ботом по команде low
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
                state=LowState.children_age
            )
        elif not VariablesMutableBot.count_room == VariablesMutableBot.count_room_flag:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if "children_age" in data["low_state"]:
                    data["low_state"]["children_age"].append([])
                else:
                    data["low_state"]["children_age"] = [[]]
            VariablesMutableBot.count_room_flag += 1
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Количество взрослых в {VariablesMutableBot.count_room_flag}-ом номере:",
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.adults_count
            )
        else:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if "children_age" in data["low_state"]:
                    data["low_state"]["children_age"].append([])
                else:
                    data["low_state"]["children_age"] = [[]]
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.chat.id,
                text="По какой категории отсортировать худшие показатели:",
                reply_markup=KeyboardsBot.keyboard_sort()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.sort
            )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\n"
                 "Введите количество детей в положительном числовом выражении:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.children_count
        )


@VariablesConstantsBot.BOT.message_handler(state=LowState.children_age)
def state_low_children_age(message: telebot.types.Message) -> None:
    """
    Функция состояния диалога с ботом по команде low
    Записывает возраст детей

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text.isdigit() and int(message.text) in range(1, 18):
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if "children_age" not in data["low_state"]:
                data["low_state"]["children_age"] = [[int(message.text)]]
            elif len(data["low_state"]["children_age"]) == VariablesMutableBot.count_room_flag:
                data["low_state"]["children_age"][VariablesMutableBot.count_room_flag - 1].append(int(message.text))
            else:
                data["low_state"]["children_age"].append([int(message.text)])
        if not VariablesMutableBot.count_children == VariablesMutableBot.count_children_flag:
            VariablesMutableBot.count_children_flag += 1
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Возраст {VariablesMutableBot.count_children_flag}-ого ребенка:",
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.children_age
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
                state=LowState.adults_count
            )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.chat.id,
                text="По какой категории отсортировать худшие показатели:",
                reply_markup=KeyboardsBot.keyboard_sort()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.sort
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
            state=LowState.children_age
        )


@VariablesConstantsBot.BOT.message_handler(state=LowState.sort)
def state_low_sort(message: telebot.types.Message) -> None:
    """
    Функция состояния диалога с ботом по команде low
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
            data["low_state"]["sort"] = VariablesConstantsBot.DICT_SORT_API_HOSTEL[message.text]
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Количество не больше 20, которое необходимо вывести:",
            reply_markup=ReplyKeyboardRemove()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.count
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Неверный ввод.\n"
                 "Выберите один из вариантов предложенных ниже:",
            reply_markup=KeyboardsBot.keyboard_sort()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.sort
        )


@VariablesConstantsBot.BOT.message_handler(state=LowState.count)
def state_low_count(message: telebot.types.Message) -> None:
    """
    Функция завершения состояния диалога с ботом по команде low
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
        data["low_state"]["count"] = message.text
    if message.text.isdigit() and int(message.text) in range(1, 21):
        create_request_db(
            message=message,
            dict_result=data["low_state"],
            command=list(data.keys())[0]
        )
        hotels_api = LowApi.low_result(dict_result=data['low_state'])
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
            state=LowState.count
        )


VariablesConstantsBot.BOT.add_custom_filter(telebot.custom_filters.StateFilter(VariablesConstantsBot.BOT))
