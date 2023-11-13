import telebot
from telebot.types import ReplyKeyboardRemove
from datetime import datetime

from config_data import FunctionsBot, VariablesConstantsBot, VariablesMutableBot
from keyboards import KeyboardsBot
from states import HighState


@VariablesConstantsBot.BOT.message_handler(state="*", commands=["high"])
def state_high_start(message: object) -> None:
    """
    Функция начального состояния диалога с ботом по команде high
    Обновляет все атрибуты класса VariablesMutable

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    VariablesMutableBot.reset_parameters()
    VariablesConstantsBot.BOT.send_message(
        chat_id=message.chat.id,
        text="По какому городу будем производить сортировку по отображению лучших результатов:",
        reply_markup=ReplyKeyboardRemove()
    )
    VariablesConstantsBot.BOT.set_state(
        user_id=message.from_user.id,
        state=HighState.city
    )
    with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
        data["high_state"] = {}

@VariablesConstantsBot.BOT.message_handler(state=HighState.city)
def state_high_city(message: object) -> None:
    """
    Функция состояния диалога с ботом по команде high
    Производит запись города для поиска

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Определитесь с датой заезда в отель.\nЗаезд. Выберите год:",
            reply_markup=KeyboardsBot.keyboard_year()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.arrival_year
        )
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["high_state"]["city"] = message.text
#
@VariablesConstantsBot.BOT.message_handler(state=HighState.arrival_year)
def state_high_arrival_year(message: object) -> None:
    """
    Функция состояния диалога с ботом по команде high
    Производит запись года заселения в номер

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    elif message.text in VariablesMutableBot.list_year:
        if int(message.text) == datetime.now().year:
            VariablesMutableBot.year = True
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["high_state"]["arrival_year"] = int(message.text)
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Заезд. Выберите месяц:",
            reply_markup=KeyboardsBot.keyboard_month()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.arrival_month
        )
        return
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Неверный ввод.\nЗаезд. Выберите год предложенный ниже:",
            reply_markup=KeyboardsBot.keyboard_year()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.arrival_year
        )

@VariablesConstantsBot.BOT.message_handler(state=HighState.arrival_month)
def state_high_arrival_month(message: object) -> None:
    """
    Функция состояния диалога с ботом по команде high
    Производит запись месяца заселения в номер

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    else:
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if VariablesConstantsBot.DICT_MOUNT_STR_INT[message.text.capitalize()] == datetime.now().month:
                VariablesMutableBot.month = True
            if message.text.capitalize() in VariablesMutableBot.list_month:
                data["high_state"]["arrival_month"] = VariablesConstantsBot.DICT_MOUNT_STR_INT[message.text.capitalize()]
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Заезд. Выберите день:",
                    reply_markup=KeyboardsBot.keyboard_day(
                        year=int(data["high_state"]["arrival_year"]),
                        month=int(data["high_state"]["arrival_month"])
                    )
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.arrival_day
                )
            else:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод.\nЗаезд. Выберите месяц предложенный ниже:",
                    reply_markup=KeyboardsBot.keyboard_month()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.arrival_month
                )

@VariablesConstantsBot.BOT.message_handler(state=HighState.arrival_day)
def state_high_arrival_day(message: object) -> None:
    """
    Функция состояния диалога с ботом по команде high
    Производит запись дня заселения в номер

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    else:
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if message.text in VariablesMutableBot.list_days:
                data["high_state"]["arrival_day"] = int(message.text)
                VariablesMutableBot.year = False
                VariablesMutableBot.month = False
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Определитесь с датой выезда из отель.\nВыезд. Выберите год:",
                    reply_markup=KeyboardsBot.keyboard_year(start_year=int(data["high_state"]["arrival_year"]))
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.departure_year
                )
            else:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод.\nЗаезд. Выберите день предложенный ниже:",
                    reply_markup=KeyboardsBot.keyboard_day(
                        year=int(data["high_state"]["arrival_year"]),
                        month=int(data["high_state"]["arrival_month"])
                    )
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.arrival_day
                )

@VariablesConstantsBot.BOT.message_handler(state=HighState.departure_year)
def state_high_departure_year(message: object) -> None:
    """
    Функция состояния диалога с ботом по команде high
    Производит запись года выезда из номера

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    else:
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if message.text in VariablesMutableBot.list_year:
                data["high_state"]["departure_year"] = int(message.text)
                if not data["high_state"]["arrival_year"] == data["high_state"]["departure_year"]:
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Выезд. Выберите месяц:",
                        reply_markup=KeyboardsBot.keyboard_month()
                    )
                else:
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Выезд. Выберите месяц:",
                        reply_markup=KeyboardsBot.keyboard_month(start_month=int(data["high_state"]["arrival_month"]))
                    )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.departure_month
                )
            else:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод.\nВыезд. Выберите год предложенный ниже:",
                    reply_markup=KeyboardsBot.keyboard_year(start_year=int(data["high_state"]["arrival_year"]))
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.departure_year
                )

