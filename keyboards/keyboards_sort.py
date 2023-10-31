from telebot import types


def keyboard_sort() -> object:
    """
    Function description:
    Создает клавиатуру для отображения возможной сортировки

    Arguments:
    None

    Returns:
    object: class 'telebot.types.ReplyKeyboardMarkup'
    """
    rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, selective=False)
    rkm.add(
        types.KeyboardButton(text="Сортировка по ценам"),
        types.KeyboardButton(text="Сортировка по оценкам проживающих"),
        types.KeyboardButton(text="Сортировка по расстоянию от центра"),
        types.KeyboardButton(text="Сортировка по звездности отелей"),
        types.KeyboardButton(text="Сортировка по количеству отзывов проживающих")
    )
    return rkm
