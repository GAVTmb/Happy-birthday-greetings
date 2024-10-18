from datetime import date
from aiogram import Bot
import datetime
from db.creat_db import cur

ADMIN_LIST = [1903314478, 253242953]

first_list_of_birthday_peoples = []


# Функфия запускается каждые 5 минут. Проверяет наличие новых клиентов у которых сегодня ДР.
# При появлении таких отправляет им сообщение с поздравлением.
async def checks_every_5_minutes(bot: Bot):
    print("Сработала функция checks_every_5_minutes")
    current_date_time = datetime.datetime.now()
    current_time = str(current_date_time.time())
    if "10" > current_time[0:2] > "23":
        pass
    else:
        new_list = birthday_today_selection_from_db()
        for item in new_list:
            if item in first_list_of_birthday_peoples:
                pass
            else:
                if item.get("tg_user_id") is None:
                    for admin_id in ADMIN_LIST:
                        await bot.send_message(admin_id, f"Сегодня день рождения у \n{item.get("name", "")} "
                                                         f"{item.get("surname", "")} \nС номером телефона: "
                                                         f"+7{item.get("phone_number", "")}\n Не забудьте поздравить!")
                else:
                    await bot.send_message(item["tg_user_id"], f"Сднем рождения {item.get("name")} "
                                                               f"{item.get("surname")}!!!")
                first_list_of_birthday_peoples.append(item)


# Функфия запускается раз в день в определенное время. Отчищает список дней рождений.
async def clearing_list(bot: Bot):
    first_list_of_birthday_peoples.clear()


# Функция получае список с датами рождений(res) вызвая функцию search_for_matches.
# По дате рождения находит клиена в БД, забирает данные клиента(id телеграмм, номер телефона, имя, фамилия).
# Формирует словарь с теми данными клиента которые есть в БД. Добавляет сформиравнные словари в список.
# На выходе получаем список со словарями, в одном словаре данные одного клиента.
def birthday_today_selection_from_db():
    res = search_for_matches()
    final_list_of_birthday_peoples = []
    for i in res:
        dict_res = {}
        result = cur.execute("SELECT tg_user_id, phone_number, name, surname FROM clients WHERE date_of_birth == ?",
                             (i,)).fetchone()
        if result[0] is not None:
            dict_res["tg_user_id"] = result[0]
        if result[1] is not None:
            dict_res["phone_number"] = result[1]
        if result[2] is not None:
            dict_res["name"] = result[2]
        if result[3] is not None:
            dict_res["surname"] = result[3]
        final_list_of_birthday_peoples.append(dict_res)
    return final_list_of_birthday_peoples


# Функция запрашивае из БД дату рождения всех клиентов,
# сравнивает с датой сегодня и добавляет все совпвдения в список-res.
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
