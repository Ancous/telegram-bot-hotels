"""
Модуль записи пользователя в базу данных
"""

import telebot

from database import User


def create_user_db(message: telebot.types.Message) -> None:
    """
    Проверяет в базе данных id пользователя, если такого пользователя нет,
    то записывает id пользователя и имя пользователя в базу данных

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    None
    """
    user_id = message.from_user.id
    query = User.select().where(User.User == user_id)
    if not query.exists():
        User.create(
            User=message.from_user.id,
            Name=message.from_user.first_name
        )
