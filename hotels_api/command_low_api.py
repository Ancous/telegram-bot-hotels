"""
Модуль работы с API сайта при команде low
"""

from hotels_api import RequrestsApi


class LowApi:
    """
    Класс подбирает отели с худшими параметрами по заданной сортировке

    Attributes:
    info_hotels_list (list): список с информацией по отобранным отелям
    response (dict): ответ по запросу к API
    quantity_hotels (int): количество выводимых результатов

    Methods:
    low_result: делает запрос к API и распределяет выполнение работы по другим методам в зависимости от сортировки
    low_price_low_to_high: выполняет подбор отелей, и записывает информацию по ним если сортировка по цене
    low_review: выполняет подбор отелей, и записывает информацию по ним если сортировка по рейтингу
    low_distance: выполняет подбор отелей, и записывает информацию по ним если сортировка по расстоянию от центра
    low_star: выполняет подбор отелей, и записывает информацию по ним если сортировка по звездности отеля
    """
    info_hotels_list = list()
    response = dict()
    quantity_hotels = 0

    @classmethod
    def low_result(cls: object, dict_result: dict) -> list:
        """
        Делает запрос к API и распределяет выполнение работы по другим методам класса в зависимости от сортировки

        Parameters:
        dict_result (dict): словарь с данными для поиска подходящих результатов с сайта Hotels.com

        Returns:
        list: список отсортированных отелей с параметрами
        """
        cls.info_hotels_list = list()
        cls.response = dict()
        cls.quantity_hotels = 0
        step_index = 0
        count_list = 0
        while True:
            count_list += 1
            size_response = RequrestsApi.post_options_filters(
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
            )["result"]["data"]["propertySearch"]["properties"]
            step_index += 200
            if len(size_response) == 0 or len(size_response) < 200:
                if len(size_response) < int(dict_result["count"]):
                    count_list -= 1
                break
        size_index = 200 * count_list - 200
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
            results_starting_index=size_index,
            currency="USD",
            eap_id=1,
            locale="en_US",
            site_id=300000001,
            available_filter="SHOW_AVAILABLE_ONLY"
        )["result"]
        cls.quantity_hotels = int(dict_result["count"])
        if int(dict_result["count"]) >= len(cls.response["data"]["propertySearch"]["properties"]):
            cls.quantity_hotels = len(cls.response["data"]["propertySearch"]["properties"])
        if dict_result["sort"] == "PRICE_LOW_TO_HIGH":
            cls.low_price_low_to_high()
        elif dict_result["sort"] == "REVIEW":
            cls.low_reviews()
        elif dict_result["sort"] == "DISTANCE":
            cls.low_distance()
        else:
            cls.low_star()

        return cls.info_hotels_list

    @classmethod
    def low_price_low_to_high(cls: object) -> None:
        """
        Выполняет подбор отелей и записывает информацию по ним если сортировка по цене

        Parameters:
        None

        Returns:
        None
        """
        sorted_response = sorted(
            cls.response["data"]["propertySearch"]["properties"],
            key=lambda d: d['price']['lead']['amount'],
            reverse=True
        )
        for count_hotel in range(cls.quantity_hotels):
            hotel_id = sorted_response[count_hotel]["id"]
            price = round(sorted_response[count_hotel]['price']['lead']['amount'], 1)
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
                cls.info_hotels_list[count_hotel][f"photo_{photo}"] = response_2["data"]["propertyInfo"][
                    "propertyGallery"]["images"][photo]["image"]["url"]
                number_photo += 1
            cls.info_hotels_list[count_hotel]["number_photo"] = number_photo

    @classmethod
    def low_reviews(cls: object) -> None:
        """
        Выполняет подбор отелей и записывает информацию по ним если сортировка по рейтингу

        Parameters:
        None

        Returns:
        None
        """
        sorted_response = sorted(
            cls.response["data"]["propertySearch"]["properties"],
            key=lambda d: d['reviews']['score']
        )
        for count_hotel in range(cls.quantity_hotels):
            hotel_id = sorted_response[count_hotel]["id"]
            reviews = float(sorted_response[count_hotel]['reviews']['score'])
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
                cls.info_hotels_list[count_hotel][f"photo_{photo}"] = response_2["data"]["propertyInfo"][
                    "propertyGallery"]["images"][photo]["image"]["url"]
                number_photo += 1
            cls.info_hotels_list[count_hotel]["number_photo"] = number_photo

    @classmethod
    def low_distance(cls: object) -> None:
        """
        Выполняет подбор отелей и записывает информацию по ним если сортировка по расстоянию от центра

        Parameters:
        None

        Returns:
        None
        """
        sorted_response = sorted(
            cls.response["data"]["propertySearch"]["properties"],
            key=lambda d: d['destinationInfo']['distanceFromDestination']["value"],
            reverse=True
        )
        for count_hotel in range(cls.quantity_hotels):
            hotel_id = sorted_response[count_hotel]["id"]
            distance = sorted_response[count_hotel]['destinationInfo']['distanceFromDestination']['value']
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
                cls.info_hotels_list[count_hotel][f"photo_{photo}"] = response_2["data"]["propertyInfo"][
                    "propertyGallery"]["images"][photo]["image"]["url"]
                number_photo += 1
            cls.info_hotels_list[count_hotel]["number_photo"] = number_photo

    @classmethod
    def low_star(cls: object) -> None:
        """
        Выполняет подбор отелей и записывает информацию по ним если сортировка по звездности отеля

        Parameters:
        None

        Returns:
        None
        """
        for info_hotel in cls.response["data"]["propertySearch"]["properties"]:
            if not isinstance(info_hotel["star"], (int, float)):
                info_hotel["star"] = 0
        sorted_response = sorted(
            cls.response["data"]["propertySearch"]["properties"],
            key=lambda d: d['star']
        )
        for count_hotel in range(cls.quantity_hotels):
            hotel_id = sorted_response[count_hotel]["id"]
            star = float(sorted_response[count_hotel]['star'])
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
                cls.info_hotels_list[count_hotel][f"photo_{photo}"] = response_2["data"]["propertyInfo"][
                    "propertyGallery"]["images"][photo]["image"]["url"]
                number_photo += 1
            cls.info_hotels_list[count_hotel]["number_photo"] = number_photo
