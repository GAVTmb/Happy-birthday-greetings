from aiogram import F, types, Router

from db.reqests_db import first_add_data_client, find_client_id
from keyboards import kb


user_router = Router()


@user_router.message(F.text == "Посмотреть мои данные")
async def add_phone_number_user(message: types.Message):
    tg_user_id = message.from_user.id
    res = find_client_id(tg_user_id)
    await message.answer(f" User name: {res[0][0]} \n"
                         f"Номер телефона: +7{res[0][1]} \n"
                         f"Имя: {res[0][2]} \n"
                         f"Фамилия: {res[0][3]} \n"
                         f"Дата рождения: {res[0][4]}",
                         reply_markup=kb.start_kb_user)


# Отлавливает все сообщения от пользователей. После первого полученного сообщения от пользователя,
# проверяет есть ли он в базе. Если такого пользователя нет, добавляет в базу его id и user name.
# Если польз-ль уже есть в базе, отправлят ему сообщение и кнопки с возможными операциями.
@user_router.message()
async def message_user(message: types.Message):
    tg_user_id = message.from_user.id
    user_name = message.from_user.username
    if bool(len(find_client_id(tg_user_id))) != False:
        await message.answer("Чё надо заебал?", reply_markup=kb.start_kb_user)
    else:
        first_add_data_client(tg_user_id, user_name)
        await message.answer("Здарова заебал!!!", reply_markup=kb.start_kb_user)
