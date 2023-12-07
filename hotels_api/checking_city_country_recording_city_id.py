from hotels_api import RequrestsApi
from translator_rus_eng import translator


def checking_city_country_recording_city_id(dict_result: dict) -> int:
    city = translator(dict_result["city"])
    country = translator(dict_result["country"])
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
        return 0
    else:
        return id_city
