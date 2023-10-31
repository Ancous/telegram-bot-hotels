from typing import Optional
from telebot import types

from config_data import Functions


def keyboard_day(year: int, month: int, start_day: Optional[int] = None) -> object:
    """
    Function description:
    Создает пользователю клавиатуру календаря относительно списка list_day
    полученного из функции create_list_day для выбора дня месяца

    Arguments:
    year (int): первый элемент списка list_year (год заселения в номер)
    month (int): первый элемент списка list_month (месяц заселения в номер)
    start_day (Optional[int]): число дня месяца от которого создается список

    Returns:
    object: class 'telebot.types.ReplyKeyboardMarkup'
    """
    rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=10, selective=False)
    if not start_day:
        baton_list = [types.KeyboardButton(text=day_1) for day_1 in Functions.create_list_day(year=year, month=month)]
    else:
        baton_list = [types.KeyboardButton(text=day_1) for day_1 in Functions.create_list_day(year=year, month=month, start_day=start_day)]
    add_baton_list = []
    for baton in baton_list:
        add_baton_list.append(baton)
    rkm.add(*add_baton_list)
    return rkm
