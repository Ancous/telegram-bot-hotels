import time


def welcome(name) -> str:
    """
    Описание функции:
    Формирует текст приветствия при выполнении команды /start

    Параметры:
    name (str): имя пользователя

    Возвращаемое значение:
    str: текст приветствия
    """
    time_now = time.localtime(time.time()).tm_hour
    if 0 <= time_now <= 5:
        welcome_text = "Доброй ночи"
    elif 6 <= time_now <= 11:
        welcome_text = "Доброе утро"
    elif 12 <= time_now <= 17:
        welcome_text = "Добрый день"
    else:
        welcome_text = "Добрый вечер"
    return (f"{welcome_text} {name}. Для дальнейшего использования бота нажмите одну из кнопок ниже.\n"
            f"/start - начало диалога с ботом\n"
            f"/help - информация по кнопкам и командам\n"
            f"/low - вывод худших показателей\n"
            f"/high - вывод лучших показателей\n"
            f"/custom - вывод показателей пользовательского диапазона\n"
            f"/history - вывод истории запросов пользователей")