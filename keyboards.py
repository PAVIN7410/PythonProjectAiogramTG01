from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="привет"), KeyboardButton(text="пока")]
], resize_keyboard=True)

inline_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="news", url='https://ria.ru/')],
        [InlineKeyboardButton(text="music", url='https://zvuk.com/')],
        [InlineKeyboardButton(text="video", url='https://smotrim.ru/')]
    ]
)





# Клавиатура /initial
async def get_initial_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
        ]
    )

# Новая клавиатура / после клика "Показать больше"
async def get_expanded_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Опция 1", callback_data="option_1"),
        InlineKeyboardButton(text="Опция 2", callback_data="option_2")
    )
    return builder.as_markup()