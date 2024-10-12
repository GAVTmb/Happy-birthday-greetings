from aiogram import F, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from db.reqests_db import replace_data_client
from keyboards import kb
from support_functions import change_phone_number

replace_user_router = Router()


class ReplaceDataUser(StatesGroup):
    which_data = State()
    new_data = State()


@replace_user_router.message(StateFilter(None), F.text == "Изменить данные")
async def replace_data_user(message: types.Message, state: FSMContext):
    await message.answer("Давай изменим заебал \nЧто будем менять?", reply_markup=kb.replace_kb_user)
    await state.set_state(ReplaceDataUser.which_data)


# Отменяет все действия выходит из режима FSM
@replace_user_router.message(StateFilter("*"), Command("Отмена"))
@replace_user_router.message(StateFilter("*"), F.text == "Отмена")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Отменил ёпта!", reply_markup=kb.start_kb_user)


@replace_user_router.message(StateFilter(ReplaceDataUser.which_data), F.text)
async def which_data(message: types.Message, state: FSMContext):
    res = message.text
    if res == "Имя":
        await state.update_data(which_data="name")
    elif res == "Фамилия":
        await state.update_data(which_data="surname")
    elif res == "Номер телефона":
        await state.update_data(which_data="phone_number")
    else:
        await state.update_data(which_data="date_of_birth")
    await message.answer(f"Напиши {res} заново", reply_markup=kb.del_kb)
    await state.set_state(ReplaceDataUser.new_data)


@replace_user_router.message(StateFilter(ReplaceDataUser.new_data), F.text)
async def new_data(message: types.Message, state: FSMContext):
    await state.update_data(new_data=message.text)
    await message.answer("Все заменил, я красавчег)",
                         reply_markup=kb.start_kb_user)
    data = await state.get_data()
    if data['which_data'] == 'phone_number':
        data['new_data'] = change_phone_number(data['new_data'])
    user_id = message.from_user.id
    replace_data_client(data["which_data"], data["new_data"], user_id)
    await state.clear()


@replace_user_router.message(StateFilter(ReplaceDataUser.new_data))
async def new_data(message: types.Message, state: FSMContext):
    await message.answer("Че за херню написал??? Пиши нормально!!!")
