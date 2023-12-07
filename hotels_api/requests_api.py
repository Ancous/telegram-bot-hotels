import json
import os
import requests

from dotenv import load_dotenv


load_dotenv()

class RequrestsApi:

    rapidapi_key = os.getenv("RAPIDAPI_KEY_HOTELS")
    rapidapi_host = os.getenv("RAPIDAPI_HOST_HOTELS")

    @classmethod
    def get_locations_suggestions(cls: object,
                                  city: str,
                                  language_code: str = None,
                                  lang_id: int = None,
                                  site_id: int = None) -> dict:
        """
        Запрос:
        Получить похожие места и предложения

        Полный url:
        "https://hotels4.p.rapidapi.com/locations/v3/search"

        Параметры:
        - city="q" (str): название стран, городов, районов, мест и т.д. ("new york", "dubai", "moscow", ...)
        - language_code="locale" (str): код языка  ("en_US", "en-GB", "hu_HU", ...)
        - lang_id="langid" (int): ...  (3001, 1007, 207, ...)
        - site_id"siteid" (int): ...  (3000007, 7504000, 6500444, ...)

        Комментарии:
        - "langid" можно получит из словаря по url "https://hotels4.p.rapidapi.com/v2/get-meta-data"  путь: ["US"]["supportedLocales"][0]["languageIdentifier"]
        - "siteid" можно получит из словаря по url "https://hotels4.p.rapidapi.com/v2/get-meta-data"  путь: ["US"]["siteId"]

        Ответ:
        - смотреть json файл "answer.json"
        """
        # -------------------------------------------------------------------------
        base_url = "https://hotels4.p.rapidapi.com"
        end_point = "/locations/v3/search"
        rapidapi_key = cls.rapidapi_key
        rapidapi_host = cls.rapidapi_host
        parameters = {
            "q": city,
            "locale": language_code,
            "langid": lang_id,
            "siteid": site_id
        }
        # -------------------------------------------------------------------------

        complete_request = base_url + end_point
        complete_parameters = parameters
        headers = {
            "X-RapidAPI-Key": rapidapi_key,
            "X-RapidAPI-Host": rapidapi_host
        }

        response = requests.get(url=complete_request, params=complete_parameters,  headers=headers)
        result = json.loads(response.text)

        if response.status_code == 200:
            return {"status_code": response.status_code, "headers": response.headers, "result": result}
        else:
            return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}

    @classmethod
    def post_options_filters(cls: object,
                             region_id: str,
                             check_in_day: int,
                             check_in_month: int,
                             check_in_year: int,
                             check_out_day: int,
                             check_out_month: int,
                             check_out_year: int,
                             adults: list[int, ...],
                             children_age: list[list[int], ...] = None,
                             hotel_name: str = None,
                             guest_rating: str = None,
                             accessibility: list[str, ...] = None,
                             traveler_type: list[str, ...] = None,
                             meal_plan: list[str, ...] = None,
                             poi: str = None,
                             region_id_filters: str = None,
                             lodging: list[str, ...] = None,
                             amenities: list[str, ...] = None,
                             stars: list[str, ...] = None,
                             payment_type: list[str, ...] = None,
                             bedroom_filter: list[str, ...] = None,
                             available_filter:str = None,
                             price_max: int = None,
                             price_min: int = None,
                             sort: str = None,
                             results_size: int = None,
                             results_starting_index: int = None,
                             latitude: int = None,
                             longitude: int = None,
                             locale: str = None,
                             site_id: int = None,
                             eap_id: int = None,
                             currency: str = None) -> dict:
        """
        Запрос:
        Список свойств с опциями и фильтрами

        Полный url:
        "https://hotels4.p.rapidapi.com/properties/v2/list"

        Параметры:
        region_id="regionId" (str): числовой идентификатор региона (23321, 321, 7567, ...)
        check_in_day="checkInDate""day" (int): день заезда  (2, 28, 15, ...)
        check_in_month="checkInDate""month" (int): месяц заезда  (2, 11, 9, ...)
        check_in_year="checkInDate""year" (int): год заезда  (2024, 2025, 2023, ...)
        check_out_day="checkOutDate""day" (int): день выезда  (2, 28, 15, ...)
        check_out_month="checkOutDate""month" (int): месяц выезда  (2, 11, 9, ...)
        check_out_year="checkOutDate""year" (int): день выезда  (2, 28, 15, ...)
        adults="adults" (tuple[int, ...]): количество взрослых  ((2,), (1, 4), (2, 1, 1), ...)
        children_age="age" (list[tuple[int], ...]): возраст детей  ([(1,), (2, 4)], [(3, 4, 7)], [(5, 2), (1, 2)], ...)
        hotel_name="hotelName" (str): название отеля  ("New York New York Hotel & Casino", "Plaza", ...)
        guest_rating="guestRating" (str): минимальный рейтинг гостя  ("15", "45", "30", ...)
        accessibility="accessibility" (list[str, ...]): предоставляемые услуги (["SIGN_LANGUAGE_INTERPRETER", ...], ["ELEVATOR", ...], ["IN_ROOM_ACCESSIBLE", ...], ...)
        traveler_type="travelerType" (list[str, ...]): причина визита  (["BUSINESS", ...], ["FAMILY", "BUSINESS", ...], ["LGBT", "BUSINESS", "FAMILY" ...])
        meal_plan="mealPlan" (list[str, ...]): питание (["FULL_BOARD", ...], ["HALF_BOARD", "FULL_BOARD", ...], ["ALL_INCLUSIVE", "FULL_BOARD", "HALF_BOARD", ...], ...)
        poi="poi" (str): координаты для поиска точек интересы ("42.223031,190.247187:51844", "12.223031,109.247187:7545844", "11.223031,117.247187:5844", ...)
        region_id_filters:"region_id" str: ...  (...)
        lodging="lodging" (list[str, ...]): тип размещения  (["VILLA", ...], ["PENSION", "VILLA", ...], ["HOTEL_RESORT", "VILLA", "PENSION", ...], ...)
        amenities="amenities" (list[str, ...]):  удобства  (["WIFI", ...], ["HOT_TUB", "WIFI"...], ["PARKING", "WIFI", "HOT_TUB", ...], ...)
        stars="star" (list[str, ...]): звёздность отеля  (["30", ...], ["10", "30", ...], ["50", "10", "50", ...], ...)
        payment_type="paymentType": вид оплаты  ("FREE_CANCELLATION", "PAY_LATER")
        bedroom_filter="bedroomFilter" list[str, ...]:  количество комнат  ("2", "0", "4", ...)
        available_filter="availableFilter": свободность (None, "SHOW_AVAILABLE_ONLY")
        price_max="max" (int)": максимальная цена отбора (200, 250, 500, ...)
        price_min="min" (int)": минимальная цена отбора (50, 25, 10, ...)
        sort="sort" (str): сортировка ответа варианты: ("PRICE_RELEVANT", "REVIEW", "DISTANCE", "PRICE_LOW_TO_HIGH", "PROPERTY_CLASS", "RECOMMENDED")
        results_size="resultsSize" (int): количество выводимых результатов  (50, 100, 150, ...)
        results_starting_index="resultsStartingIndex" (int): ... (1, 8, 15, ...)
        locale="locale" (str): код языка ("en_US", "en-GB", "hu_HU", ...)
        site_id="siteId" (int): ...  (3000007, 7504000, 6500444, ...)
        eap_id="eapid" (int): ... (1, 28, 40, ...)
        currency="currency" (str): валюта ("USD", "EUR", "GBP", ...)

        Комментарии:
        - "regionId" можно получит из словаря по url "https://hotels4.p.rapidapi.com/locations/v3/search "  путь: ["sr"]["gaiaId"]
        - "eapid" можно получит из словаря по url "https://hotels4.p.rapidapi.com/v2/get-meta-data"  путь: ["US"]["EAPID"]
        - "siteId" можно получит из словаря по url "https://hotels4.p.rapidapi.com/v2/get-meta-data"  путь: ["US"]["siteId"]
        - "age" может отсутствовать если ребенок не указывается
        - возможные варианты записи sort:  ["PRICE_RELEVANT" (цена и рекомендации сайта), "REVIEW" (оценка гостей), "DISTANCE" (расстояние до центра), "PRICE_LOW_TO_HIGH" (цена от меньшего к большему), "PROPERTY_CLASS" (количество звезд), "RECOMMENDED" (рекомендации сайта)]
        - возможные варианты записи accessibility: ["SIGN_LANGUAGE_INTERPRETER" (сурдопереводчик), "STAIR_FREE_PATH" (...), "SERVICE_ANIMAL" (сервис для животных), "ELEVATOR" (лифт), "IN_ROOM_ACCESSIBLE (большие комнаты)", "ROLL_IN_SHOWER (...)", "ACCESSIBLE_BATHROOM" (комфортный душ), "ACCESSIBLE_PARKING" (парковка)]
        - возможные варианты записи traveler_type: ["BUSINESS" (бизнес), "FAMILY" (семейный), "LGBT" (ЛГБТ)]
        - возможные варианты записи meal_plan: ["FREE_BREAKFAST" (бесплатный завтрак), "HALF_BOARD" (полупансион), "FULL_BOARD" (полный пансион), "ALL_INCLUSIVE" (всё включено)]
        - возможные варианты записи lodging: ["VILLA" (вилла), "CONDO_RESORT" (апартаменты), "PENSION" (пансион), "TOWNHOUSE" (таунхаус), "AGRITOURISM" (агротуризм), "HOTEL_RESORT" (отель), "HOLIDAY_PARK" (коттеджный поселок), "CONDO" (квартира)]
        - возможные варианты записи amenities: ["FREE_AIRPORT_TRANSPORTATIO" (бесплатный транспорт в аэропорт), "OCEAN_VIEW" (вид на океан), "HOT_TUB" (джакузи), "PETS" (домашние животные), "CASINO" (казино), "SPA_ON_SITE" (спа), "CRIB" (детская кроватка), "BALCONY_OR_TERRACE" (балкон или терраса), "PARKING" (стоянка), "ELECTRIC_CAR" (электромобиль), "RESTAURANT_IN_HOTEL" (ресторан в отеле), "KITCHEN_KITCHENETTE" (кухня), "GYM" (спортзал), "POOL" (бассейн), "WASHER_DRYER" (стиральная машина и сушилка), "WATER_PARK" (аквапарк), "AIR_CONDITIONING" (кондиционер), "WIFI" (wi-fi)]
        - возможные варианты записи stars: ["10" (1-звезда у отеля), "20" (2-звезды у отеля), "30" (3-звезды у отеля), "40" (4-звезды у отеля), "50" (5-звезд у отеля)]
        - возможные варианты записи payment_type: ["FREE_CANCELLATION" (бесплатная отмена), "PAY_LATER" (оплата по заселению)]
        - возможные варианты записи payment_type: : ["0" (студия), "1" (одна комната), "2" (две комнаты), "3" (три комнаты), "4" (четыре комнаты)]
        - возможные варианты записи available_filter: ["SHOW_AVAILABLE_ONLY" (только доступные)]
        - price_max и price_min указывается в валюте "currency"
        - poi указывается в формате "latitude,longitude:regionId"

        Ответ:
        - смотреть json файл "answer.json"
        """
        # -------------------------------------------------------------------------
        base_url = "https://hotels4.p.rapidapi.com"
        end_point = "/properties/v2/list"
        rapidapi_key = cls.rapidapi_key
        rapidapi_host = cls.rapidapi_host
        payload = {
            "destination": {
                "regionId": region_id,
                "coordinates": {
                    "latitude": latitude,
                    "longitude": longitude
                },
            },
            "checkInDate": {
                "day": check_in_day,
                "month": check_in_month,
                "year": check_in_year
            },
            "checkOutDate": {
                "day": check_out_day,
                "month": check_out_month,
                "year": check_out_year
            },
            "filters": {
                "price": {
                    "max": price_max,
                    "min": price_min
                },
                "hotelName": hotel_name,
                "guestRating": guest_rating,
                "accessibility": accessibility,
                "travelerType": traveler_type,
                "mealPlan": meal_plan,
                "poi": poi,
                "regionId": region_id_filters,
                "lodging": lodging,
                "amenities": amenities,
                "star": stars,
                "paymentType": payment_type,
                "bedroomFilter": bedroom_filter,
                "availableFilter": available_filter
            },
            "sort": sort,
            "resultsSize": results_size,
            "resultsStartingIndex": results_starting_index,
            "eapid": eap_id,
            "currency": currency,
        }
        # -------------------------------------------------------------------------

        if adults:
            payload["rooms"] = [{"adults": adults[count_rooms], "children": []} for count_rooms in range(len(adults))]

        if children_age:
            for count in range(len(children_age)):
                payload["rooms"][count]["children"] = [{"age": age} for age in children_age[count]]

        if locale:
            payload["locale"] = locale

        if site_id:
            payload["siteId"] = site_id

        complete_request = base_url + end_point
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": rapidapi_key,
            "X-RapidAPI-Host": rapidapi_host
        }

        response = requests.post(url=complete_request, json=payload, headers=headers)
        result = json.loads(response.text)

        if response.status_code == 200:
            return {"status_code": response.status_code, "headers": response.headers, "result": result}
        else:
            return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}

    @classmethod
    def post_full_information_property(cls: object,
                                       property_id: str,
                                       locale: str = None,
                                       site_id: int = None,
                                       eap_id: int = None,
                                       currency: str = None) -> dict:
        """
        Запрос:
        Получить подробную информацию об объекте

        Полный url:
        "https://hotels4.p.rapidapi.com/properties/v2/detail"

        Параметры:
        property_id="propertyId" (str): ...  ("123584", "78845", "45648654", ...)
        locale="locale" (str): код языка ("en_US", "en-GB", "hu_HU", ...)
        site_id="siteId" (int): ...  (3000007, 7504000, 6500444, ...)
        eap_id="eapid" (int): ... (1, 28, 40, ...)
        currency="currency" (str): валюта ("USD", "EUR", "GBP", ...)

        Комментарии:
        - "propertyId" можно получит из словаря по url "https://hotels4.p.rapidapi.com/properties/v2/list"  путь: ["data"]["propertySearch"]["properties"][0]["id"]
        - "siteid" можно получит из словаря по url "https://hotels4.p.rapidapi.com/v2/get-meta-data"  путь: ["US"]["siteId"]
        - "eapid" можно получит из словаря по url "https://hotels4.p.rapidapi.com/v2/get-meta-data"  путь: ["US"]["EAPID"]

        Ответ:
        - смотреть json файл "answer.json"
        """
        # -------------------------------------------------------------------------
        base_url = "https://hotels4.p.rapidapi.com"
        end_point = "/properties/v2/detail"
        rapidapi_key = cls.rapidapi_key
        rapidapi_host = cls.rapidapi_host
        payload = {
            "currency": currency,
            "eapid": eap_id,
            "propertyId": property_id
        }
        # -------------------------------------------------------------------------

        if site_id:
            payload["siteId"] = site_id

        if locale:
            payload["locale"] = locale

        complete_request = base_url + end_point
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": rapidapi_key,
            "X-RapidAPI-Host": rapidapi_host
        }

        response = requests.post(url=complete_request, json=payload, headers=headers)
        result = json.loads(response.text)

        if response.status_code == 200:
            return {"status_code": response.status_code, "headers": response.headers, "result": result}
        else:
            return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}
