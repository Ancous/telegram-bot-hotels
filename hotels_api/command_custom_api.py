"""
Модуль работы с API сайта при команде custom
"""

from hotels_api import RequrestsApi


class CustomApi:
    """
    Класс подбирает отели пользовательского диапазона по заданной сортировке

    Attributes:
    info_hotels_list (list): список с информацией по отобранным отелям
    response (dict): ответ по запросу к API
    full_list_hotels (int): количество записанных результатов в info_hotels_list

    Methods:
    custom_result: делает запрос к API и распределяет выполнение работы по другим методам в зависимости от сортировки
    custom_price_low_to_high: выполняет подбор отелей, и записывает информацию по ним если сортировка по цене
    custom_review: выполняет подбор отелей, и записывает информацию по ним если сортировка по рейтингу
    custom_distance: выполняет подбор отелей, и записывает информацию по ним если сортировка по расстоянию от центра
    custom_star: выполняет подбор отелей, и записывает информацию по ним если сортировка по звездности отеля
    """
    info_hotels_list = list()
    response = dict()
    full_list_hotels = 0

    @classmethod
    def custom_result(cls: object, dict_result: dict) -> list:
        """
        Делает запрос к API и распределяет выполнение работы по другим методам класса в зависимости от сортировки

        Parameters:
        dict_result (dict): словарь с данными для поиска подходящих результатов с сайта Hotels.com

        Returns:
        list: список отсортированных отелей с параметрами
        """
        cls.info_hotels_list = list()
        cls.response = dict()
        cls.full_list_hotels = 0
        step_index = 0
        while True:
            cls.response = RequrestsApi.post_options_filters(
                region_id=dict_result["city_id"],
                check_in_day=dict_result["arrival_day"],
                check_in_month=dict_result["arrival_month"],
                check_in_year=dict_result["arrival_year"],
                check_out_day=dict_result["departure_day"],
                check_out_month=dict_result["departure_month"],
                check_out_year=dict_result["departure_year"],
                adults=dict_result["adults"],
                children_age=dict_result["children_age"],
                sort=dict_result["sort"],
                results_size=200,
                results_starting_index=step_index,
                currency="USD",
                eap_id=1,
                locale="en_US",
                site_id=300000001,
                available_filter="SHOW_AVAILABLE_ONLY"
            )["result"]
            step_index += 200
            if len(cls.response["data"]["propertySearch"]["properties"]) == 0:
                return cls.info_hotels_list
            if (dict_result["sort"] == "PRICE_LOW_TO_HIGH" and
                    cls.response["data"]["propertySearch"]["properties"][-1][
                        "price"]["lead"]["amount"] > dict_result["range_max"]):
                cls.custom_price_low_to_high(dict_result=dict_result)
                break
            elif (dict_result["sort"] == "REVIEW" and
                  cls.response["data"]["propertySearch"]["properties"][-1][
                      "reviews"]["score"] < dict_result["range_min"]):
                cls.custom_reviews(dict_result=dict_result)
                break
            elif (dict_result["sort"] == "DISTANCE" and
                  cls.response["data"]["propertySearch"]["properties"][-1][
                      "destinationInfo"]["distanceFromDestination"]["value"] > dict_result["range_max"]):
                cls.custom_distance(dict_result=dict_result)
                break
            elif (dict_result["sort"] == "PROPERTY_CLASS" and
                  cls.response["data"]["propertySearch"]["properties"][-1][
                      "star"] < dict_result["range_min"]):
                cls.custom_star(dict_result=dict_result)
                break

        return cls.info_hotels_list

    @classmethod
    def custom_price_low_to_high(cls: object, dict_result: dict) -> None:
        """
        Выполняет подбор отелей и записывает информацию по ним если сортировка по цене

        Parameters:
        dict_result (dict): словарь с данными для поиска подходящих результатов с сайта Hotels.com

        Returns:
        None
        """
        for count_hotel in range(len(cls.response["data"]["propertySearch"]["properties"])):
            if (dict_result["range_min"] <=
                    cls.response["data"]["propertySearch"]["properties"][count_hotel]['price']['lead']['amount'] <=
                    dict_result["range_max"]):
                hotel_id = cls.response["data"]["propertySearch"]["properties"][count_hotel]["id"]
                price = round(
                    cls.response['data']['propertySearch']['properties'][count_hotel]['price']['lead']['amount'],
                    1
                )
                response_2 = RequrestsApi.post_full_information_property(
                    property_id=hotel_id
                )["result"]
                cls.info_hotels_list.append(
                    {
                        "name_hotels": f"Название отеля: {response_2['data']['propertyInfo']['summary']['name']}",
                        "sort_element": f"Цена за одни сутки: {price} USD",
                        "url": f"Ссылка отеля на сайте Hotels: https://www.hotels.com/h{hotel_id}.Hotel-Information"
                    }
                )
                count_photo = 3
                number_photo = 0
                if len(response_2["data"]["propertyInfo"]["propertyGallery"]["images"]) < 3:
                    count_photo = len(response_2["data"]["propertyInfo"]["propertyGallery"]["images"])
                for photo in range(count_photo):
                    cls.info_hotels_list[cls.full_list_hotels][f"photo_{photo}"] = response_2["data"]["propertyInfo"][
                        "propertyGallery"]["images"][photo]["image"]["url"]
                    number_photo += 1
                cls.info_hotels_list[cls.full_list_hotels]["number_photo"] = number_photo
                cls.full_list_hotels += 1
            if cls.full_list_hotels >= int(dict_result["count"]):
                break

    @classmethod
    def custom_reviews(cls: object, dict_result: dict) -> None:
        """
        Выполняет подбор отелей и записывает информацию по ним если сортировка по рейтингу

        Parameters:
        dict_result (dict): словарь с данными для поиска подходящих результатов с сайта Hotels.com

        Returns:
        None
        """
        for count_hotel in range(len(cls.response["data"]["propertySearch"]["properties"])):
            if (dict_result["range_min"] <=
                    cls.response['data']['propertySearch']['properties'][count_hotel]['reviews']['score'] <=
                    dict_result["range_max"]):
                hotel_id = cls.response["data"]["propertySearch"]["properties"][count_hotel]["id"]
                reviews = float(cls.response['data']['propertySearch']['properties'][count_hotel]['reviews']['score'])
                response_2 = RequrestsApi.post_full_information_property(
                    property_id=hotel_id
                )["result"]
                cls.info_hotels_list.append(
                    {
                        "name_hotels": f"Название отеля: {response_2['data']['propertyInfo']['summary']['name']}",
                        "sort_element": f"Оценка: {reviews}",
                        "url": f"Ссылка отеля на сайте Hotels: https://www.hotels.com/h{hotel_id}.Hotel-Information"
                    }
                )
                count_photo = 3
                number_photo = 0
                if len(response_2["data"]["propertyInfo"]["propertyGallery"]["images"]) < 3:
                    count_photo = len(response_2["data"]["propertyInfo"]["propertyGallery"]["images"])
                for photo in range(count_photo):
                    cls.info_hotels_list[cls.full_list_hotels][f"photo_{photo}"] = response_2["data"]["propertyInfo"][
                        "propertyGallery"]["images"][photo]["image"]["url"]
                    number_photo += 1
                cls.info_hotels_list[cls.full_list_hotels]["number_photo"] = number_photo
                cls.full_list_hotels += 1
            if cls.full_list_hotels >= int(dict_result["count"]):
                break

    @classmethod
    def custom_distance(cls: object, dict_result: dict) -> None:
        """
        Выполняет подбор отелей и записывает информацию по ним если сортировка по расстоянию от центра

        Parameters:
        dict_result (dict): словарь с данными для поиска подходящих результатов с сайта Hotels.com

        Returns:
        None
        """
        for count_hotel in range(len(cls.response["data"]["propertySearch"]["properties"])):
            if (dict_result["range_min"] <=
                    cls.response['data']['propertySearch']['properties'][count_hotel]['destinationInfo'][
                        'distanceFromDestination']['value'] <=
                    dict_result["range_max"]):
                hotel_id = cls.response["data"]["propertySearch"]["properties"][count_hotel]["id"]
                distance = cls.response['data']['propertySearch']['properties'][
                    count_hotel]['destinationInfo']['distanceFromDestination']['value']
                response_2 = RequrestsApi.post_full_information_property(
                    property_id=hotel_id
                )["result"]
                cls.info_hotels_list.append(
                    {
                        "name_hotels": f"Название отеля: {response_2['data']['propertyInfo']['summary']['name']}",
                        "sort_element": f"Расстояние до центра: {distance} км.",
                        "url": f"Ссылка отеля на сайте Hotels: https://www.hotels.com/h{hotel_id}.Hotel-Information"
                    }
                )
                count_photo = 3
                number_photo = 0
                if len(response_2["data"]["propertyInfo"]["propertyGallery"]["images"]) < 3:
                    count_photo = len(response_2["data"]["propertyInfo"]["propertyGallery"]["images"])
                for photo in range(count_photo):
                    cls.info_hotels_list[cls.full_list_hotels][f"photo_{photo}"] = response_2["data"]["propertyInfo"][
                        "propertyGallery"]["images"][photo]["image"]["url"]
                    number_photo += 1
                cls.info_hotels_list[cls.full_list_hotels]["number_photo"] = number_photo
                cls.full_list_hotels += 1
            if cls.full_list_hotels >= int(dict_result["count"]):
                break

    @classmethod
    def custom_star(cls: object, dict_result: dict) -> None:
        """
        Выполняет подбор отелей и записывает информацию по ним если сортировка по звездности отеля

        Parameters:
        dict_result (dict): словарь с данными для поиска подходящих результатов с сайта Hotels.com

        Returns:
        None
        """
        for count_hotel in range(len(cls.response["data"]["propertySearch"]["properties"])):
            if not isinstance(cls.response["data"]["propertySearch"]["properties"][count_hotel]["star"], (int, float)):
                cls.response["data"]["propertySearch"]["properties"][count_hotel]["star"] = 0
            if (dict_result["range_min"] <=
                    cls.response['data']['propertySearch']['properties'][count_hotel]['star'] <=
                    dict_result["range_max"]):
                hotel_id = cls.response["data"]["propertySearch"]["properties"][count_hotel]["id"]
                star = float(cls.response['data']['propertySearch']['properties'][count_hotel]['star'])
                response_2 = RequrestsApi.post_full_information_property(
                    property_id=hotel_id
                )["result"]
                cls.info_hotels_list.append(
                    {
                        "name_hotels": f"Название отеля: {response_2['data']['propertyInfo']['summary']['name']}",
                        "sort_element": f"Количество звезд: {star}",
                        "url": f"Ссылка отеля на сайте Hotels: https://www.hotels.com/h{hotel_id}.Hotel-Information"
                    }
                )
                count_photo = 3
                number_photo = 0
                if len(response_2["data"]["propertyInfo"]["propertyGallery"]["images"]) < 3:
                    count_photo = len(response_2["data"]["propertyInfo"]["propertyGallery"]["images"])
                for photo in range(count_photo):
                    cls.info_hotels_list[cls.full_list_hotels][f"photo_{photo}"] = response_2["data"]["propertyInfo"][
                        "propertyGallery"]["images"][photo]["image"]["url"]
                    number_photo += 1
                cls.info_hotels_list[cls.full_list_hotels]["number_photo"] = number_photo
                cls.full_list_hotels += 1
            if cls.full_list_hotels >= int(dict_result["count"]):
                break
