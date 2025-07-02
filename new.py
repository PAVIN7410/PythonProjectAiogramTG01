import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import asyncio
import config

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=config.TOKEN)
dp = Dispatcher()

# Создаем таблицу, если нужно
def create_table():
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        grade TEXT
    )
    ''')
    conn.commit()
    conn.close()

create_table()

# Стейты
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

# Старт
@dp.message(Command(commands=["start", "register"]))
async def start_cmd(message: types.Message, state: FSMContext):
    await message.answer("Давайте заполнять ваши данные. Как вас зовут?")
    await state.set_state(Form.name)

# Обработка имени
@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Ваш возраст? (числом)")
    await state.set_state(Form.age)

# Обработка возраста
@dp.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите числом ваш возраст.")
        return
    await state.update_data(age=age)
    await message.answer("Ваш класс (например, 5А)?")
    await state.set_state(Form.grade)

# Обработка класса (grade)
@dp.message(Form.grade)
async def process_grade(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    age = data['age']
    grade = message.text

    # Сохраняем в базу
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO students (name, age, grade) VALUES (?, ?, ?)',
        (name, age, grade)
    )
    conn.commit()
    conn.close()

    await message.answer(f"Данные сохранены:\nИмя: {name}\nВозраст: {age}\nКласс: {grade}")
    await state.clear()

#Обработка других сообщений
@dp.message()
async def default_message(message: types.Message):
    await message.answer("Пожалуйста, используйте команду /start или /register для начала.")

# Запуск бота

import asyncio

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))





