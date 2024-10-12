from typing import List, Any

from db.creat_db import cur, base


def first_add_data_client(tg_user_id, user_name):
    cur.execute("INSERT INTO clients (tg_user_id, user_name)"
                "VALUES(?, ?)", (tg_user_id, user_name))
    base.commit()


# Добавить слиента в базу
# def add_client(phone_number, name, surname, date_of_birth):
#     cur.execute("INSERT INTO clients (phone_number, name, surname, date_of_birth)"
#                 "VALUES(?, ?, ?, ?)", (phone_number, name, surname, date_of_birth))
#     base.commit()


def add_data_client(phone_number, name, surname, date_of_birth, tg_user_id):
    cur.execute("UPDATE clients SET phone_number == ?, "
                "name == ?, "
                "surname == ?, "
                "date_of_birth == ? "
                "WHERE tg_user_id == ?",
                (phone_number, name, surname, date_of_birth, tg_user_id))
    base.commit()


# Изменить данные клиента
def replace_data_client(column_name, new_data, what_replace):
    cur.execute(f"UPDATE clients SET {column_name} == ? WHERE tg_user_id == ?", (new_data, what_replace))
    base.commit()


# Поиск клиента по номеру телефона
def find_client(phone_number):
    result = cur.execute("SELECT * FROM clients WHERE phone_number == ?", (phone_number,)).fetchone()
    # if None == resault:
    #     print(f"Нет клиента с данным номером телефона: {phone_number}")
    # else:
    return result


# Поиск клиента по tg_user_id
def find_client_id(tg_user_id):
    result = cur.execute("SELECT user_name, phone_number, name, surname, date_of_birth FROM clients "
                          "WHERE tg_user_id == ?", (tg_user_id,)).fetchmany(1)
    return result


# Удаление клиента по номеру телефона
def delete_client(what_delete):
    cur.execute(f"DELETE FROM clients WHERE phone_number ==?", (what_delete,))
    base.commit()
