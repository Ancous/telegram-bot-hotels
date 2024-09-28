"""
Модуль работы по неизвестным сообщениям и командам для бота
"""

import telebot

from keyboards import KeyboardsBot
from config_data import VariablesConstantsBot


@VariablesConstantsBot.BOT.message_handler(func=lambda message: message.text not in VariablesConstantsBot.COMMANDS)
def error_text(message: telebot.types.Message) -> None:
    """
    Если пользователь написал не обрабатываемое сообщение
    отправляет в ответ подсказку по командам бота и сообщение о не понимании что делать

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    VariablesConstantsBot.BOT.send_message(
        chat_id=message.chat.id,
        text="Я не понимаю вашего запроса. Выберите команду из предложенных ниже",
        reply_markup=KeyboardsBot.keyboard_start()
    )
