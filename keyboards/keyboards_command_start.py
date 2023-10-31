from telebot import types


def keyboard_start() -> object:
    """
    Function description:
    Создает клавиатуру для команды /start

    Arguments:
    None

    Returns:
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
