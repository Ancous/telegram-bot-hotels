from config_data import Functions
from config_data import VariablesConstants
from database.main_database import User
from keyboards import keyboard_start


@VariablesConstants.BOT.message_handler(commands=["start"])
def start(message: object) -> None:
    """
    Function description:
    При первом посещении записывает id пользователя и имя пользователя в базу данных
    Отправляет текст приветствия

    Arguments:
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
    VariablesConstants.BOT.delete_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id
    )
    VariablesConstants.BOT.send_message(
        chat_id=message.chat.id,
        text=Functions.welcome(
            name=message.from_user.first_name
        ),
        reply_markup=keyboard_start()
    )
