import time
import os
from pydantic import BaseSettings, SecretStr
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ('hello_world', "Приветствие")
)

class SiteSetting(BaseSettings):
    BOT_TOKEN: SecretStr = os.getenv("BOT_TOKEN", None)

class Time:
    @staticmethod
    def times_day():
        time_now = time.localtime(time.time()).tm_hour
        if 0 <= time_now <= 5:
            return "Good night"
        elif 6 <= time_now <= 11:
            return "Good morning"
        elif 12 <= time_now <= 17:
            return "Good afternoon"
        else:
            return "Good evening"
