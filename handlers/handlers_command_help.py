from config_data import VariablesConstants


@VariablesConstants.BOT.message_handler(commands=["help"])
def my_help(message: object) -> None:
    """
    Function description:
    Отправляет подсказку по командам бота

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns значение:
    None
    """
    VariablesConstants.BOT.delete_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id
    )
    VariablesConstants.BOT.send_message(
        chat_id=message.chat.id,
        text=f"Рабочие команды:\n{VariablesConstants.DESCRIPTION_COMMANDS}"
    )
