"""
Модуль работы по команде start
"""

from config_data import FunctionsBot
from config_data import VariablesConstantsBot
from database.main_database import User
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
    user_id = message.from_user.id
    query = User.select().where(User.user_id == user_id)
    if not query.exists():
        User.create(
            user_id=message.from_user.id,
            name=message.from_user.first_name
        )
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
