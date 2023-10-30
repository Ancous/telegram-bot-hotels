from config_data import bot, welcome
from database import User
from keyboards import keyboard_start


@bot.message_handler(commands=["start"])
def start(message: object) -> None:
    """
    Описание функции:
    При первом посещении записывает id пользователя и имя пользователя в базу данных
    Отправляет текст приветствия

    Параметры:
    message (object): class 'telebot.types.Message'

    Возвращаемое значение:
    None
    """
    user_id = message.from_user.id
    query = User.select().where(User.user_id == user_id)
    if not query.exists():
        User.create(
            user_id=message.from_user.id,
            name=message.from_user.first_name
        )
    bot.send_message(
        chat_id=message.chat.id,
        text=welcome(
            name=message.from_user.first_name
        ),
        reply_markup=keyboard_start()
    )
    bot.delete_state(message.from_user.id)