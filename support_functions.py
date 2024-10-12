
# Функция принимает на вход номер телефона и приводит его к формату 10 цифр без кода страны.
# Результат типа str Пример: "9001112233"
def change_phone_number(phone_number):
    rev_number = "".join((phone_number.split()))[::-1]
    new_number = "".join(reversed(rev_number[0:10]))
    return new_number


def checking_date_of_birth(date_of_birth):
    rev_date_of_birth = date_of_birth[::-1]
    number = rev_date_of_birth[0:2][::-1]
    month = rev_date_of_birth[3:5][::-1]
    if 0 < int(number) < 32 and 0 < int(month) < 13:
        res = True
    else:
        res = False
    return res
