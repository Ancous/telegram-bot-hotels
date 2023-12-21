"""
...
"""

from config_data import VariablesConstantsBot


@VariablesConstantsBot.BOT.message_handler(commands=["history"])
def history(message: object) -> None:
    """
    ...

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    VariablesConstantsBot.BOT.delete_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id
    )
    VariablesConstantsBot.BOT.send_message(
        chat_id=message.chat.id,
        text="Здесь будет история запросов"
    )
