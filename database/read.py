"""
Модуль поиска последних десяти запросов поиска
"""

from database import Request, User, Response


def read_db(message: object) -> dict:
    """
    Читает базу данных и собирает последние десять запросов с ответами пользователя

    Parameters:
    message (object): class 'telebot.types.Message'

    Returns:
    dict: список последних запросов с ответами из базы данных
    """
    message = message.from_user.id
    dict_data = dict()
    count_request = None
    count_response = 1

    table_data = (Response
                  .select()
                  .join(Request, on=(Request.id == Response.Request_id))
                  .join(User, on=(User.id == Request.User_id))
                  .where(User.User == message)
                  .order_by(Response.Request_id.desc())
                  )

    for elem in table_data:
        if len(dict_data) > 10:
            dict_data.pop(str(elem.Request_id.id))
            break
        if not count_request == elem.Request_id.id:
            count_response = 1
            count_request = elem.Request_id.id
        if str(elem.Request_id.id) not in dict_data:
            dict_data[str(count_request)] = {
                "request": {
                    "Type": elem.Request_id.Type,
                    "Param_sort": elem.Request_id.Param_sort,
                    "Country": elem.Request_id.Country,
                    "City": elem.Request_id.City,
                    "Arrival_date": elem.Request_id.Arrival_date,
                    "Departure_date": elem.Request_id.Departure_date,
                    "Count_rooms": elem.Request_id.Count_rooms,
                    "Count_adults": elem.Request_id.Count_adults,
                    "Count_children": elem.Request_id.Count_children
                },
                "response": {
                    f"{str(count_response)}": {
                        "Name_hotels": elem.Name_hotels,
                        "Short_info": elem.Short_info,
                        "Url_site": elem.Url_site,
                    }
                }
            }
            count_response += 1
        else:
            dict_data[str(count_request)]["response"][f"{str(count_response)}"] = {
                "Name_hotels": elem.Name_hotels,
                "Short_info": elem.Short_info,
                "Url_site": elem.Url_site,
            }
            count_response += 1

    return dict_data
