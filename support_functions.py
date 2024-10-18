
# Функция принимает на вход номер телефона и приводит его к формату 10 цифр без кода страны.
# Результат типа str Пример: "9001112233"
def change_phone_number(phone_number):
    rev_number = "".join((phone_number.split()))[::-1]
    new_number = "".join(reversed(rev_number[0:10]))
    return new_number

# Проверяет на коректность дату рождения.
def checking_date_of_birth(date_of_birth):
    rev_date_of_birth = date_of_birth[::-1]
    number = rev_date_of_birth[0:2][::-1]
    month = rev_date_of_birth[3:5][::-1]
    if 0 < int(number) < 32 and 0 < int(month) < 13:
        res = True
    else:
        res = False
    return res


def data_in_dict(list_data):
    list_result = []
    for item in list_data:
        dict_data = {}
        if item[0] is not None:
            dict_data["id"] = item[0]
        if item[1] is not None:
            dict_data["tg_user_id"] = item[1]
        if item[2] is not None:
            dict_data["user_name"] = item[2]
        if item[3] is not None:
            dict_data["phone_number"] = item[3]
        if item[4] is not None:
            dict_data["name"] = item[4]
        if item[5] is not None:
            dict_data["surname"] = item[5]
        if item[6] is not None:
            dict_data["date_of_birth"] = item[6]
        list_result.append(dict_data)
    return list_result


def text_formation(data):
    generated_text = []
    for item in data:
        text = (f"id: {item.get("id", "")} \n"
                f"Телеграм id: {item.get("tg_user_id", "")} \n"
                f"Имя: {item.get("name", "")} \n"
                f"Фамилия: {item.get("surname", "")} \n"
                f"Номер телефона: +7{item.get("phone_number", "")} \n"
                f"Дата рождения: {item.get("date_of_birth", "")} \n \n")
        generated_text.append(text)
    return generated_text

