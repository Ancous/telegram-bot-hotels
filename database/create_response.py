"""
Модуль записи данных ответа в базу данных
"""

from database import Request, Response


def create_response_db(list_result: list) -> None:
    """
    Записывает данные ответа в базу данных

    Parameters:
    list_result (list): список данных с результатами поиска

    Returns:
    None
    """
    req_id = Request.select().order_by(Request.id.desc()).get()
    name = None
    short_info = None
    url_site = None
    photo = list()
    for elem in list_result:
        for key, values in elem.items():
            if key == "name_hotels":
                name = values.split(":")[-1].lstrip()
            elif key == "sort_element":
                short_info = values.split(":")[-1].lstrip()
            elif key == "url":
                url_site = "https:" + values.split(":")[-1].lstrip()
            elif key[:5] == "photo":
                photo.append("https:" + values.split(":")[-1].lstrip())
        photo_result = '\n'.join(photo)
        photo.clear()
        Response.create(
            Request_id=req_id.id,
            Name_hotels=name,
            Short_info=short_info,
            Url_site=url_site,
            Photo=photo_result
        )
