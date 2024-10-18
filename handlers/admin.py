from aiogram import F, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from birthday_today.search_function import ADMIN_LIST
from db.reqests_db import find_all_clients, add_data_client
from keyboards import kb
from support_functions import change_phone_number, checking_date_of_birth

admin_router = Router()


@admin_router.message(Command("admin"))
async def admin_login(message: types.Message):
    if message.from_user.id in ADMIN_LIST:
        await message.answer("Вы вошли в режим аминистратора!",
                             reply_markup=kb.start_kb_admin)


@admin_router.message(F.text == "Выход")
async def exit_admin(message: types.Message):
    await message.answer("Досвидания!", reply_markup=kb.start_kb_user)


@admin_router.message(F.text == "Все клиенты")
async def show_all_clients(message: types.Message):
    result_list = find_all_clients()
    await message.answer(f"Вот:\n{"".join(result_list)}",
                         reply_markup=kb.start_kb_admin)


class AddDataClient(StatesGroup):
    phone_number_client = State()
    name_client = State()
    surname_client = State()
    date_of_birth_client = State()

    texts = {"AddDataClient:phone_number_client": "Пиши номер заново",
             "AddDataClient:name_client": "Пиши имя заново",
             "AddDataClient:surname_client": "Пиши фамилию заново",
             "AddDataClient:date_of_birth_client": "...",
             }


# Отлавливает нажатие кнопки "Добавить данные". Входит в режим FSM, отправляет сообщение пользователю
# и ожидает ответ пользователя. Ввод номера телефона.
@admin_router.message(StateFilter(None), F.text == "Добавить клиента")
async def add_phone_number_client(message: types.Message, state: FSMContext):
    await message.answer("Давай добавим заебал!!!\nНапиши номер телефона",
                         reply_markup=kb.cancel_kb_client)
    await state.set_state(AddDataClient.phone_number_client)


# Отменяет все действия выходит из режима FSM
@admin_router.message(StateFilter("*"), Command("Отменить"))
@admin_router.message(StateFilter("*"), F.text == "Отменить")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Отменил ебать!", reply_markup=kb.start_kb_admin)


# Возвращает на шаг незад
@admin_router.message(StateFilter("*"), Command("Назад"))
@admin_router.message(StateFilter("*"), F.text == "Назад")
async def return_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == AddDataClient.phone_number_client:
        await message.answer("эээ... назад некуда... пиши номер или жми отмену")
        return

    previous = None
    for step in AddDataClient.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вернул к предыдущему шагу. Повнимательнее заебал \n"
                                 f" {AddDataClient.texts[previous.state]}")
            return
        previous = step


# Ввод имени.
@admin_router.message(StateFilter(AddDataClient.phone_number_client), F.text)
async def add_name_client(message: types.Message, state: FSMContext):
    await state.update_data(phone_number_client=change_phone_number(message.text))
    await message.answer("Напиши имя заебал",
                         reply_markup=kb.cancel_kb_client)
    await state.set_state(AddDataClient.name_client)


@admin_router.message(StateFilter(AddDataClient.phone_number_client))
async def add_name_client(message: types.Message, state: FSMContext):
    await message.answer("Че за херню написал??? Пиши номер телефона!!!")


# Ввод фамилии.
@admin_router.message(StateFilter(AddDataClient.name_client), F.text)
async def add_surname_client(message: types.Message, state: FSMContext):
    await state.update_data(name_client=message.text)
    await message.answer("Теперь фамилию ёпта",
                         reply_markup=kb.cancel_kb_client)
    await state.set_state(AddDataClient.surname_client)


@admin_router.message(StateFilter(AddDataClient.name_client))
async def add_surname_client(message: types.Message, state: FSMContext):
    await message.answer("Че за херню написал??? Пиши имя!!!")


# Ввод даты рождения.
@admin_router.message(StateFilter(AddDataClient.surname_client), F.text)
async def add_date_of_birth_client(message: types.Message, state: FSMContext):
    await state.update_data(surname_client=message.text)
    await message.answer("Теперь дату рождения год-месяц-число <-- ВОТ ТАК",
                         reply_markup=kb.cancel_kb_client)
    await state.set_state(AddDataClient.date_of_birth_client)


@admin_router.message(StateFilter(AddDataClient.surname_client))
async def add_date_of_birth_client(message: types.Message, state: FSMContext):
    await message.answer("Че за херню написал??? Пиши фамалию!!!")


# Отправляет сообщение пользователю, что все добавлено. Формирует словарь с данными отправляет в БД.
# После чего удаляет из памяти и выходит из режима FSM.
@admin_router.message(StateFilter(AddDataClient.date_of_birth_client), F.text)
async def add_phone_number_client(message: types.Message, state: FSMContext):
    if checking_date_of_birth(message.text) == False:
        await message.answer("Херню написал!!! Пиши как надо")
    else:
        await state.update_data(date_of_birth_client=message.text)
        await message.answer("Все добавил, устал капец",
                             reply_markup=kb.start_kb_admin)
        data_client = await state.get_data()
        add_data_client(data_client["phone_number_client"], data_client["name_client"],
                        data_client["surname_client"], data_client["date_of_birth_client"])
        await message.answer(f"Проверь заебал!!! \n Телефон: +7{data_client["phone_number_client"]} \n "
                             f"Имя: {data_client["name_client"]} \n "
                             f"Фамилия: {data_client["surname_client"]} \n "
                             f"Дата рождения: {data_client["date_of_birth_client"]}")
        await state.clear()


@admin_router.message(StateFilter(AddDataClient.date_of_birth_client))
async def add_phone_number_client(message: types.Message, state: FSMContext):
    await message.answer("Че за херню написал??? Пиши когда родился!!!")
