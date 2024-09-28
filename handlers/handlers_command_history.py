"""
Модуль работы по команде history
"""

import telebot

from database import read_db
from config_data import VariablesConstantsBot


@VariablesConstantsBot.BOT.message_handler(commands=["history"])
def history(message: telebot.types.Message) -> None:
    """
    Выводит историю последних десять запросов поиска с ответами

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    VariablesConstantsBot.BOT.delete_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id
    )
    result = read_db(message=message)
    if not result:
        VariablesConstantsBot.BOT.send_message(
            chat_id=message.chat.id,
            text="У вас нет истории запросов."
        )
    else:
        for values in result.values():
            text = (
                f"Запрос:\n"
                f"Тип поиска : {values['request']['Type']}\n"
                f"Вид сортировки : {values['request']['Param_sort']}\n"
                f"Страна поиска : {values['request']['Country']}\n"
                f"Город поиска : {values['request']['City']}\n"
                f"Дата заезда : {values['request']['Arrival_date']}\n"
                f"Дата выезда : {values['request']['Departure_date']}\n"
                f"Количество арендуемых номеров : {values['request']['Count_rooms']}\n"
                f"Количество взрослых : {values['request']['Count_adults']}\n"
                f"Количество детей : {values['request']['Count_children']}\n"
                f"\n"
            )
            for key_1, values_1 in values["response"].items():
                text += (
                    f"Ответ {key_1}:\n"
                    f"\t\t\t\t\tНазвание отеля : {values_1['Name_hotels']}\n"
                    f"\t\t\t\t\tКраткая информация : {values_1['Short_info']}\n"
                    f"\t\t\t\t\tИнформация по отелю :\n {values_1['Url_site']}\n"
                )
            VariablesConstantsBot.BOT.send_message(
                chat_id=message.chat.id,
                text=text
            )
