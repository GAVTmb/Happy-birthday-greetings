from aiogram import F, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from db.reqests_db import add_data_user
from keyboards import kb
from support_functions import change_phone_number, checking_date_of_birth

add_user_router = Router()


class AddDataUser(StatesGroup):
    phone_number = State()
    name = State()
    surname = State()
    date_of_birth = State()

    texts = {"AddDataUser:phone_number": "Пиши номер заново",
             "AddDataUser:name": "Пиши имя заново",
             "AddDataUser:surname": "Пиши фамилию заново",
             "AddDataUser:date_of_birth": "...",
             }


# Отлавливает нажатие кнопки "Добавить данные". Входит в режим FSM, отправляет сообщение пользователю
# и ожидает ответ пользователя. Ввод номера телефона.
@add_user_router.message(StateFilter(None), F.text == "Добавить данные")
async def add_phone_number_user(message: types.Message, state: FSMContext):
    await message.answer("Давай добавим заебал!!!\nНапиши свой номер телефона",
                         reply_markup=kb.cancel_kb_user)
    await state.set_state(AddDataUser.phone_number)


# Отменяет все действия выходит из режима FSM
@add_user_router.message(StateFilter("*"), Command("Отмена"))
@add_user_router.message(StateFilter("*"), F.text == "Отмена")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Отменил ёпта!", reply_markup=kb.start_kb_user)


# Возвращает на шаг незад
@add_user_router.message(StateFilter("*"), Command("Назад"))
@add_user_router.message(StateFilter("*"), F.text == "Назад")
async def return_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == AddDataUser.phone_number:
        await message.answer("эээ... назад некуда... пиши свой номер или жми отмену")
        return

    previous = None
    for step in AddDataUser.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вернул к предыдущему шагу. Повнимательнее заебал \n"
                                 f" {AddDataUser.texts[previous.state]}")
            return
        previous = step


# Ввод имени.
@add_user_router.message(StateFilter(AddDataUser.phone_number), F.text)
async def add_name_user(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=change_phone_number(message.text))
    await message.answer("Напиши имя заебал",
                         reply_markup=kb.cancel_kb_user)
    await state.set_state(AddDataUser.name)


@add_user_router.message(StateFilter(AddDataUser.phone_number))
async def add_name_user(message: types.Message, state: FSMContext):
    await message.answer("Че за херню написал??? Пиши номер телефона!!!")


# Ввод фамилии.
@add_user_router.message(StateFilter(AddDataUser.name), F.text)
async def add_surname_user(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь фамилию ёпта",
                         reply_markup=kb.cancel_kb_user)
    await state.set_state(AddDataUser.surname)


@add_user_router.message(StateFilter(AddDataUser.name))
async def add_surname_user(message: types.Message, state: FSMContext):
    await message.answer("Че за херню написал??? Пиши имя!!!")


# Ввод даты рождения.
@add_user_router.message(StateFilter(AddDataUser.surname), F.text)
async def add_date_of_birth_user(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Теперь дату рождения год-месяц-число <-- ВОТ ТАК",
                         reply_markup=kb.cancel_kb_user)
    await state.set_state(AddDataUser.date_of_birth)


@add_user_router.message(StateFilter(AddDataUser.surname))
async def add_date_of_birth_user(message: types.Message, state: FSMContext):
    await message.answer("Че за херню написал??? Пиши фамалию!!!")


# Отправляет сообщение пользователю, что все добавлено. Формирует словарь с данными отправляет в БД.
# После чего удаляет из памяти и выходит из режима FSM.
@add_user_router.message(StateFilter(AddDataUser.date_of_birth), F.text)
async def add_phone_number_user(message: types.Message, state: FSMContext):
    if checking_date_of_birth(message.text) == False:
        await message.answer("Херню написал!!! Пиши как надо")
    else:
        await state.update_data(date_of_birth=message.text)
        await message.answer("Все добавил, устал капец",
                             reply_markup=kb.start_kb_user)
        data = await state.get_data()
        user_id = message.from_user.id
        add_data_user(data["phone_number"], data["name"], data["surname"], data["date_of_birth"], user_id)
        await message.answer(f"Проверь заебал!!! \n Телефон: +7{data["phone_number"]} \n Имя: {data["name"]} \n "
                             f"Фамилия: {data["surname"]} \n Дата рождения: {data["date_of_birth"]}")
        await state.clear()


@add_user_router.message(StateFilter(AddDataUser.date_of_birth))
async def add_phone_number_user(message: types.Message, state: FSMContext):
    await message.answer("Че за херню написал??? Пиши когда родился!!!")
