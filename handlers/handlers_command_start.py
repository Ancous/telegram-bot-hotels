"""
Модуль работы по команде start
"""

from config_data import FunctionsBot
from config_data import VariablesConstantsBot
from database import create_user_db
from keyboards import KeyboardsBot


@VariablesConstantsBot.BOT.message_handler(commands=["start"])
def start(message: object) -> None:
    """
    При первом посещении записывает id пользователя и имя пользователя в базу данных
    Отправляет текст приветствия

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    create_user_db(message=message)
    VariablesConstantsBot.BOT.delete_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id
    )
    VariablesConstantsBot.BOT.send_message(
        chat_id=message.chat.id,
        text=FunctionsBot.welcome(
            name=message.from_user.first_name
        ),
        reply_markup=KeyboardsBot.keyboard_start()
    )
