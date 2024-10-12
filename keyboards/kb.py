from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


del_kb = ReplyKeyboardRemove()

start_kb_user = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить данные"),
            KeyboardButton(text="Изменить данные")
        ],
        [
            KeyboardButton(text="Посмотреть мои данные")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder=""
)

cancel_kb_user = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена"),
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder=""
)

replace_kb_user = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Имя"),
            KeyboardButton(text="Фамилия")
        ],
        [
            KeyboardButton(text="Номер телефона"),
            KeyboardButton(text="Дата рождения")
        ],
        [
            KeyboardButton(text="Отмена")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder=""
)
