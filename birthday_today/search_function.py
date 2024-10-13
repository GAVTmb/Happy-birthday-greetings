from datetime import date

import pytz
import schedule

from db.creat_db import cur


def sending_message():
    list_of_birthday_people = birthday_today_selection_from_db()
    for item in list_of_birthday_people:
        if item["tg_user_id"] == None:
            print(f"отправить напоминание админу. Номер телефона:{item["phone_number"]}")
        else:
            # await bot.send_message(item["tg_user_id"], "С днем рождения!!!")
            print(f"отправить поздравление клиенту. id клиента:{item["tg_user_id"]}")


def birthday_today_selection_from_db():
    res = search_for_matches()
    list_phone_number = []
    for i in res:
        dict_res = {}
        result = cur.execute("SELECT tg_user_id, phone_number FROM clients WHERE date_of_birth == ?", (i,)).fetchone()
        dict_res["tg_user_id"] = result[0]
        dict_res["phone_number"] = result[1]
        list_phone_number.append(dict_res)
        # print(list_phone_number)
    return list_phone_number


def search_for_matches():
    dates_of_birth = cur.execute("SELECT date_of_birth FROM clients").fetchall()
    date_list = []
    d_n = date.today()
    date_list.append(str(d_n))
    res = []
    for i in dates_of_birth:
        if i[0][5:] in date_list[0][5:]:
            res.append(i[0])
    return res


schedule.every(20).seconds.do(sending_message)
# schedule.every().days.at("09:30", pytz.timezone("Europe/Moscow")).do(birthday_today_selection_from_db)