@VariablesConstantsBot.BOT.message_handler(state=HighState.departure_month)
def state_high_departure_month(message: object) -> None:
    """
    Функция состояния диалога с ботом по команде high
    Производит запись месяца выезда из номера

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    else:
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if message.text.capitalize() in VariablesMutableBot.list_month:
                data["high_state"]["departure_month"] = VariablesConstantsBot.DICT_MOUNT_STR_INT[message.text.capitalize()]
                if (int(data["high_state"]["arrival_year"]) == int(data["high_state"]["departure_year"]) and
                    int(data["high_state"]["arrival_month"]) == int(data["high_state"]["departure_month"])):
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Выезд. Выберите день:",
                        reply_markup=KeyboardsBot.keyboard_day(
                            year=int(data["high_state"]["departure_year"]),
                            month=int(data["high_state"]["departure_month"]),
                            start_day=int(data["high_state"]["arrival_day"])
                        )
                    )
                else:
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Выезд. Выберите день:",
                        reply_markup=KeyboardsBot.keyboard_day(
                            year=int(data["high_state"]["arrival_year"]),
                            month=int(data["high_state"]["arrival_month"])
                        )
                    )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.departure_day
                )
            else:
                if not data["high_state"]["arrival_year"] == data["high_state"]["departure_year"]:
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Неверный ввод.\nВыезд. Выберите месяц предложенный ниже:",
                        reply_markup=KeyboardsBot.keyboard_month()
                    )
                else:
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Неверный ввод.\nВыезд. Выберите месяц предложенный ниже:",
                        reply_markup=KeyboardsBot.keyboard_month(start_month=int(data["high_state"]["arrival_month"]))
                    )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.departure_month
                )

@VariablesConstantsBot.BOT.message_handler(state=HighState.departure_day)
def state_high_departure_day(message: object) -> None:
    """
    Функция состояния диалога с ботом по команде high
    Производит запись дня выезда из номера

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    else:
        with (VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data):
            if message.text in VariablesMutableBot.list_days:
                data["high_state"]["departure_day"] = int(message.text)
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Количество номеров:",
                    reply_markup=ReplyKeyboardRemove()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.room_count
                )
            else:
                if (int(data["high_state"]["arrival_year"]) == int(data["high_state"]["departure_year"]) and
                    int(data["high_state"]["arrival_month"]) == int(data["high_state"]["departure_month"])):
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Неверный ввод.\nВыезд. Выберите день предложенный ниже:",
                        reply_markup=KeyboardsBot.keyboard_day(
                            year=int(data["high_state"]["departure_year"]),
                            month=int(data["high_state"]["departure_month"]),
                            start_day=int(data["high_state"]["arrival_day"])
                        )
                    )
                else:
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Неверный ввод.\nВыезд. Выберите день предложенный ниже:",
                        reply_markup=KeyboardsBot.keyboard_day(
                            year=int(data["high_state"]["arrival_year"]),
                            month=int(data["high_state"]["arrival_month"])
                        )
                    )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.departure_day
                )

@VariablesConstantsBot.BOT.message_handler(state=HighState.room_count)
def state_high_room_count(message: object) -> None:
    """
    Функция состояния диалога с ботом по команде high
    Запоминает количество арендуемых номеров

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    elif message.text.isdigit() and int(message.text) >= 1:
        VariablesMutableBot.count_room = int(message.text)
        VariablesMutableBot.count_room_flag += 1
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text=f"Количество взрослых в {VariablesMutableBot.count_room_flag}-ом номере:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.adults_count
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВведите количество номеров в положительном числовом выражении:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.room_count
        )

@VariablesConstantsBot.BOT.message_handler(state=HighState.adults_count)
def state_high_adults_count(message: object) -> None:
    """
    Функция состояния диалога с ботом по команде high
    Производит запись о количестве проживающих в номере

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    elif message.text.isdigit() and int(message.text) >= 1:
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if not "adults" in data["high_state"]:
                data["high_state"]["adults"] = [int(message.text)]
            else:
                data["high_state"]["adults"].append(int(message.text))
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text=f"Количество детей в {VariablesMutableBot.count_room_flag}-ом номере:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.children_count
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВведите количество взрослых в положительном числовом выражении:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.adults_count
        )

