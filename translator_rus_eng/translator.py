"""
Модуль определения языка ввода пользователя и перевода на английский язык
"""

import os
import requests

from dotenv import load_dotenv

load_dotenv()

rapidapi_key = os.getenv("RAPIDAPI_KEY_TRANSLATOR")
rapidapi_host = os.getenv("RAPIDAPI_HOST_TRANSLATOR")


def writing_language(word_s: str) -> str:
    """
    Определяет язык входящего слова для перевода

    Parameters:
    word_s (str): слово для определения языка

    Returns:
    str: язык с которого надо перевести
    """
    url_writing_language = "https://google-translate1.p.rapidapi.com/language/translate/v2/detect"
    payload = {
        "q": word_s
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": rapidapi_host
    }
    response = requests.post(url=url_writing_language, data=payload, headers=headers)
    return response.json()["data"]["detections"][0][0]["language"]


def translator(word_s: str) -> str:
    """
    Переводит входящее слово на английский язык

    Parameters:
    word_s (str): слово для перевода

    Returns:
    str: переведенное слово
    """
    url_translator = "https://google-translate1.p.rapidapi.com/language/translate/v2"
    language = writing_language(word_s)
    if language == "en":
        return word_s
    payload_1 = {
        "q": word_s,
        "target": "en",
        "source": language
    }
    headers_1 = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": rapidapi_host
    }
    response_1 = requests.post(url=url_translator, data=payload_1, headers=headers_1)
    return response_1.json()["data"]["translations"][0]["translatedText"]
