import telebot
from telebot.types import ReplyKeyboardRemove

from config_data import Functions, VariablesConstants, VariablesMutable
from keyboards import Keyboards
from states import HighState


@VariablesConstants.BOT.message_handler(state="*", commands=["high"])
def state_high_start(message: object) -> None:
    """
    Function description:
    Функция начального состояния диалога с ботом по команде high
    Обновляет все атрибуты класса VariablesMutable

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    VariablesMutable.reset_parameters()
    VariablesConstants.BOT.send_message(
        chat_id=message.chat.id,
        text="По какому городу будем производить сортировку по отображению лучших результатов:",
        reply_markup=ReplyKeyboardRemove()
    )
    VariablesConstants.BOT.set_state(
        user_id=message.from_user.id,
        state=HighState.city
    )
    with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
        data["high_state"] = {}

@VariablesConstants.BOT.message_handler(state=HighState.city)
def state_high_city(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде high
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
            reply_markup=Keyboards.keyboard_year()
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.arrival_year
        )
        with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["high_state"]["city"] = message.text
#
@VariablesConstants.BOT.message_handler(state=HighState.arrival_year)
def state_high_arrival_year(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде high
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
            data["high_state"]["arrival_year"] = int(message.text)
        VariablesConstants.BOT.send_message(
            chat_id=message.chat.id,
            text="Заезд. Выберите месяц:",
            reply_markup=Keyboards.keyboard_month()
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.arrival_month
        )
        return
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.chat.id,
            text="Неверный ввод.\nЗаезд. Выберите год предложенный ниже:",
            reply_markup=Keyboards.keyboard_year()
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.arrival_year
        )

@VariablesConstants.BOT.message_handler(state=HighState.arrival_month)
def state_high_arrival_month(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде high
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
                data["high_state"]["arrival_month"] = VariablesConstants.DICT_MOUNT_STR_INT[message.text.capitalize()]
                VariablesConstants.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Заезд. Выберите день:",
                    reply_markup=Keyboards.keyboard_day(
                        year=int(data["high_state"]["arrival_year"]),
                        month=int(data["high_state"]["arrival_month"])
                    )
                )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.arrival_day
                )
            else:
                VariablesConstants.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод.\nЗаезд. Выберите месяц предложенный ниже:",
                    reply_markup=Keyboards.keyboard_month()
                )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.arrival_month
                )

@VariablesConstants.BOT.message_handler(state=HighState.arrival_day)
def state_high_arrival_day(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде high
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
                data["high_state"]["arrival_day"] = int(message.text)
                VariablesConstants.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Определитесь с датой выезда из отель.\nВыезд. Выберите год:",
                    reply_markup=Keyboards.keyboard_year(start_year=int(data["high_state"]["arrival_year"]))
                )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.departure_year
                )
            else:
                VariablesConstants.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод.\nЗаезд. Выберите день предложенный ниже:",
                    reply_markup=Keyboards.keyboard_day(
                        year=int(data["high_state"]["arrival_year"]),
                        month=int(data["high_state"]["arrival_month"])
                    )
                )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.arrival_day
                )

@VariablesConstants.BOT.message_handler(state=HighState.departure_year)
def state_high_departure_year(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде high
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
                data["high_state"]["departure_year"] = int(message.text)
                if not data["high_state"]["arrival_year"] == data["high_state"]["departure_year"]:
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Выезд. Выберите месяц:",
                        reply_markup=Keyboards.keyboard_month()
                    )
                else:
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Выезд. Выберите месяц:",
                        reply_markup=Keyboards.keyboard_month(start_month=int(data["high_state"]["arrival_month"]))
                    )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.departure_month
                )
            else:
                VariablesConstants.BOT.send_message(
                    chat_id=message.chat.id,
                    text="Неверный ввод.\nВыезд. Выберите год предложенный ниже:",
                    reply_markup=Keyboards.keyboard_year(start_year=int(data["high_state"]["arrival_year"]))
                )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.departure_year
                )

@VariablesConstants.BOT.message_handler(state=HighState.departure_month)
def state_high_departure_month(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде high
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
                data["high_state"]["departure_month"] = VariablesConstants.DICT_MOUNT_STR_INT[message.text.capitalize()]
                if (int(data["high_state"]["arrival_year"]) == int(data["high_state"]["departure_year"]) and
                    int(data["high_state"]["arrival_month"]) == int(data["high_state"]["departure_month"])):
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Выезд. Выберите день:",
                        reply_markup=Keyboards.keyboard_day(
                            year=int(data["high_state"]["departure_year"]),
                            month=int(data["high_state"]["departure_month"]),
                            start_day=int(data["high_state"]["arrival_day"])
                        )
                    )
                else:
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Выезд. Выберите день:",
                        reply_markup=Keyboards.keyboard_day(
                            year=int(data["high_state"]["arrival_year"]),
                            month=int(data["high_state"]["arrival_month"])
                        )
                    )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.departure_day
                )
            else:
                if not data["high_state"]["arrival_year"] == data["high_state"]["departure_year"]:
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Неверный ввод.\nВыезд. Выберите месяц предложенный ниже:",
                        reply_markup=Keyboards.keyboard_month()
                    )
                else:
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Неверный ввод.\nВыезд. Выберите месяц предложенный ниже:",
                        reply_markup=Keyboards.keyboard_month(start_month=int(data["high_state"]["arrival_month"]))
                    )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.departure_month
                )

@VariablesConstants.BOT.message_handler(state=HighState.departure_day)
def state_high_departure_day(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде high
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
                data["high_state"]["departure_day"] = int(message.text)
                VariablesConstants.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Количество номеров:",
                    reply_markup=ReplyKeyboardRemove()
                )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.room_count
                )
            else:
                if (int(data["high_state"]["arrival_year"]) == int(data["high_state"]["departure_year"]) and
                    int(data["high_state"]["arrival_month"]) == int(data["high_state"]["departure_month"])):
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Неверный ввод.\nВыезд. Выберите день предложенный ниже:",
                        reply_markup=Keyboards.keyboard_day(
                            year=int(data["high_state"]["departure_year"]),
                            month=int(data["high_state"]["departure_month"]),
                            start_day=int(data["high_state"]["arrival_day"])
                        )
                    )
                else:
                    VariablesConstants.BOT.send_message(
                        chat_id=message.chat.id,
                        text="Неверный ввод.\nВыезд. Выберите день предложенный ниже:",
                        reply_markup=Keyboards.keyboard_day(
                            year=int(data["high_state"]["arrival_year"]),
                            month=int(data["high_state"]["arrival_month"])
                        )
                    )
                VariablesConstants.BOT.set_state(
                    user_id=message.from_user.id,
                    state=HighState.departure_day
                )

@VariablesConstants.BOT.message_handler(state=HighState.room_count)
def state_high_room_count(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде high
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
            state=HighState.adults_count
        )
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВведите количество номеров в положительном числовом выражении:",
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.room_count
        )

@VariablesConstants.BOT.message_handler(state=HighState.adults_count)
def state_high_adults_count(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде high
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
            if not "adults" in data["high_state"]:
                data["high_state"]["adults"] = [int(message.text)]
            else:
                data["high_state"]["adults"].append(int(message.text))
        VariablesConstants.BOT.send_message(
            chat_id=message.from_user.id,
            text=f"Количество детей в {VariablesMutable.count_room_flag}-ом номере:",
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.children_count
        )
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВведите количество взрослых в положительном числовом выражении:",
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.adults_count
        )

@VariablesConstants.BOT.message_handler(state=HighState.children_count)
def state_high_children_count(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде high
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
                state=HighState.children_age
            )
        elif not VariablesMutable.count_room == VariablesMutable.count_room_flag:
            with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if not "children_age" in data["high_state"]:
                    data["high_state"]["children_age"] = [[]]
                else:
                    data["high_state"]["children_age"].append([])
            VariablesMutable.count_room_flag += 1
            VariablesConstants.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Количество взрослых в {VariablesMutable.count_room_flag}-ом номере:",
            )
            VariablesConstants.BOT.set_state(
                user_id=message.from_user.id,
                state=HighState.adults_count
            )
        else:
            with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
                data["high_state"]["children_age"].append([])
            VariablesConstants.BOT.send_message(
                chat_id=message.chat.id,
                text="По какой категории отсортировать лучшие показатели:",
                reply_markup=Keyboards.keyboard_sort())
            VariablesConstants.BOT.set_state(
                user_id=message.from_user.id,
                state=HighState.sort
            )
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВведите количество детей в положительном числовом выражении:",
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.children_count
        )

@VariablesConstants.BOT.message_handler(state=HighState.children_age)
def state_high_children_age(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде high
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
            if not "children_age" in data["high_state"]:
                data["high_state"]["children_age"] = [[int(message.text)]]
            elif len(data["high_state"]["children_age"]) == VariablesMutable.count_room_flag:
                data["high_state"]["children_age"][VariablesMutable.count_room_flag - 1].append(int(message.text))
            else:
                data["high_state"]["children_age"].append([int(message.text)])
        if not VariablesMutable.count_children == VariablesMutable.count_children_flag:
            VariablesMutable.count_children_flag += 1
            VariablesConstants.BOT.send_message(
                chat_id=message.from_user.id,
                text=f"Возраст {VariablesMutable.count_children_flag}-ого ребенка:",
            )
            VariablesConstants.BOT.set_state(
                user_id=message.from_user.id,
                state=HighState.children_age
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
                state=HighState.adults_count
            )
        else:
            VariablesConstants.BOT.send_message(
                chat_id=message.chat.id,
                text="По какой категории отсортировать лучшие показатели:",
                reply_markup=Keyboards.keyboard_sort())
            VariablesConstants.BOT.set_state(
                user_id=message.from_user.id,
                state=HighState.sort
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
            state=HighState.children_age
        )

@VariablesConstants.BOT.message_handler(state=HighState.sort)
def state_high_sort(message: object) -> None:
    """
    Function description:
    Функция состояния диалога с ботом по команде high
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
            state=HighState.count
        )
        with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["high_state"]["sort"] = VariablesConstants.DICT_SORT_API_HOSTEL[message.text]
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.chat.id,
            text="Неверный ввод.\nВыберите один из вариантов предложенных ниже:",
            reply_markup=Keyboards.keyboard_sort()
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.sort
        )

@VariablesConstants.BOT.message_handler(state=HighState.count)
def state_high_count(message: object) -> None:
    """
    Function description:
    Функция завершения состояния диалога с ботом по команде high
    Производит запись количества выводимых результатов

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstants.COMMANDS:
        Functions.conversation_transition(message)
        return
    elif message.text.isdigit():
        with VariablesConstants.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["high_state"]["count"] = message.text
        VariablesConstants.BOT.send_message(
            chat_id=message.chat.id,
            text=f"{data}"
        )
        VariablesConstants.BOT.delete_state(
            user_id=message.from_user.id,
            chat_id=message.chat.id
        )
    else:
        VariablesConstants.BOT.send_message(
            chat_id=message.chat.id,
            text="Неверный ввод.\nЯ хочу получить положительное число:"
        )
        VariablesConstants.BOT.set_state(
            user_id=message.from_user.id,
            state=HighState.count
        )

VariablesConstants.BOT.add_custom_filter(telebot.custom_filters.StateFilter(VariablesConstants.BOT))