@VariablesConstantsBot.BOT.message_handler(state=HighState.children_count)
def state_high_children_count(message: object) -> None:
    """
    Функция состояния диалога с ботом по команде high
    Запоминает количество детей и производит запись о детях если понадобится

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    elif message.text.isdigit() and int(message.text) >= 0:
        VariablesMutableBot.count_children = int(message.text)
        if not VariablesMutableBot.count_children == 0:
            VariablesMutableBot.count_children_flag += 1
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Возраст {VariablesMutableBot.count_children_flag}-ого ребенка:",
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=HighState.children_age
            )
        elif not VariablesMutableBot.count_room == VariablesMutableBot.count_room_flag:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if not "children_age" in data["high_state"]:
                    data["high_state"]["children_age"] = [[]]
                else:
                    data["high_state"]["children_age"].append([])
            VariablesMutableBot.count_room_flag += 1
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Количество взрослых в {VariablesMutableBot.count_room_flag}-ом номере:",
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=HighState.adults_count
            )
        else:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                data["high_state"]["children_age"].append([])
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.chat.id,
                text="По какой категории отсортировать лучшие показатели:",
                reply_markup=KeyboardsBot.keyboard_sort())
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=HighState.sort
            )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВведите количество детей в положительном числовом выражении:",
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.children_count
        )

@VariablesConstantsBot.BOT.message_handler(state=HighState.children_age)
def state_high_children_age(message: object) -> None:
    """
    Функция состояния диалога с ботом по команде high
    Записывает возраст детей

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    elif message.text.isdigit() and  0 < int(message.text) < 18:
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if not "children_age" in data["high_state"]:
                data["high_state"]["children_age"] = [[int(message.text)]]
            elif len(data["high_state"]["children_age"]) == VariablesMutableBot.count_room_flag:
                data["high_state"]["children_age"][VariablesMutableBot.count_room_flag - 1].append(int(message.text))
            else:
                data["high_state"]["children_age"].append([int(message.text)])
        if not VariablesMutableBot.count_children == VariablesMutableBot.count_children_flag:
            VariablesMutableBot.count_children_flag += 1
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Возраст {VariablesMutableBot.count_children_flag}-ого ребенка:",
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=HighState.children_age
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
                state=HighState.adults_count
            )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.chat.id,
                text="По какой категории отсортировать лучшие показатели:",
                reply_markup=KeyboardsBot.keyboard_sort())
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=HighState.sort
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
            state=HighState.children_age
        )

@VariablesConstantsBot.BOT.message_handler(state=HighState.sort)
def state_high_sort(message: object) -> None:
    """
    Функция состояния диалога с ботом по команде high
    Производит запись выбранной сортировки

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    elif message.text in VariablesConstantsBot.DICT_SORT_API_HOSTEL:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Количество которое необходимо вывести:",
            reply_markup=ReplyKeyboardRemove()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.count
        )
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["high_state"]["sort"] = VariablesConstantsBot.DICT_SORT_API_HOSTEL[message.text]
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Неверный ввод.\nВыберите один из вариантов предложенных ниже:",
            reply_markup=KeyboardsBot.keyboard_sort()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.sort
        )

@VariablesConstantsBot.BOT.message_handler(state=HighState.count)
def state_high_count(message: object) -> None:
    """
    Функция завершения состояния диалога с ботом по команде high
    Производит запись количества выводимых результатов

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    elif message.text.isdigit():
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["high_state"]["count"] = message.text
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text=f"{data['high_state']}"
        )
        VariablesConstantsBot.BOT.delete_state(
            user_id=message.from_user.id,
            chat_id=message.chat.id
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="Неверный ввод.\nЯ хочу получить положительное число:"
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.count
        )

VariablesConstantsBot.BOT.add_custom_filter(telebot.custom_filters.StateFilter(VariablesConstantsBot.BOT))
