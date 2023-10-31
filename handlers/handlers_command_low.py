import telebot
from telebot.types import ReplyKeyboardRemove

from config_data import Functions, VariablesConstants, VariablesMutable
from keyboards import keyboard_year, keyboard_month, keyboard_day, keyboard_sort
from states import LowState


@VariablesConstants.BOT.message_handler(state="*", commands=["low"])
def state_low_start(message: object) -> None:
    """
    Function description:
    Функция начального состояния диалога с ботом по команде low
    Обновляет все атрибуты класса VariablesMutable

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    VariablesMutable.reset_parameters()
    VariablesConstants.BOT.send_message(
        chat_id=message.chat.id,
        text="По какому городу будем производить сортировку по отображению худших результатов:",
        reply_markup=ReplyKeyboardRemove()
    )
    VariablesConstants.BOT.set_state(
        user_id=message.from_user.id,
        state=LowState.city
    )
    with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
        data["low_state"] = {}

@VariablesConstants.BOT.message_handler(state=LowState.city)
def state_high_city(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде low
    Производит запись города для поиска и сортировки поиска

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.chat.id,
            text="Определитесь с датой заезда в отель.\nЗаезд. Выберите год:",
            reply_markup=keyboard_year()
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.arrival_year
        )
        with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["low_state"]["city"] = message.text

@VariablesConstants.BOT.message_handler(state=LowState.arrival_year)
def state_low_arrival_year(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде low
    Производит запись года заселения в номер

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
    elif message.text in VariablesMutable.list_year:
        with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["low_state"]["arrival_year"] = int(message.text)
        VariablesConstants.BOT.send_message(
            chat_id=message.chat.id,
            text="Заезд. Выберите месяц:",
            reply_markup=keyboard_month()
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.arrival_month
        )
        return
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.chat.id,
            text="Неверный ввод.\nЗаезд. Выберите год предложенный ниже:",
            reply_markup=keyboard_year()
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.arrival_year
        )

@VariablesConstants.BOT.message_handler(state=LowState.arrival_month)
def state_low_arrival_month(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде low
    Производит запись месяца заселения в номер

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
    else:
        with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if message.text.capitalize() in VariablesMutable.list_month:
                data["low_state"]["arrival_month"] = VariablesConstants.DICT_MOUNT_STR_INT[message.text.capitalize()]
                VariablesConstants.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Заезд. Выберите день:",
                    reply_markup=keyboard_day(
                        year=int(data["low_state"]["arrival_year"]),  # готово
                        month=int(data["low_state"]["arrival_month"])  # готово
                    )
                )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=LowState.arrival_day
                )
            else:
                VariablesConstants.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод.\nЗаезд. Выберите месяц предложенный ниже:",
                    reply_markup=keyboard_month()
                )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=LowState.arrival_month
                )

@VariablesConstants.BOT.message_handler(state=LowState.arrival_day)
def state_low_arrival_day(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде low
    Производит запись дня заселения в номер

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
    else:
        with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if message.text in VariablesMutable.list_days:
                data["low_state"]["arrival_day"] = int(message.text)
                VariablesConstants.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Определитесь с датой выезда из отель.\nВыезд. Выберите год:",
                    reply_markup=keyboard_year(start_year=int(data["low_state"]["arrival_year"]))  # готово
                )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=LowState.departure_year
                )
            else:
                VariablesConstants.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод.\nЗаезд. Выберите день предложенный ниже:",
                    reply_markup=keyboard_day(
                        year=int(data["low_state"]["arrival_year"]),  # готово
                        month=int(data["low_state"]["arrival_month"])  # готово
                    )
                )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=LowState.arrival_day
                )

@VariablesConstants.BOT.message_handler(state=LowState.departure_year)
def state_low_departure_year(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде low
    Производит запись года выезда из номера

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
    else:
        with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if message.text in VariablesMutable.list_year:
                data["low_state"]["departure_year"] = int(message.text)
                if not data["low_state"]["arrival_year"] == data["low_state"]["departure_year"]:
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Выезд. Выберите месяц:",
                        reply_markup=keyboard_month()
                    )
                else:
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Выезд. Выберите месяц:",
                        reply_markup=keyboard_month(start_month=int(data["low_state"]["arrival_month"]))  # готово
                    )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=LowState.departure_month
                )
            else:
                VariablesConstants.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод.\nВыезд. Выберите год предложенный ниже:",
                    reply_markup=keyboard_year(start_year=int(data["high_state"]["arrival_year"]))  # готово
                )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=LowState.departure_year
                )

@VariablesConstants.BOT.message_handler(state=LowState.departure_month)
def state_low_departure_month(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде low
    Производит запись месяца выезда из номера

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
    else:
        with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if message.text.capitalize() in VariablesMutable.list_month:
                data["low_state"]["departure_month"] = VariablesConstants.DICT_MOUNT_STR_INT[message.text.capitalize()]
                if (int(data["low_state"]["arrival_year"]) == int(data["low_state"]["departure_year"]) and
                    int(data["low_state"]["arrival_month"]) == int(data["low_state"]["departure_month"])):
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Выезд. Выберите день:",
                        reply_markup=keyboard_day(
                            year=int(data["low_state"]["departure_year"]),  # готово
                            month=int(data["low_state"]["departure_month"]),  # готово
                            start_day=int(data["low_state"]["arrival_day"])  # готово
                        )
                    )
                else:
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Выезд. Выберите день:",
                        reply_markup=keyboard_day(
                            year=int(data["low_state"]["arrival_year"]),  # готово
                            month=int(data["low_state"]["arrival_month"])  # готово
                        )
                    )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=LowState.departure_day
                )
            else:
                if not data["low_state"]["arrival_year"] == data["low_state"]["departure_year"]:
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Неверный ввод.\nВыезд. Выберите месяц предложенный ниже:",
                        reply_markup=keyboard_month()
                    )
                else:
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Неверный ввод.\nВыезд. Выберите месяц предложенный ниже:",
                        reply_markup=keyboard_month(start_month=int(data["low_state"]["arrival_month"]))  # готово
                    )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=LowState.departure_month
                )

@VariablesConstants.BOT.message_handler(state=LowState.departure_day)
def state_low_departure_day(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде low
    Производит запись дня выезда из номера

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
    else:
        with (VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data):
            if message.text in VariablesMutable.list_days:
                data["low_state"]["departure_day"] = int(message.text)
                VariablesConstants.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Количество номеров:",
                    reply_markup=ReplyKeyboardRemove()
                )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=LowState.room_count
                )
            else:
                if (int(data["low_state"]["arrival_year"]) == int(data["low_state"]["departure_year"]) and
                    int(data["low_state"]["arrival_month"]) == int(data["low_state"]["departure_month"])):
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Неверный ввод.\nВыезд. Выберите день предложенный ниже:",
                        reply_markup=keyboard_day(
                            year=int(data["low_state"]["departure_year"]),  # готово
                            month=int(data["low_state"]["departure_month"]),  # готово
                            start_day=int(data["low_state"]["arrival_day"])  # готово
                        )
                    )
                else:
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Неверный ввод.\nВыезд. Выберите день предложенный ниже:",
                        reply_markup=keyboard_day(
                            year=int(data["low_state"]["arrival_year"]),  # готово
                            month=int(data["low_state"]["arrival_month"])  # готово
                        )
                    )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=LowState.departure_day
                )

@VariablesConstants.BOT.message_handler(state=LowState.room_count)
def state_low_room_count(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде low
    Запоминает количество арендуемых номеров

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
    elif message.text.isdigit() and int(message.text) >= 1:
        VariablesMutable.count_room = int(message.text)
        VariablesMutable.count_room_flag += 1
        VariablesConstants.BOT.send_message(
            chat_id=message.from_user.id,
            text=f"Количество взрослых в {VariablesMutable.count_room_flag}-ом номере:",
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.adults_count
        )
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВведите количество номеров в положительном числовом выражении:",
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.room_count
        )

@VariablesConstants.BOT.message_handler(state=LowState.adults_count)
def state_low_adults_count(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде low
    Производит запись о количестве проживающих в номере

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
    elif message.text.isdigit() and int(message.text) >= 1:
        with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if not "adults" in data["low_state"]:
                data["low_state"]["adults"] = [int(message.text)]
            else:
                data["low_state"]["adults"].append(int(message.text))
        VariablesConstants.BOT.send_message(
            chat_id=message.from_user.id,
            text=f"Количество детей в {VariablesMutable.count_room_flag}-ом номере:",
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.children_count
        )
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВведите количество взрослых в положительном числовом выражении:",
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.adults_count
        )

@VariablesConstants.BOT.message_handler(state=LowState.children_count)
def state_low_children_count(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде low
    Запоминает количество детей и производит запись о детях если понадобится

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
    elif message.text.isdigit() and int(message.text) >= 0:
        VariablesMutable.count_children = int(message.text)
        if not VariablesMutable.count_children == 0:
            VariablesMutable.count_children_flag += 1
            VariablesConstants.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Возраст {VariablesMutable.count_children_flag}-ого ребенка:",
            )
            VariablesConstants.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.children_age
            )
        elif not VariablesMutable.count_room == VariablesMutable.count_room_flag:
            with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if not "children_age" in data["low_state"]:
                    data["low_state"]["children_age"] = [[]]
                else:
                    data["low_state"]["children_age"].append([])
            VariablesMutable.count_room_flag += 1
            VariablesConstants.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Количество взрослых в {VariablesMutable.count_room_flag}-ом номере:",
            )
            VariablesConstants.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.adults_count
            )
        else:
            with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
                data["low_state"]["children_age"].append([])
            VariablesConstants.BOT.send_message(
                chat_id=message.chat.id,
                text="По какой категории отсортировать лучшие показатели:",
                reply_markup=keyboard_sort())
            VariablesConstants.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.sort
            )
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВведите количество детей в положительном числовом выражении:",
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.children_count
        )

@VariablesConstants.BOT.message_handler(state=LowState.children_age)
def state_low_children_age(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде low
    Записывает возраст детей

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
    elif message.text.isdigit() and  0 < int(message.text) < 18:
        with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if not "children_age" in data["low_state"]:
                data["low_state"]["children_age"] = [[int(message.text)]]
            elif len(data["low_state"]["children_age"]) == VariablesMutable.count_room_flag:
                data["low_state"]["children_age"][VariablesMutable.count_room_flag - 1].append(int(message.text))
            else:
                data["low_state"]["children_age"].append([int(message.text)])
        if not VariablesMutable.count_children == VariablesMutable.count_children_flag:
            VariablesMutable.count_children_flag += 1
            VariablesConstants.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Возраст {VariablesMutable.count_children_flag}-ого ребенка:",
            )
            VariablesConstants.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.children_age
            )
        elif not VariablesMutable.count_room == VariablesMutable.count_room_flag:
            VariablesMutable.count_children = 0
            VariablesMutable.count_children_flag = 0
            VariablesMutable.count_room_flag += 1
            VariablesConstants.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Количество взрослых в {VariablesMutable.count_room_flag}-ом номере:",
            )
            VariablesConstants.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.adults_count
            )
        else:
            VariablesConstants.BOT.send_message(
                chat_id=message.chat.id,
                text="По какой категории отсортировать лучшие показатели:",
                reply_markup=keyboard_sort())
            VariablesConstants.BOT.set_state(
                user_id=message.from_user.id,
                state=LowState.sort
            )
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\n"
                 "Введите возраст ребёнка в положительном числовом выражении\n"
                 "Так же возраст ребенка должен быть в диапазоне от 1 до 18 лет:",
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.children_age
        )

@VariablesConstants.BOT.message_handler(state=LowState.sort)
def state_low_sort(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде low
    Производит запись выбранной сортировки

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
    elif message.text in VariablesConstants.DICT_SORT_API_HOSTEL:
        VariablesConstants.BOT.send_message(
            chat_id=message.chat.id,
            text="Количество которое необходимо вывести:",
            reply_markup=ReplyKeyboardRemove()
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.count
        )
        with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["low_state"]["sort"] = VariablesConstants.DICT_SORT_API_HOSTEL[message.text]
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.chat.id,
            text="Неверный ввод.\nВыберите один из вариантов предложенных ниже:",
            reply_markup=keyboard_sort()
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.sort
        )

@VariablesConstants.BOT.message_handler(state=LowState.count)
def state_low_count(message: object) -> None:
    """
    Function description:
    Функция завершения состояния диалога с ботом по команде low
    Производит запись количества выводимых результатов

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
    elif message.text.isdigit():
        with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["low_state"]["count"] = message.text
        VariablesConstants.BOT.send_message(
            chat_id=message.chat.id,
            text=f"{data}"
        )
        VariablesConstants.BOT.delete_state(
            user_id=message.from_user.id
        )
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.chat.id,
            text="Неверный ввод.\nЯ хочу получить положительное число:"
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=LowState.count
        )

VariablesConstants.BOT.add_custom_filter(telebot.custom_filters.StateFilter(VariablesConstants.BOT))
