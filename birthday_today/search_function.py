from datetime import date

from db.creat_db import cur


def birthday_today_selection_from_db():
    res = search_for_matches()
    list_phone_number = []
    for i in res:
        resault = cur.execute("SELECT phone_number, tg_user_id FROM clients WHERE date_of_birth == ?", (i,)).fetchone()
        list_phone_number.append(resault[0])
        print(list_phone_number)
    return list_phone_number


def search_for_matches():
    dates_of_birth = cur.execute("SELECT date_of_birth FROM clients").fetchall()
    print(dates_of_birth)
    date_list = []
    d_n = date.today()
    date_list.append(str(d_n))
    res = []
    for i in dates_of_birth:
        if i[0][5:] in date_list[0][5:]:
            res.append(i[0])
    return res


