import telebot
from telebot.types import ReplyKeyboardRemove
from datetime import datetime

from config_data import VariablesMutableBot, VariablesConstantsBot, FunctionsBot
from keyboards import KeyboardsBot
from states import CustomState


@VariablesConstantsBot.BOT.message_handler(state="*", commands=["custom"])
def state_custom_start(message) -> None:
    """
    Функция начального состояния диалога с ботом по команде custom
    Обновляет все атрибуты класса VariablesMutable

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    VariablesMutableBot.reset_parameters()
    VariablesConstantsBot.BOT.send_message(
        chat_id=message.from_user.id,
        text="По какому городу будем производить подбор отелей:",
        reply_markup=ReplyKeyboardRemove()
    )
    VariablesConstantsBot.BOT.set_state(
        user_id=message.from_user.id,
        state=CustomState.city
    )
    with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
        data["custom_state"] = {}

@VariablesConstantsBot.BOT.message_handler(state=CustomState.city)
def state_custom_city(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
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
            chat_id=message.from_user.id,
            text="Определитесь с датой заезда в отель.\nЗаезд. Выберите год:",
            reply_markup=KeyboardsBot.keyboard_year()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.arrival_year
        )
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["custom_state"]["city"] = message.text

@VariablesConstantsBot.BOT.message_handler(state=CustomState.arrival_year)
def state_custom_arrival_year(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
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
                data["custom_state"]["arrival_day"] = int(message.text)
                VariablesMutableBot.year = False
                VariablesMutableBot.month = False
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Определитесь с датой выезда из отель.\nВыезд. Выберите год:",
                    reply_markup=KeyboardsBot.keyboard_year(data["custom_state"]["arrival_year"])
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
                data["custom_state"]["departure_month"] = VariablesConstantsBot.DICT_MOUNT_STR_INT[message.text.capitalize()]
                if (int(data["custom_state"]["arrival_year"]) == int(data["custom_state"]["departure_year"]) and
                    int(data["custom_state"]["arrival_month"]) == int(data["custom_state"]["departure_month"])):
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.from_user.id,
                        text="Выезд. Выберите день:",
                        reply_markup=KeyboardsBot.keyboard_day(
                            year=int(data["custom_state"]["arrival_year"]),
                            month=int(data["custom_state"]["arrival_month"]),
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
                return
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
                data["custom_state"]["departure_day"] = int(message.text)
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="По какой категории отсортировать худшие показатели:",
                    reply_markup=KeyboardsBot.keyboard_sort())
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.sort
                )
                return
            else:
                if (int(data["custom_state"]["arrival_year"]) == int(data["custom_state"]["departure_year"]) and
                    int(data["custom_state"]["arrival_month"]) == int(data["custom_state"]["departure_month"])):
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.from_user.id,
                        text="Неверный ввод.\nВыезд. Выберите день предложенный ниже:",
                        reply_markup=KeyboardsBot.keyboard_day(
                            data["custom_state"]["arrival_day"],
                            year=data["custom_state"]["departure_year"],
                            month=data["custom_state"]["departure_month"]
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

@VariablesConstantsBot.BOT.message_handler(state=CustomState.sort)
def state_custom_sort(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Производит запись выбранной сортировки

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    elif message.text in VariablesConstantsBot.DICT_SORT_API_HOSTEL:
        FunctionsBot.create_list_values_filters(message.text)
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["custom_state"]["sort"] = VariablesConstantsBot.DICT_SORT_API_HOSTEL[message.text]
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Какой фильтр будем использовать:",
            reply_markup=KeyboardsBot.keyboard_filter()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters
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

@VariablesConstantsBot.BOT.message_handler(state=CustomState.filters)
def state_custom_filters(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Предлагает фильтры

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    elif message.text == "Завершить с выбором фильтров":
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Количество номеров:",
            reply_markup=ReplyKeyboardRemove()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.room_count
        )
        return
    elif message.text in VariablesConstantsBot.DICT_FILTERS_API_HOSTEL:
        if message.text in VariablesMutableBot.list_del_filters[0]:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="По этому фильтру будет производиться сортировка.\nВыберите фильтр из предложенных ниже:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )
        elif not message.text in VariablesMutableBot.list_del_filters:
            VariablesMutableBot.list_del_filters.append(message.text)
            if message.text == "Фильтр по ценам":
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Введите минимальную цену:",
                    reply_markup=ReplyKeyboardRemove()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.filters_price
                )
            if message.text == "Фильтр по названию отеля":
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Введите название отеля:",
                    reply_markup=ReplyKeyboardRemove()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.filters_hotel_name
                )
            if message.text == "Фильтр по оценкам проживающих":
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Выберите минимальную оценку рейтинга отеля для поиска:",
                    reply_markup=KeyboardsBot.keyboard_guest_rating()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.filters_guest_rating
                )
            if message.text == "Фильтр по специальным услугам":
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Выберите специальную услугу которую желаете видеть в номере:",
                    reply_markup=KeyboardsBot.keyboard_accessibility()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.filters_accessibility
                )
            if message.text == "Фильтр по причине визита":
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Выберите причину визита:",
                    reply_markup=KeyboardsBot.keyboard_traveler_type()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.filters_traveler_type
                )
            if message.text == "Фильтр по питанию":
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Выберите вариант питания:",
                    reply_markup=KeyboardsBot.keyboard_meal_plan()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.filters_meal_plan
                )
            if message.text == "Фильтр по типу размещения":
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Выберите тип размещения:",
                    reply_markup=KeyboardsBot.keyboard_lodging()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.filters_lodging
                )
            if message.text == "Фильтр по услугам":
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Выберите предпочтение при выборе отеля отеле:",
                    reply_markup=KeyboardsBot.keyboard_amenities()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.filters_amenities
                )
            if message.text == "Фильтр по звездности отелей":
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Выберите звёздность отеля:",
                    reply_markup=KeyboardsBot.keyboard_stars()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.filters_stars
                )
            if message.text == "Фильтр по услугам оплаты":
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Выберите способ оплаты:",
                    reply_markup=KeyboardsBot.keyboard_payment_type()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.filters_payment_type
                )
            if message.text == "Фильтр по количеству комнат в номере":
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Выберите количеству комнат в номере:",
                    reply_markup=KeyboardsBot.keyboard_bedroom_filter()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.filters_bedroom
                )
            if message.text == "Фильтр по свободным номерам на нужные даты":
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Показывать только свободные номера на нужные даты?",
                    reply_markup=KeyboardsBot.keyboard_available_filter()
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.filters_available
                )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Такой фильтр уже выбран.\nВыберите фильтр из предложенных ниже:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВыберите фильтр из предложенных ниже:",
            reply_markup=KeyboardsBot.keyboard_filter()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters
        )

@VariablesConstantsBot.BOT.message_handler(state=CustomState.filters_price)
def state_custom_filters_price(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с фильтром цены

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    else:
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if message.text.replace('.','',1).isdigit() and not "price_min" in data["custom_state"]:
                data["custom_state"]["price_min"] = int(message.text)
            elif message.text.replace('.','',1).isdigit():
                if int(message.text) < data["custom_state"]["price_min"]:
                    VariablesConstantsBot.BOT.send_message(
                        chat_id=message.from_user.id,
                        text="Неверный ввод.\nМаксимальная цена должна бть выше минимальной."
                    )
                    VariablesConstantsBot.BOT.set_state(
                        user_id=message.from_user.id,
                        state=CustomState.filters_price
                    )
                else:
                    data["custom_state"]["price_max"] = int(message.text)
            else:
                VariablesConstantsBot.BOT.send_message(
                    chat_id=message.from_user.id,
                    text="Неверный ввод.\nВведите цену в числовом выражении."
                )
                VariablesConstantsBot.BOT.set_state(
                    user_id=message.from_user.id,
                    state=CustomState.filters_price
                )
        if not "price_max" in data["custom_state"]:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Введите максимальную цену:"
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters_price
            )
            return
        if (not VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
                len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL) + 1):
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.room_count
            )
        elif (VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
              len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL)):
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
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё фильтр будем использовать:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )

@VariablesConstantsBot.BOT.message_handler(state=CustomState.filters_hotel_name)
def state_custom_filters_hotel_name(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с фильтром названия отеля

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
        data["custom_state"]["hotel_name"] = message.text
    if (not VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
            len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL) + 1):
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Количество номеров:",
            reply_markup=ReplyKeyboardRemove()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.room_count
        )
    elif (VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
          len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL)):
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
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Какой ещё фильтр будем использовать:",
            reply_markup=KeyboardsBot.keyboard_filter()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters
        )

@VariablesConstantsBot.BOT.message_handler(state=CustomState.filters_guest_rating)
def state_custom_filters_guest_rating(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с фильтром звездности отеля

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    elif message.text in VariablesConstantsBot.DICT_GUEST_RATING:
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            data["custom_state"]["guest_rating"] = VariablesConstantsBot.DICT_GUEST_RATING[message.text]
        if (not VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
                len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL) + 1):
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.room_count
            )
        elif (VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
              len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL)):
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
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё фильтр будем использовать:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВыберите один из вариантов ниже:",
            reply_markup=KeyboardsBot.keyboard_guest_rating()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_guest_rating
        )

@VariablesConstantsBot.BOT.message_handler(state=CustomState.filters_accessibility)
def state_custom_filters_accessibility(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с фильтром специальных услуг

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    elif message.text == "Завершить с выбором специальных услуг" or len(VariablesMutableBot.list_del_accessibility) + 1 == len(VariablesConstantsBot.DICT_ACCESSIBILITY):
        if not message.text == "Завершить с выбором специальных услуг":
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                data["custom_state"]["accessibility"].append(VariablesConstantsBot.DICT_ACCESSIBILITY[message.text])
        if (not VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
                len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL) + 1):
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.room_count
            )
        elif (VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
              len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL)):
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
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё фильтр будем использовать:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )
        return
    if message.text in VariablesConstantsBot.DICT_ACCESSIBILITY:
        if not message.text in VariablesMutableBot.list_del_accessibility:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if not "accessibility" in data["custom_state"]:
                    data["custom_state"]["accessibility"] = [VariablesConstantsBot.DICT_ACCESSIBILITY[message.text]]
                else:
                    data["custom_state"]["accessibility"].append(VariablesConstantsBot.DICT_ACCESSIBILITY[message.text])
            VariablesMutableBot.list_del_accessibility.append(message.text)
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё специальную услугу будем использовать:",
                reply_markup=KeyboardsBot.keyboard_accessibility()
            )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Такая специальная услуга уже выбрана.\nВыберите специальную услугу из предложенных ниже:",
                reply_markup=KeyboardsBot.keyboard_accessibility()
            )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_accessibility
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВыберите специальную услугу из предложенных ниже:",
            reply_markup=KeyboardsBot.keyboard_accessibility()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_accessibility
        )

@VariablesConstantsBot.BOT.message_handler(state=CustomState.filters_traveler_type)
def state_custom_filters_traveler_type(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с фильтром причины визита

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text == "Завершить с выбором причины визита" or len(VariablesMutableBot.list_del_traveler_type) + 1 == len(VariablesConstantsBot.DICT_TRAVELER_TYPE):
        if not message.text == "Завершить с выбором причины визита":
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                data["custom_state"]["traveler_type"].append(VariablesConstantsBot.DICT_TRAVELER_TYPE[message.text])
        if (not VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
                len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL) + 1):
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.room_count
            )
        elif (VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
              len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL)):
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
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё фильтр будем использовать:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )
        return
    if message.text in VariablesConstantsBot.DICT_TRAVELER_TYPE:
        if not message.text in VariablesMutableBot.list_del_traveler_type:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if not "traveler_type" in data["custom_state"]:
                    data["custom_state"]["traveler_type"] = [VariablesConstantsBot.DICT_TRAVELER_TYPE[message.text]]
                else:
                    data["custom_state"]["traveler_type"].append(VariablesConstantsBot.DICT_TRAVELER_TYPE[message.text])
            VariablesMutableBot.list_del_traveler_type.append(message.text)
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какую ещё причину визита будем использовать:",
                reply_markup=KeyboardsBot.keyboard_traveler_type()
            )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Такая причина визита уже выбрана.\nВыберите причину визита из предложенных ниже:",
                reply_markup=KeyboardsBot.keyboard_traveler_type()
            )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_traveler_type
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВыберите причину визита из предложенных ниже:",
            reply_markup=KeyboardsBot.keyboard_traveler_type()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_traveler_type
        )
@VariablesConstantsBot.BOT.message_handler(state=CustomState.filters_meal_plan)
def state_custom_filters_meal_plan(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с фильтром вариантов питания

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text == "Завершить с выбором вариантов питания" or len(VariablesMutableBot.list_del_meal_plan) + 1 == len(VariablesConstantsBot.DICT_MEAL_PLAN):
        if not message.text == "Завершить с выбором вариантов питания":
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                data["custom_state"]["meal_plan"].append(VariablesConstantsBot.DICT_MEAL_PLAN[message.text])
        if (not VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
                len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL) + 1):
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.room_count
            )
        elif (VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
              len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL)):
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
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё фильтр будем использовать:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )
        return
    if message.text in VariablesConstantsBot.DICT_MEAL_PLAN:
        if not message.text in VariablesMutableBot.list_del_meal_plan:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if not "meal_plan" in data["custom_state"]:
                    data["custom_state"]["meal_plan"] = [VariablesConstantsBot.DICT_MEAL_PLAN[message.text]]
                else:
                    data["custom_state"]["meal_plan"].append(VariablesConstantsBot.DICT_MEAL_PLAN[message.text])
            VariablesMutableBot.list_del_meal_plan.append(message.text)
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё вариант питания будем использовать:",
                reply_markup=KeyboardsBot.keyboard_meal_plan()
            )

        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Такой вариант питания уже выбран.\nВыберите вариант питания из предложенных ниже:",
                reply_markup=KeyboardsBot.keyboard_meal_plan()
            )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_meal_plan
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВыберите вариант питания из предложенных ниже:",
            reply_markup=KeyboardsBot.keyboard_meal_plan()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_meal_plan
        )

@VariablesConstantsBot.BOT.message_handler(state=CustomState.filters_lodging)
def state_custom_filters_lodging(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с фильтром типа размещения

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text == "Завершить с выбором типа размещения" or len(VariablesMutableBot.list_del_lodging) + 1 == len(VariablesConstantsBot.DICT_LODGING):
        if not message.text == "Завершить с выбором типа размещения":
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                data["custom_state"]["lodging"].append(VariablesConstantsBot.DICT_LODGING[message.text])
        if (not VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
                len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL) + 1):
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.room_count
            )
        elif (VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
              len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL)):
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
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё фильтр будем использовать:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )
        return
    if message.text in VariablesConstantsBot.DICT_LODGING:
        if not message.text in VariablesMutableBot.list_del_lodging:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if not "lodging" in data["custom_state"]:
                    data["custom_state"]["lodging"] = [VariablesConstantsBot.DICT_LODGING[message.text]]
                else:
                    data["custom_state"]["lodging"].append(VariablesConstantsBot.DICT_LODGING[message.text])
            VariablesMutableBot.list_del_lodging.append(message.text)
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё тип размещения будем использовать:",
                reply_markup=KeyboardsBot.keyboard_lodging()
            )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Такой тип размещения уже выбран.\nВыберите тип размещения из предложенных ниже:",
                reply_markup=KeyboardsBot.keyboard_lodging()
            )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_lodging
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВыберите тип размещения из предложенных ниже:",
            reply_markup=KeyboardsBot.keyboard_lodging()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_lodging
        )

@VariablesConstantsBot.BOT.message_handler(state=CustomState.filters_amenities)
def state_custom_filters_amenities(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с фильтром услуг в отеле

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text == "Завершить с выбором желаемых услуг в отеле" or len(VariablesMutableBot.list_del_amenities) + 1 == len(VariablesConstantsBot.DICT_AMENITIES):
        if not message.text == "Завершить с выбором желаемых услуг в отеле":
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                data["custom_state"]["amenities"].append(VariablesConstantsBot.DICT_AMENITIES[message.text])
        if (not VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
                len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL) + 1):
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.room_count
            )
        elif (VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
              len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL)):
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
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё фильтр будем использовать:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )
        return
    if message.text in VariablesConstantsBot.DICT_AMENITIES:
        if not message.text in VariablesMutableBot.list_del_amenities:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if not "amenities" in data["custom_state"]:
                    data["custom_state"]["amenities"] = [VariablesConstantsBot.DICT_AMENITIES[message.text]]
                else:
                    data["custom_state"]["amenities"].append(VariablesConstantsBot.DICT_AMENITIES[message.text])
            VariablesMutableBot.list_del_amenities.append(message.text)
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какая услуга ещё предпочтительна при выборе отеля:",
                reply_markup=KeyboardsBot.keyboard_amenities()
            )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Такая услуга уже выбрана.\nВыберите желаемую услугу при выборе отеля ниже:",
                reply_markup=KeyboardsBot.keyboard_amenities()
            )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_amenities
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВыберите желаемую услугу при выборе отеля ниже:",
            reply_markup=KeyboardsBot.keyboard_amenities()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_amenities
        )

@VariablesConstantsBot.BOT.message_handler(state=CustomState.filters_stars)
def state_custom_filters_stars(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с фильтром звёздности отеля

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text == "Завершить с выбором звёздности отеля" or len(VariablesMutableBot.list_del_stars) + 1 == len(VariablesConstantsBot.DICT_STARS):
        if not message.text == "Завершить с выбором звёздности отеля":
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                data["custom_state"]["stars"].append(VariablesConstantsBot.DICT_STARS[message.text])
        if (not VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
                len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL) + 1):
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.room_count
            )
        elif (VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
              len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL)):
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
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё фильтр будем использовать:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )
        return
    if message.text in VariablesConstantsBot.DICT_STARS:
        if not message.text in VariablesMutableBot.list_del_stars:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if not "stars" in data["custom_state"]:
                    data["custom_state"]["stars"] = [VariablesConstantsBot.DICT_STARS[message.text]]
                else:
                    data["custom_state"]["stars"].append(VariablesConstantsBot.DICT_STARS[message.text])
            VariablesMutableBot.list_del_stars.append(message.text)
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какая звёздность отеля ещё предпочтительна:",
                reply_markup=KeyboardsBot.keyboard_stars()
            )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Такая звёздность отеля уже выбрана.\nВыберите желаемую звёздность отеля ниже:",
                reply_markup=KeyboardsBot.keyboard_stars()
            )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_stars
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВыберите желаемую звёздность отеля ниже:",
            reply_markup=KeyboardsBot.keyboard_stars()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_stars
        )

@VariablesConstantsBot.BOT.message_handler(state=CustomState.filters_payment_type)
def state_custom_filters_payment_type(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с фильтром услуг по оплате

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text == "Завершить с выбором услуг по оплате" or len(VariablesMutableBot.list_del_payment_type) + 1 == len(VariablesConstantsBot.DICT_PAYMENT_TYPE):
        if not message.text == "Завершить с выбором услуг по оплате":
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                data["custom_state"]["payment_type"].append(VariablesConstantsBot.DICT_PAYMENT_TYPE[message.text])
        if (not VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
                len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL) + 1):
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.room_count
            )
        elif (VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
              len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL)):
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
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё фильтр будем использовать:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )
        return
    if message.text in VariablesConstantsBot.DICT_PAYMENT_TYPE:
        if not message.text in VariablesMutableBot.list_del_payment_type:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if not "payment_type" in data["custom_state"]:
                    data["custom_state"]["payment_type"] = [VariablesConstantsBot.DICT_PAYMENT_TYPE[message.text]]
                else:
                    data["custom_state"]["payment_type"].append(VariablesConstantsBot.DICT_PAYMENT_TYPE[message.text])
            VariablesMutableBot.list_del_payment_type.append(message.text)
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какая услуга по оплате ещё нужна:",
                reply_markup=KeyboardsBot.keyboard_payment_type()
            )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Такая услуга по оплате уже выбрана.\nВыберите желаемую услуга по оплате ниже:",
                reply_markup=KeyboardsBot.keyboard_payment_type()
            )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_payment_type
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВыберите желаемую услуга по оплате ниже:",
            reply_markup=KeyboardsBot.keyboard_payment_type()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_payment_type
        )

@VariablesConstantsBot.BOT.message_handler(state=CustomState.filters_bedroom)
def state_custom_filters_bedroom_filter(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с фильтром количества комнат в номере

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text == "Завершить с выбором количества комнат в номере" or len(VariablesMutableBot.list_del_bedroom_filter) + 1 == len(VariablesConstantsBot.DICT_BEDROOM_FILTER):
        if not message.text == "Завершить с выбором количества комнат в номере":
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                data["custom_state"]["bedroom_filter"].append(VariablesConstantsBot.DICT_BEDROOM_FILTER[message.text])
        if (not VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
                len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL) + 1):
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.room_count
            )
        elif (VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
              len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL)):
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
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё фильтр будем использовать:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )
        return
    if message.text in VariablesConstantsBot.DICT_BEDROOM_FILTER:
        if not message.text in VariablesMutableBot.list_del_bedroom_filter:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if not "bedroom_filter" in data["custom_state"]:
                    data["custom_state"]["bedroom_filter"] = [VariablesConstantsBot.DICT_BEDROOM_FILTER[message.text]]
                else:
                    data["custom_state"]["bedroom_filter"].append(VariablesConstantsBot.DICT_BEDROOM_FILTER[message.text])
            VariablesMutableBot.list_del_bedroom_filter.append(message.text)
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какие номера вас ещё интересуют:",
                reply_markup=KeyboardsBot.keyboard_bedroom_filter()
            )
        else:
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Такое количество комнат в номере уже выбрано.\nВыберите количество комнат в номере ниже:",
                reply_markup=KeyboardsBot.keyboard_bedroom_filter()
            )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_bedroom
        )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВыберите количество комнат в номере ниже:",
            reply_markup=KeyboardsBot.keyboard_bedroom_filter()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_bedroom
        )

@VariablesConstantsBot.BOT.message_handler(state=CustomState.filters_available)
def state_custom_filters_available_filter(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
    Работает с фильтром доступности брони номера в отеле

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
        return
    if message.text == "Да":
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if not "available_filter" in data["custom_state"]:
                data["custom_state"]["available_filter"] = "SHOW_AVAILABLE_ONLY"
        if (not VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
                len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL) + 1):
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.room_count
            )
        elif (VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
              len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL)):
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
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё фильтр будем использовать:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )
    elif  message.text == "Нет":
        if (not VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
                len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL) + 1):
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Количество номеров:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.room_count
            )
        elif (VariablesMutableBot.list_del_filters[0] in ("Фильтр по ценам", "Фильтр по оценкам проживающих", "Фильтр по звездности отелей") and
              len(VariablesMutableBot.list_del_filters) == len(VariablesConstantsBot.DICT_FILTERS_API_HOSTEL)):
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
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.from_user.id,
                text="Какой ещё фильтр будем использовать:",
                reply_markup=KeyboardsBot.keyboard_filter()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.filters
            )
    else:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.from_user.id,
            text="Неверный ввод.\nВыберите один из вариантов ниже:",
            reply_markup=KeyboardsBot.keyboard_available_filter()
        )
        VariablesConstantsBot.BOT.set_state(
            user_id=message.from_user.id,
            state=CustomState.filters_available
        )

@VariablesConstantsBot.BOT.message_handler(state=CustomState.room_count)
def state_custom_room_count(message) -> None:
    """
    Функция состояния диалога с ботом по команде custom
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

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    elif message.text.isdigit() and int(message.text) >= 1:
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if not "adults" in data["custom_state"]:
                data["custom_state"]["adults"] = [int(message.text)]
            else:
                data["custom_state"]["adults"].append(int(message.text))
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
                state=CustomState.children_age
            )
        elif not VariablesMutableBot.count_room == VariablesMutableBot.count_room_flag:
            with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
                if not "children_age" in data["custom_state"]:
                    data["custom_state"]["children_age"] = [[]]
                else:
                    data["custom_state"]["children_age"].append([])
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
                data["custom_state"]["children_age"].append([])
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.chat.id,
                text="По какой категории отсортировать лучшие показатели:",
                reply_markup=KeyboardsBot.keyboard_sort())
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

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    if message.text in VariablesConstantsBot.COMMANDS:
        FunctionsBot.conversation_transition(message)
    elif message.text.isdigit() and  0 < int(message.text) < 18:
        with VariablesConstantsBot.BOT.retrieve_data(user_id=message.from_user.id) as data:
            if not "children_age" in data["custom_state"]:
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
                text="Количество которое необходимо вывести:",
                reply_markup=ReplyKeyboardRemove()
            )
            VariablesConstantsBot.BOT.set_state(
                user_id=message.from_user.id,
                state=CustomState.count
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

@VariablesConstantsBot.BOT.message_handler(state=CustomState.count)
def state_custom_count(message) -> None:
    """
    Функция завершения состояния диалога с ботом по команде custom
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
            data["custom_state"]["count"] = message.text
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text=f"{data['custom_state']}"
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
            state=CustomState.count
        )

VariablesConstantsBot.BOT.add_custom_filter(telebot.custom_filters.StateFilter(VariablesConstantsBot.BOT))
