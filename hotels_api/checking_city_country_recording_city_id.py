"""
Модуль работы с API сайта для поиска города
"""

from hotels_api import RequrestsApi
# from translator_rus_eng import translator


def checking_city_country_recording_city_id(dict_result: dict) -> (bool, int):
    """
    Проверяет наличие id-города по запросу к hostel-api

    Parameters:
    dict_result (dict): словарь с названием страны и города

    Returns:
    bool, int: id города для поиска
    """
    # city = translator(dict_result["city"])
    # country = translator(dict_result["country"])
    city = dict_result["city"]
    country = dict_result["country"]
    id_city = None
    response_1 = RequrestsApi.get_locations_suggestions(
        city=city,
        lang_id=1033,
        site_id=300000001
    )["result"]
    for resp_1 in response_1["sr"]:
        if resp_1["type"] == "CITY" and resp_1["regionNames"]["fullName"].split(", ")[-1].lower() == country.lower():
            id_city = resp_1["gaiaId"]
            break
    if id_city is None:
        return False
    else:
        return id_city
