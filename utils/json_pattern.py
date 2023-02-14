def into_json(
    org_id,
    name,
    address,
    coordinates,
    website,
    opening_hours,
    ypage,
    rating,
    n_reviews,
    phone,
    social,
    stops,
    tags,
):
    """Шаблон файла OUTPUT.json"""

    opening_hours_new = []
    days = ["mo", "tu", "we", "th", "fr", "sa", "su"]

    # Проверка opening_hours на отсутствие одного их рабочих дней
    # Создается отдельный список (opening_hours_new) с полученными значениями
    # Далее он проверяется на отсутствие того или иного рабочего дня
    # На индекс отсутствующего элемента вставляется значение  "   выходной"
    for day in opening_hours:
        opening_hours_new.append(day[:2].lower())
    for i in days:
        if i not in opening_hours_new:
            opening_hours.insert(days.index(i), "   выходной")

    data_grabbed = {
        "ID": org_id,
        "name": name,
        "address": address,
        "coordinates": coordinates,
        "website": website,
        "opening_hours": f"'mon': {opening_hours[0][3:]}, "
        f"'tue': {opening_hours[1][3:]}, "
        f"'wed': {opening_hours[2][3:]}, "
        f"'thu': {opening_hours[3][3:]}, "
        f"'fri': {opening_hours[4][3:]}, "
        f"'sat': {opening_hours[5][3:]}, "
        f"'sun': {opening_hours[6][3:]}",
        "ypage": ypage,
        "rating": rating,
        "n_reviews": n_reviews,
        "phone": phone,
        "social": social,
        "stops": stops,
        "tags": tags,
    }
    return data_grabbed
