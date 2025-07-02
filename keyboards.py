from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создаём кнопки
button_hello = KeyboardButton('Привет')
button_goodbye = KeyboardButton('Пока')

# Создаём клавиатуру с двумя кнопками в одном ряду
main_menu_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [button_hello, button_goodbye],
    ]
)