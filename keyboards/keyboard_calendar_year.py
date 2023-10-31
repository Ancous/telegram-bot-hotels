from typing import Optional
from telebot import types

from config_data import Functions


def keyboard_year(start_year: Optional[int] = None) -> object:
    """
    Function description:
    Создает пользователю клавиатуру календаря относительно списка list_year
    полученного из функции create_list_year для выбора года

    Arguments:
    start_year (Optional[int]): год который передается а функцию create_list_year

    Returns:
    object: class 'telebot.types.ReplyKeyboardMarkup'
    """
    rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, selective=False)
    if not start_year:
        baton_list = [types.KeyboardButton(text=str(year)) for year in Functions.create_list_year()]
    else:
        baton_list = [types.KeyboardButton(text=str(year)) for year in Functions.create_list_year(start_year=start_year)]
    add_baton_list = []
    for baton in baton_list:
        add_baton_list.append(baton)
    rkm.add(*add_baton_list)
    return rkm
