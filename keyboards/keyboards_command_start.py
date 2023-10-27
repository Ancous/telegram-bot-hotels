from telebot import types


def keyboard_start() -> object:
    """
    Описание функции:
    Создает клавиатуру для команды /start

    Параметры:
    None

    Возвращаемое значение:
    object: class 'telebot.types.ReplyKeyboardMarkup'
    """
    rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    rkm.add(
        types.KeyboardButton(text="/start"),
        types.KeyboardButton(text="/help"),
        types.KeyboardButton(text="/low"),
        types.KeyboardButton(text="/high"),
        types.KeyboardButton(text="/custom"),
        types.KeyboardButton(text="/history")
    )
    return rkm
