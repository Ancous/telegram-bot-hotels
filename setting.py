import os
import time
from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr


load_dotenv()

class SiteSetting(BaseSettings):
    TOKEN: SecretStr = os.getenv("TOKEN", None)


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


if __name__ in "__main__":
    SiteSetting()
    Time()
