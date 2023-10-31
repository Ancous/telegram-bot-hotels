from typing import Optional
from telebot import types

from config_data import Functions


def keyboard_month(start_month: Optional[int] = None) -> object:
    """
    Function description:
    Создает пользователю клавиатуру календаря относительно списка list_month
    полученного из функции create_list_month для выбора месяца

    Arguments:
    start_month (Optional[int]): число месяца которое передается а функцию create_list_month

    Returns:
    object: class 'telebot.types.ReplyKeyboardMarkup'
    """
    rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, selective=False)
    if not start_month:
        baton_list = [types.KeyboardButton(text=str(year)) for year in Functions.create_list_month()]
    else:
        baton_list = [types.KeyboardButton(text=str(year)) for year in Functions.create_list_month(start_month=start_month)]
    add_baton_list = []
    for baton in baton_list:
        add_baton_list.append(baton)
    rkm.add(*add_baton_list)
    return rkm
