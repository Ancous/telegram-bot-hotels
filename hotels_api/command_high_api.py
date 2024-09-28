"""
Модуль работы с API сайта при команде high
"""

from hotels_api import RequrestsApi


class HighApi:
    """
    Класс подбирает отели с лучшими параметрами по заданной сортировке

    Attributes:
    info_hotels_list (list): список с информацией по отобранным отелям
    response (dict): ответ по запросу к API
    quantity_hotels (int): количество выводимых результатов

    Methods:
    high_result: делает запрос к API и распределяет выполнение работы по другим методам в зависимости от сортировки
    high_price_low_to_high: выполняет подбор отелей, и записывает информацию по ним если сортировка по цене
    high_review: выполняет подбор отелей, и записывает информацию по ним если сортировка по рейтингу
    high_distance: выполняет подбор отелей, и записывает информацию по ним если сортировка по расстоянию от центра
    high_star: выполняет подбор отелей, и записывает информацию по ним если сортировка по звездности отеля
    """
    info_hotels_list = list()
    response = dict()
    quantity_hotels = 0

    @classmethod
    def high_result(cls, dict_result: dict) -> list:
        """
        Делает запрос к API и распределяет выполнение работы по другим методам класса в зависимости от сортировки

        Arguments:
        dict_result (dict): словарь с данными для поиска подходящих результатов с сайта Hotels.com

        Returns:
        list: список отсортированных отелей с параметрами
        """
        cls.info_hotels_list = list()
        cls.response = dict()
        cls.quantity_hotels = 0
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
            cls.high_price_low_to_high()
        elif dict_result["sort"] == "REVIEW":
            cls.high_review()
        elif dict_result["sort"] == "DISTANCE":
            cls.high_distance()
        else:
            cls.high_star()

        return cls.info_hotels_list

    @classmethod
    def high_price_low_to_high(cls) -> None:
        """
        Выполняет подбор отелей и записывает информацию по ним если сортировка по цене

        Parameters:
        None

        Returns:
        None
        """
        for count_hotel in range(cls.quantity_hotels):
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
                cls.info_hotels_list[count_hotel][f"photo_{photo}"] = response_2["data"]["propertyInfo"][
                    "propertyGallery"]["images"][photo]["image"]["url"]
                number_photo += 1
            cls.info_hotels_list[count_hotel]["number_photo"] = number_photo

    @classmethod
    def high_review(cls) -> None:
        """
        Выполняет подбор отелей и записывает информацию по ним если сортировка по рейтингу

        Parameters:
        None

        Returns:
        None
        """
        for count_hotel in range(cls.quantity_hotels):
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
                cls.info_hotels_list[count_hotel][f"photo_{photo}"] = response_2["data"]["propertyInfo"][
                    "propertyGallery"]["images"][photo]["image"]["url"]
                number_photo += 1
            cls.info_hotels_list[count_hotel]["number_photo"] = number_photo

    @classmethod
    def high_distance(cls) -> None:
        """
        Выполняет подбор отелей и записывает информацию по ним если сортировка по расстоянию от центра

        Parameters:
        None

        Returns:
        None
        """
        for count_hotel in range(cls.quantity_hotels):
            hotel_id = cls.response["data"]["propertySearch"]["properties"][count_hotel]["id"]
            distance = cls.response['data']['propertySearch']['properties'][count_hotel][
                'destinationInfo']['distanceFromDestination']['value']
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
    def high_star(cls) -> None:
        """
        Выполняет подбор отелей и записывает информацию по ним если сортировка по звездности отеля

        Parameters:
        None

        Returns:
        None
        """
        for count_hotel in range(cls.quantity_hotels):
            if not isinstance(cls.response["data"]["propertySearch"]["properties"][count_hotel]["star"], (int, float)):
                cls.response["data"]["propertySearch"]["properties"][count_hotel]["star"] = 0
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
                cls.info_hotels_list[count_hotel][f"photo_{photo}"] = response_2["data"]["propertyInfo"][
                    "propertyGallery"]["images"][photo]["image"]["url"]
                number_photo += 1
            cls.info_hotels_list[count_hotel]["number_photo"] = number_photo
