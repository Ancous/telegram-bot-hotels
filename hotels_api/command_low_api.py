from hotels_api import RequrestsApi


def low_result(dict_result: dict) -> list:
    """

    """
    info_hotels_list = list()
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
        results_size=50,
        currency="USD",
        eap_id=1,
        locale="en_US",
        site_id=300000001,
        available_filter="SHOW_AVAILABLE_ONLY"
    )["result"]["data"]["propertySearch"]["summary"]["matchedPropertiesSize"]
    size = size_response - int(dict_result["count"])
    response_2 = RequrestsApi.post_options_filters(
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
        results_size=50,
        results_starting_index = size - 25,
        currency="USD",
        eap_id=1,
        locale="en_US",
        site_id=300000001,
        available_filter="SHOW_AVAILABLE_ONLY"
    )["result"]
    if dict_result["sort"] == "PRICE_LOW_TO_HIGH":
        sorted_response_2 = sorted(
            response_2["data"]["propertySearch"]["properties"],
            key=lambda d: d['price']['lead']['amount'],
            reverse=True
        )
        for count_hotel in range(int(dict_result["count"])):
            hotel_id = sorted_response_2[count_hotel]["id"]
            response_3 = RequrestsApi.post_full_information_property(
                property_id=hotel_id
            )["result"]
            info_hotels_list.append(
                {
                    "name_hotels": f"Название отеля: {response_3['data']['propertyInfo']['summary']['name']}",
                    "sort_element": f"Цена за одни сутки: {round(sorted_response_2[count_hotel]['price']['lead']['amount'], 1)} USD",
                    "url": f"Ссылка отеля на сайте Hotels: https://www.hotels.com/h{hotel_id}.Hotel-Information"
                }
            )
            count_photo = 3
            number_photo = 0
            if len(response_3["data"]["propertyInfo"]["propertyGallery"]["images"]) < 3:
                count_photo = len(response_3["data"]["propertyInfo"]["propertyGallery"]["images"])
            for i in range(count_photo):
                info_hotels_list[count_hotel][f"photo_{i}"] = response_3["data"]["propertyInfo"]["propertyGallery"]["images"][i]["image"]["url"]
                number_photo += 1
            info_hotels_list[count_hotel]["number_photo"] = number_photo
    elif dict_result["sort"] == "REVIEW":
        sorted_response_2 = sorted(
            response_2["data"]["propertySearch"]["properties"],
            key=lambda d: d['reviews']['score']
        )
        for count_hotel in range(int(dict_result["count"])):
            hotel_id = sorted_response_2[count_hotel]["id"]
            response_3 = RequrestsApi.post_full_information_property(
                property_id=hotel_id
            )["result"]
            info_hotels_list.append(
                {
                    "name_hotels": f"Название отеля: {response_3['data']['propertyInfo']['summary']['name']}",
                    "sort_element": f"Оценка: {float(sorted_response_2[count_hotel]['reviews']['score'])}",
                    "url": f"Ссылка отеля на сайте Hotels: https://www.hotels.com/h{hotel_id}.Hotel-Information"
                }
            )
            count_photo = 3
            number_photo = 0
            if len(response_3["data"]["propertyInfo"]["propertyGallery"]["images"]) < 3:
                count_photo = len(response_3["data"]["propertyInfo"]["propertyGallery"]["images"])
            for i in range(count_photo):
                info_hotels_list[count_hotel][f"photo_{i}"] = response_3["data"]["propertyInfo"]["propertyGallery"]["images"][i]["image"]["url"]
                number_photo += 1
            info_hotels_list[count_hotel]["number_photo"] = number_photo
    elif dict_result["sort"] == "DISTANCE":
        sorted_response_2 = sorted(
            response_2["data"]["propertySearch"]["properties"],
            key=lambda d: d['destinationInfo']['distanceFromDestination']["value"],
            reverse=True
        )
        for count_hotel in range(int(dict_result["count"])):
            hotel_id = sorted_response_2[count_hotel]["id"]
            response_3 = RequrestsApi.post_full_information_property(
                property_id=hotel_id
            )["result"]
            info_hotels_list.append(
                {
                    "name_hotels": f"Название отеля: {response_3['data']['propertyInfo']['summary']['name']}",
                    "sort_element": f"Расстояние до центра: {sorted_response_2[count_hotel]['destinationInfo']['distanceFromDestination']['value']} км.",
                    "url": f"Ссылка отеля на сайте Hotels: https://www.hotels.com/h{hotel_id}.Hotel-Information"
                }
            )
            count_photo = 3
            number_photo = 0
            if len(response_3["data"]["propertyInfo"]["propertyGallery"]["images"]) < 3:
                count_photo = len(response_3["data"]["propertyInfo"]["propertyGallery"]["images"])
            for i in range(count_photo):
                info_hotels_list[count_hotel][f"photo_{i}"] = response_3["data"]["propertyInfo"]["propertyGallery"]["images"][i]["image"]["url"]
                number_photo += 1
            info_hotels_list[count_hotel]["number_photo"] = number_photo
    else:
        for i in response_2["data"]["propertySearch"]["properties"]:
            if not isinstance(i["star"], (int, float)):
                i["star"] = 0
        sorted_response_2 = sorted(
            response_2["data"]["propertySearch"]["properties"],
            key=lambda d: d['star']
        )
        for count_hotel in range(int(dict_result["count"])):
            hotel_id = sorted_response_2[count_hotel]["id"]
            response_3 = RequrestsApi.post_full_information_property(
                property_id=hotel_id
            )["result"]
            info_hotels_list.append(
                {
                    "name_hotels": f"Название отеля: {response_3['data']['propertyInfo']['summary']['name']}",
                    "sort_element": f"Количество звезд: {float(sorted_response_2[count_hotel]['star'])}",
                    "url": f"Ссылка отеля на сайте Hotels: https://www.hotels.com/h{hotel_id}.Hotel-Information"
                }
            )
            count_photo = 3
            number_photo = 0
            if len(response_3["data"]["propertyInfo"]["propertyGallery"]["images"]) < 3:
                count_photo = len(response_3["data"]["propertyInfo"]["propertyGallery"]["images"])
            for i in range(count_photo):
                info_hotels_list[count_hotel][f"photo_{i}"] = response_3["data"]["propertyInfo"]["propertyGallery"]["images"][i]["image"]["url"]
                number_photo += 1
            info_hotels_list[count_hotel]["number_photo"] = number_photo

    return info_hotels_list
