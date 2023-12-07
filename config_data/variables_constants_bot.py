import os
import telebot

from dotenv import load_dotenv


load_dotenv()

class VariablesConstantsBot:
    """
    Класс для хранения постоянных переменных

    Attributes:
    BOT (object): class 'telebot.TeleBot' для запуска бота
    DB_PATH (str): название базы данных
    COMMANDS (tuple): кортеж с командами бота
    DESCRIPTION_COMMANDS (str): описание команд бота
    DICT_SORT_API_HOSTEL (dict): словарь для вывода пользователю возможной сортировки и перевода значений сортировки для работы с API-Hotels.com
    DICT_MOUNT_STR_INT (dict): словарь для перевода строкового значения месяца в числовое значение
    DICT_FILTERS_API_HOSTEL (dict): словарь всех фильтров для работы с API-Hotels.com
    DICT_GUEST_RATING (dict): словарь фильтров по оценкам проживающих в отеле для работы с API-Hotels.com
    DICT_ACCESSIBILITY (dict): словарь фильтров по специальным услугам в отеле для работы с API-Hotels.com
    DICT_TRAVELER_TYPE (dict): словарь фильтров по причине визита в отель для работы с API-Hotels.com
    DICT_MEAL_PLAN (dict): словарь фильтров по вариантам питания в отеле для работы с API-Hotels.com
    DICT_LODGING (dict): словарь фильтров по типу размещения в отеле для работы с API-Hotels.com
    DICT_AMENITIES (dict): словарь фильтров по услугам в отеле для работы с API-Hotels.com
    DICT_STARS (dict): словарь фильтров по звездности отелей для работы с API-Hotels.com
    DICT_PAYMENT_TYPE (dict): словарь фильтров по услугам оплаты в отеле для работы с API-Hotels.com
    DICT_BEDROOM_FILTER (dict): словарь фильтров по количеству комнат в номере отеля для работы с API-Hotels.com
    """
    BOT = telebot.TeleBot(os.getenv("TOKEN_BOT"))
    DB_PATH = "UserDatabase.db"
    COMMANDS = ("/start", "/help", "/low", "/high", "/custom", "/history")
    DESCRIPTION_COMMANDS = (
        "/start............начало диалога с ботом\n"
        "/help.............информация по кнопкам и командам\n"
        "/high.............вывод лучших показателей\n"
        "/low...............вывод худших показателей\n"
        "/custom.......вывод показателей пользовательского диапазона\n"
        "/history........вывод истории запросов"
    )
    DICT_SORT_API_HOSTEL = {
        "Сортировка по ценам": "PRICE_LOW_TO_HIGH",
        "Сортировка по оценкам проживающих": "REVIEW",
        "Сортировка по расстоянию до центра": "DISTANCE",
        "Сортировка по звездности отелей": "PROPERTY_CLASS",
    }
    DICT_MOUNT_STR_INT = {
        "Январь": 1, "Февраль": 2, "Март": 3, "Апрель": 4,
        "Май": 5, "Июнь": 6, "Июль": 7, "Август": 8,
        "Сентябрь": 9, "Октябрь": 10, "Ноябрь": 11, "Декабрь": 12
    }
    DICT_FILTERS_API_HOSTEL = {
        "Фильтр по ценам": "price",
        "Фильтр по названию отеля": "hotelName",
        "Фильтр по оценкам проживающих": "guestRating",
        "Фильтр по специальным услугам": "accessibility",
        "Фильтр по причине визита": "travelerType",
        "Фильтр по питанию": "mealPlan",
        "Фильтр по типу размещения": "lodging",
        "Фильтр по услугам": "amenities",
        "Фильтр по звездности отелей": "star",
        "Фильтр по услугам оплаты": "paymentType",
        "Фильтр по количеству комнат в номере": "bedroomFilter",
        "Фильтр по свободным номерам на нужные даты": "availableFilter"
    }
    DICT_GUEST_RATING = {
        "Минимальная оценка 7": "35",
        "Минимальная оценка 8": "40",
        "Минимальная оценка 9": "45"
    }
    DICT_ACCESSIBILITY = {
        "Сурдопереводчик": "SIGN_LANGUAGE_INTERPRETER",
        "Лесница для инвалидов": "STAIR_FREE_PATH",
        "Сервис для животных": "SERVICE_ANIMAL",
        "Лифт": "ELEVATOR",
        "Комната для инвалидов": "IN_ROOM_ACCESSIBLE",
        "Душевая кабина в уровень пола": "ROLL_IN_SHOWER",
        "Душевая кабина для инвалидов": "ACCESSIBLE_BATHROOM",
        "Парковка для инвалидов": "ACCESSIBLE_PARKING"
    }
    DICT_TRAVELER_TYPE = {
        "По работе": "BUSINESS",
        "По семейным обстоятельствам": "FAMILY",
    }
    DICT_MEAL_PLAN = {
        "Бесплатный завтрак": "FREE_BREAKFAST",
        "Полупансион": "HALF_BOARD",
        "Полный пансион": "FULL_BOARD",
        "Всё включено": "ALL_INCLUSIVE"
    }
    DICT_LODGING = {
        "Вилла": "VILLA",
        "Апартаменты": "CONDO_RESORT",
        "Пансион": "PENSION",
        "Таунхаус": "TOWNHOUSE",
        "Агротуризм": "AGRITOURISM",
        "Отель": "HOTEL_RESORT",
        "Коттеджный поселок": "HOLIDAY_PARK",
        "Квартира": "CONDO"
    }
    DICT_AMENITIES = {
        "Бесплатный транспорт в аэропорт": "FREE_AIRPORT_TRANSPORTATIO",
        "Вид на океан": "OCEAN_VIEW",
        "Джакузи": "HOT_TUB",
        "Домашние животные": "PETS",
        "Казино": "CASINO",
        "Спа": "SPA_ON_SITE",
        "Детская кроватка": "CRIB",
        "Балкон или терраса": "BALCONY_OR_TERRACE",
        "Стоянка": "PARKING",
        "Электромобиль": "ELECTRIC_CAR",
        "Ресторан в отеле": "RESTAURANT_IN_HOTEL",
        "Кухня": "KITCHEN_KITCHENETTE",
        "Спортзал": "GYM",
        "Бассейн": "POOL",
        "Стиральная машина и сушилка": "WASHER_DRYER",
        "Аквапарк": "WATER_PARK",
        "Кондиционер": "AIR_CONDITIONING",
        "Wi-fi": "WIFI"
    }
    DICT_STARS = {
        "1": "10",
        "2": "20",
        "3": "30",
        "4": "40",
        "5": "50",
    }
    DICT_PAYMENT_TYPE = {
        "Бесплатное аннулирование": "FREE_CANCELLATION",
        "Оплата при заселении": "PAY_LATER",
    }
    DICT_BEDROOM_FILTER = {
        "Студия": "0",
        "Одна комната": "1",
        "Две комната": "2",
        "Три комната": "3",
        "Четыре комната": "4",
    }
