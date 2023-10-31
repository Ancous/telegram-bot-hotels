from config_data import VariablesConstants
from keyboards import keyboard_start


@VariablesConstants.BOT.message_handler(func=lambda message: not message.text in VariablesConstants.COMMANDS)
def error_text(message: object) -> None:
    """
    Function description:
    Если пользователь написал не обрабатываемое сообщение
    отправляет в ответ подсказку по командам бота и сообщение о не понимании, что делать

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    VariablesConstants.BOT.send_message(
        chat_id=message.chat.id,
        text="Я не понимаю вашего запроса. Выберите команду из предложенных ниже",
        reply_markup = keyboard_start()
    )