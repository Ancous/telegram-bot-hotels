"""
Модуль работы по команде help
"""

from config_data import VariablesConstantsBot


@VariablesConstantsBot.BOT.message_handler(commands=["help"])
def my_help(message: object) -> None:
    """
    Отправляет подсказку по командам бота

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns значение:
    None
    """
    VariablesConstantsBot.BOT.delete_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id
    )
    VariablesConstantsBot.BOT.send_message(
        chat_id=message.chat.id,
        text=f"Рабочие команды:\n{VariablesConstantsBot.DESCRIPTION_COMMANDS}"
    )
