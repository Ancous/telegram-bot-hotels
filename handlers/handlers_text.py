from config_data import VariablesConstantsBot
from keyboards import KeyboardsBot


@VariablesConstantsBot.BOT.message_handler(func=lambda message: not message.text in VariablesConstantsBot.COMMANDS)
def error_text(message: object) -> None:
    """
    Если пользователь написал не обрабатываемое сообщение
    отправляет в ответ подсказку по командам бота и сообщение о не понимании что делать

    Arguments:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    VariablesConstantsBot.BOT.send_message(
        chat_id=message.chat.id,
        text="Я не понимаю вашего запроса. Выберите команду из предложенных ниже",
        reply_markup=KeyboardsBot.keyboard_start()
    )